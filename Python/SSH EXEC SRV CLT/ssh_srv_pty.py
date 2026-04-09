#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ssh_server_exec_revised.py
Version réécrite du serveur SSH (Paramiko) fourni par l'utilisateur.
Objectifs principaux implémentés :
 - Support d'un shell interactif réel via PTY (pty.openpty + Popen).
 - Gestion multi-clients (accept en boucle, thread par connexion).
 - Support optionnel d'authentification par clé publique (authorized_keys file).
 - Renforcement du hachage des mots de passe (PBKDF2 par défaut; Argon2 si passlib disponible).
 - Meilleur logging et audit minimal (format datetime + IP + user + action).
 - Meilleure gestion des ressources et nettoyage.

ATTENTION : ce serveur exécute des commandes reçues. Usage uniquement en environnement
contrôlé, jamais en production sans durcissement supplémentaire (sandbox, chroot, containers,
ACLs, monitoring, etc.).

Pour usage local/tests : créer un fichier user_pass.hash contenant "salt_hex:hash_hex" (si mot de passe utilisé),
ou un fichier authorized_keys pour les clés publiques. Cf. variables de configuration ci-dessous.

"""

from __future__ import annotations
import os
import sys
import socket
import threading
import logging
import shlex
import subprocess
import hmac
import hashlib
from pathlib import Path
import ipaddress
import secrets
import getpass
import time
import select
import pty
import errno

# Tentative d'import de paramiko (la même logique d'installation automatique que l'original)
import importlib
import subprocess as _sp

def try_install_and_import(name: str):
    try:
        return importlib.import_module(name)
    except ImportError:
        print(f"[+] {name} non trouvé — tentative d'installation via pip...")
        try:
            _sp.check_call([sys.executable, "-m", "pip", "install", name])
        except Exception:
            print("[!] Impossible d'installer via pip dans cet environnement.")
            raise
        return importlib.import_module(name)

try:
    paramiko = try_install_and_import('paramiko')
except Exception:
    sys.exit(1)

# Optionnel : passlib pour Argon2 (si présent, on l'utilisera)
try:
    from passlib.hash import argon2
    PASSLIB_ARGON2 = True
except Exception:
    PASSLIB_ARGON2 = False

# --- Configuration
CWD = Path(__file__).parent
HOSTKEY_PATH = CWD / 'test_rsa.key'
PASSWORD_HASH_FILE = CWD / 'user_pass.hash'  # format: salt_hex:hash_hex (PBKDF2) OR argon2 hash
# Si PBKDF2 est utilisé, on augmente l'itération par défaut à une valeur raisonnable pour tests.
PASSWORD_HASH_ITER = 400_000
USERNAME_EXPECTED = 'geoffroy'
SOCKET_TIMEOUT = 60
SSH_PORT = 2222
AUTHORIZED_KEYS = CWD / 'authorized_keys'  # optional

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger('ssh_server_exec')

# --- Helpers

def generate_host_key(path: Path):
    log.info('Génération d\'une clé RSA 2048 bits...')
    key = paramiko.RSAKey.generate(2048)
    key.write_private_key_file(str(path))
    try:
        path.chmod(0o600)
    except Exception:
        pass
    log.info('Clé hôte créée : %s', path)


def read_stored_hash(path: Path):
    """Retourne None si absent/invalid. Si passlib/argon2 est utilisé, on renvoie la chaîne complète.
    Si PBKDF2, on renvoie (salt_bytes, hash_bytes).
    """
    if not path.exists():
        return None
    raw = path.read_text().strip()
    # Détection simple : si la ligne contient '$argon2' on renvoie la chaîne (passlib format)
    if raw.startswith('$argon2') or raw.startswith('$argon2i') or raw.startswith('$argon2id'):
        return raw
    try:
        salt_hex, hash_hex = raw.split(':')
        return bytes.fromhex(salt_hex), bytes.fromhex(hash_hex)
    except Exception:
        log.error('Format user_pass.hash invalide (attendu salt:hash ou argon2 string).')
        return None


def create_password_hash_file(path: Path, iterations: int = PASSWORD_HASH_ITER):
    print('[!] user_pass.hash absent — on peut en créer un maintenant.')
    choice = input('Créer user_pass.hash ici ? (o/N) : ').strip().lower()
    if choice != 'o':
        print('OK — pas de fichier créé. Le serveur refusera l\'authentification par mot de passe.')
        return False
    pwd = getpass.getpass('Entrez le mot de passe à stocker (sera haché): ')
    if not pwd:
        print('Mot de passe vide — annulation.')
        return False
    if PASSLIB_ARGON2:
        # stocker la string argon2 complète
        hashed = argon2.hash(pwd)
        path.write_text(hashed)
    else:
        salt = secrets.token_bytes(16)
        hashed = hashlib.pbkdf2_hmac('sha256', pwd.encode('utf-8'), salt, iterations)
        path.write_text(f"{salt.hex()}:{hashed.hex()}")
    try:
        path.chmod(0o600)
    except Exception:
        pass
    print('[+] user_pass.hash créé.')
    return True


def pbkdf2_hash(password: str, salt: bytes, iterations: int = PASSWORD_HASH_ITER):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)


def verify_password(password: str, stored):
    """Retourne True si le mot de passe est correct. """
    if stored is None:
        return False
    if isinstance(stored, str):
        # passlib argon2 string
        if not PASSLIB_ARGON2:
            # si le hash est argon2 mais passlib non installé, on ne peut vérifier
            log.error('Hash Argon2 trouvé mais passlib non disponible.')
            return False
        try:
            return argon2.verify(password, stored)
        except Exception:
            return False
    else:
        salt, stored_hash = stored
        return hmac.compare_digest(pbkdf2_hash(password, salt), stored_hash)


def load_authorized_keys(path: Path):
    """Charge un fichier authorized_keys (OpenSSH public keys). Retourne liste de clé Paramiko.
    Si absent, retourne une liste vide.
    """
    if not path.exists():
        return []
    keys = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        try:
            key = paramiko.RSAKey(data=paramiko.py3compat.decodebytes(line.encode()))
            keys.append(key)
        except Exception:
            try:
                key = paramiko.Ed25519Key(data=paramiko.py3compat.decodebytes(line.encode()))
                keys.append(key)
            except Exception:
                # paramiko peut charger via from_string helpers; on laisse tomber sils ne conviennent pas
                pass
    return keys


# --- Server interface
class Server(paramiko.ServerInterface):
    def __init__(self, client_addr, authorized_keys_list):
        super().__init__()
        self.event = threading.Event()
        self._forward_listeners = {}
        self.client_addr = client_addr
        self.authorized_keys = authorized_keys_list
        self.transport = None

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        # debug demande PTY
        print("PTY REQUEST")
        # accepter le PTY
        return True
    
    def check_channel_shell_request(self, channel):
        # debug ouverture shell
        print("EVENT SET!!")
        # mémorisation channel shell
        self.shell_channel = channel
        # activation event pour signaler un shell
        self.event.set()
        return True

    def check_auth_password(self, username, password):
        log.info('Tentative auth par password: user=%s ip=%s', username, self.client_addr[0])
        if username != USERNAME_EXPECTED:
            return paramiko.AUTH_FAILED
        stored = read_stored_hash(PASSWORD_HASH_FILE)
        if stored is None:
            log.warning('Aucun hash de mot de passe : refus auth par mot de passe.')
            return paramiko.AUTH_FAILED
        if verify_password(password, stored):
            log.info('Authentification password réussie pour %s', username)
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        log.info('Tentative auth par clé publique: user=%s ip=%s', username, self.client_addr[0])
        if username != USERNAME_EXPECTED:
            return paramiko.AUTH_FAILED
        # comparer la clé fournie à la liste autorisée (si présente)
        for allowed in self.authorized_keys:
            try:
                if allowed.get_name() == key.get_name() and allowed == key:
                    log.info('Authentification par clé publique acceptée pour %s', username)
                    return paramiko.AUTH_SUCCESSFUL
            except Exception:
                continue
        log.info('Clé publique non reconnue.')
        return paramiko.AUTH_FAILED

    def check_channel_direct_tcpip_request(self, chanid, origin, destination):
        log.info('Requête TCPIP directe de %s vers %s', origin, destination)
        return paramiko.OPEN_SUCCEEDED

    def check_port_forward_request(self, address, port):
        bind_addr = address if address else '0.0.0.0'
        key = (bind_addr, port)
        if key in self._forward_listeners:
            log.info('Forward déjà en place pour %s:%d', bind_addr, port)
            return port
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind((bind_addr, port))
            server_sock.listen(5)
        except Exception as e:
            log.exception('Impossible de binder %s:%d: %s', bind_addr, port, e)
            return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

        def listener_loop(server_sock, bind_addr, bind_port):
            log.info('Listener forward actif sur %s:%d', bind_addr, bind_port)
            while True:
                try:
                    client_sock, client_addr = server_sock.accept()
                except Exception as e:
                    log.info('Listener fermé ou erreur accept(): %s', e)
                    break
                origin = (client_addr[0], client_addr[1])
                dest = (bind_addr, bind_port)
                try:
                    chan = self.transport.open_forwarded_tcpip_channel(origin, dest)
                except Exception as e:
                    log.exception('Impossible d\'ouvrir channel forwarded-tcpip: %s', e)
                    client_sock.close()
                    continue
                t = threading.Thread(target=relay_socket_channel, args=(client_sock, chan), daemon=True)
                t.start()

        thr = threading.Thread(target=listener_loop, args=(server_sock, bind_addr, port), daemon=True)
        thr.start()
        self._forward_listeners[key] = (server_sock, thr)
        log.info('Request port forward accepted: %s:%d', bind_addr, port)
        return port

    def cancel_port_forward_request(self, address, port):
        bind_addr = address if address else '0.0.0.0'
        key = (bind_addr, port)
        if key not in self._forward_listeners:
            return
        server_sock, thr = self._forward_listeners.pop(key)
        try:
            server_sock.close()
        except Exception:
            pass
        log.info('Forward cancelled for %s:%d', bind_addr, port)
        return


# Relay entre socket TCP et channel (identique)
def relay_socket_channel(sock, chan):
    try:
        sock.setblocking(False)
        chan.settimeout(0.1)
        while True:
            r, _, _ = select.select([sock, chan], [], [], 0.5)
            if sock in r:
                try:
                    data = sock.recv(4096)
                except Exception:
                    data = None
                if not data:
                    break
                try:
                    chan.sendall(data)
                except Exception:
                    break
            if chan in r:
                try:
                    data = chan.recv(4096)
                except Exception:
                    data = None
                if not data:
                    break
                try:
                    sock.sendall(data)
                except Exception:
                    break
    finally:
        try:
            chan.close()
        except Exception:
            pass
        try:
            sock.close()
        except Exception:
            pass


# Execute command safe (utilisé pour exec_command channel)
def execute_command_safe(cmd_str, timeout=20):
    try:
        args = shlex.split(cmd_str)
        if not args:
            return 0, ''
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout, shell=False)
        out = (proc.stdout or '') + (proc.stderr or '')
        return proc.returncode, out
    except subprocess.TimeoutExpired:
        return 124, 'ERROR: timeout expired\n'
    except FileNotFoundError:
        return 127, 'ERROR: command not found\n'
    except Exception as e:
        return 1, f'ERROR: {e}\n'


# Shell PTY handler: relaye PTY <-> channel
def handle_pty_shell(chan):
    """PTY shell handler — plus robuste : select() sur master_fd uniquement,
    et utilisation de chan.recv_ready() pour lire le channel Paramiko."""
    master_fd, slave_fd = pty.openpty()
    shell = os.environ.get('SHELL', '/bin/bash')
    proc = subprocess.Popen(
        [shell],
        preexec_fn=os.setsid,
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True
    )
    os.close(slave_fd)

    try:
        chan.settimeout(0.1)
        while True:
            # attendre sur le PTY (master_fd) un peu — 100ms
            r, _, _ = select.select([master_fd], [], [], 0.1)

            # données provenant du shell -> envoyer vers le channel
            if master_fd in r:
                try:
                    data = os.read(master_fd, 4096)
                except OSError as e:
                    # EIO peut signifier that the slave side is closed
                    if getattr(e, 'errno', None) == errno.EIO:
                        break
                    raise
                if not data:
                    break
                try:
                    chan.sendall(data)
                except Exception:
                    break

            # données provenant du client -> lire via chan.recv() si prêtes
            try:
                while chan.recv_ready():
                    data = chan.recv(4096)
                    if not data:
                        # remote closed
                        break
                    os.write(master_fd, data)
            except Exception:
                # problème de lecture du channel : sortir et nettoyer
                break

            # vérifier si le processus shell est terminé
            if proc.poll() is not None:
                # drain any remaining output
                try:
                    while True:
                        out = os.read(master_fd, 4096)
                        if not out:
                            break
                        try:
                            chan.sendall(out)
                        except Exception:
                            break
                except OSError:
                    pass
                break

            # si le remote a fermé le channel, quit
            if chan.closed:
                break

    finally:
        try:
            chan.close()
        except Exception:
            pass
        try:
            os.close(master_fd)
        except Exception:
            pass
        try:
            proc.terminate()
        except Exception:
            pass



# Par-connexion: gère le transport et les channels pour un client
def handle_client_connection(client_sock, client_addr, hostkey):
    # début thread client
    log.info('Thread client démarré pour %s:%d', client_addr[0], client_addr[1])
    try:
        # création transport SSH
        transport = paramiko.Transport(client_sock)
        transport.add_server_key(hostkey)

        # chargement clés autorisées
        authorized = load_authorized_keys(AUTHORIZED_KEYS)

        # initialisation serveur
        server = Server(client_addr, authorized)
        server.transport = transport
        transport.start_server(server=server)

        # boucle tant que la connexion est active
        while transport.is_active():
            # attente d’un channel
            chan = transport.accept(1)
            if chan is None:
                time.sleep(0.1)
                continue

            # attente des requêtes PTY + SHELL
            print("WAITING FOR SHELL…")
            server.event.wait(5)

            print("SERVER EVENT:", server.event.is_set())

            # mode shell interactif
            if server.event.is_set() and hasattr(server, "shell_channel"):
                print("STARTING SHELL")
                handle_pty_shell(chan)
                continue

            # mode exec simple
            try:
                data = chan.recv(4096).decode(errors='replace')
            except Exception:
                data = ''
            cmd = data.strip()

            if cmd.lower() == 'exit':
                chan.send(b'Bye\n')
                chan.close()
            else:
                ret, out = execute_command_safe(cmd, timeout=30)
                if not out:
                    out = f'(exit {ret})\n'
                chan.send(out.encode())
                chan.close()

    except Exception as e:
        log.exception('Erreur connection client %s: %s', client_addr, e)

    finally:
        try: transport.close()
        except: pass
        try: client_sock.close()
        except: pass

        log.info('Thread client terminé pour %s', client_addr)

# Main server: accepte plusieurs connexions (thread par connexion)
def main():
    bind_addr = '0.0.0.0'
    # host key
    if not HOSTKEY_PATH.exists():
        generate_host_key(HOSTKEY_PATH)
    try:
        hostkey = paramiko.RSAKey(filename=str(HOSTKEY_PATH))
    except Exception as e:
        log.error('Impossible de charger la clé hôte: %s', e)
        sys.exit(1)

    # password hash prompt si absent
    if not PASSWORD_HASH_FILE.exists():
        created = create_password_hash_file(PASSWORD_HASH_FILE)
        if not created:
            log.warning('Pas de user_pass.hash — aucun client ne pourra s\'authentifier par mot de passe.')
    else:
        if read_stored_hash(PASSWORD_HASH_FILE) is None:
            log.error('user_pass.hash mal formaté — corrige et relance.')
            sys.exit(1)

    # socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind_addr, SSH_PORT))
        sock.listen(100)
        sock.settimeout(None)
        log.info('Listening on %s:%d', bind_addr, SSH_PORT)
    except Exception as e:
        log.exception('Erreur bind/listen: %s', e)
        sys.exit(1)

    try:
        while True:
            client, addr = sock.accept()
            log.info('Connexion entrante: %s:%d', addr[0], addr[1])
            t = threading.Thread(target=handle_client_connection, args=(client, addr, hostkey), daemon=True)
            t.start()
    except KeyboardInterrupt:
        log.info('Arrêt demandé par utilisateur.')
    finally:
        try:
            sock.close()
        except Exception:
            pass
        log.info('Serveur arrêté.')


if __name__ == '__main__':
    main()
