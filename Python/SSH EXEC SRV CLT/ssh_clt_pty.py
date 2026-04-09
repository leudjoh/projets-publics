#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ssh_client_fixed.py
Client SSH Paramiko corrigé pour éviter blocage après auth.
Supporte : auth par clé ou mot de passe, exec command, shell interactif (PTY).
Utilise un modèle threadé pour l'interaction (stdin->channel, channel->stdout).
"""
from __future__ import annotations
import argparse
import getpass
import sys
import os
import socket
import threading
import select

# Import paramiko (avec tentative d'installation automatique)
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
    paramiko = try_install_and_import("paramiko")
except Exception:
    print("Paramiko requis. Installe manuellement et réessaie.")
    sys.exit(1)

def parse_args():
    p = argparse.ArgumentParser(description="Client SSH Paramiko")
    p.add_argument("--host")
    p.add_argument("--port", type=int, default=2222)
    p.add_argument("--user")
    p.add_argument("--key", help="Chemin vers clé privée (optionnel)")
    p.add_argument("--cmd", help="Commande à exécuter (exec).")
    p.add_argument("--shell", action="store_true", help="Ouvrir shell interactif (PTY).")
    p.add_argument("--known-hosts", help="Fichier known_hosts (optionnel).")
    p.add_argument("--timeout", type=float, default=10.0)
    return p.parse_args()

def load_host_keys_policy(client, known_hosts_path):
    if known_hosts_path and os.path.exists(known_hosts_path):
        client.load_host_keys(known_hosts_path)
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
    else:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def stdin_to_channel(chan):
    """Thread : lit stdin et envoie sur channel (en bytes)."""
    try:
        while True:
            data = os.read(sys.stdin.fileno(), 1024)
            if not data:
                break
            chan.send(data)
    except Exception:
        # fermeture ou erreur -> on ferme le channel si possible
        try:
            chan.shutdown_write()
        except Exception:
            pass

def channel_to_stdout(chan):
    """Thread : lit channel et écrit sur stdout."""
    try:
        while True:
            if chan.recv_ready():
                data = chan.recv(4096)
                if not data:
                    break
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
            else:
                # si channel fermé ou EOF
                if chan.exit_status_ready() and not chan.recv_ready():
                    break
    except Exception:
        pass

def interactive_shell_threaded(chan):
    """
    Lance deux threads : stdin->channel et channel->stdout.
    Compatible en pratique sur la plupart des plateformes.
    """
    # si on est dans un non-tty (redirection), on reste quand même fonctionnel.
    thr_in = threading.Thread(target=stdin_to_channel, args=(chan,), daemon=True)
    thr_out = threading.Thread(target=channel_to_stdout, args=(chan,), daemon=True)
    thr_in.start()
    thr_out.start()
    # attendre la fin : soit channel fermé, soit thread out termine
    try:
        while thr_out.is_alive():
            thr_out.join(timeout=0.1)
    except KeyboardInterrupt:
        # permettre Ctrl-C localement
        try:
            chan.close()
        except Exception:
            pass

def run_exec_via_channel(transport, command, timeout=30):
    chan = transport.open_session(timeout=5)
    chan.exec_command(command)
    out_chunks = []
    err_chunks = []
    while True:
        if chan.recv_ready():
            out_chunks.append(chan.recv(4096))
        if chan.recv_stderr_ready():
            err_chunks.append(chan.recv_stderr(4096))
        if chan.exit_status_ready():
            break
    stdout = b"".join(out_chunks).decode(errors="replace")
    stderr = b"".join(err_chunks).decode(errors="replace")
    exit_status = chan.recv_exit_status()
    chan.close()
    return exit_status, stdout, stderr

def main():
    args = parse_args()

    # Affichage des exemples si aucun argument utile n'est fourni
    if len(sys.argv) == 1:
        print("Usage: ssh_clt_pty.py [-h] --host HOST [--port PORT] --user USER [--key KEY] [--cmd CMD] [--shell] [--known-hosts KNOWN_HOSTS] [--timeout TIMEOUT]")
        print("\n=== Exemples d’utilisation ===\n")
        print("1) Shell interactif :")
        print("   python ssh_clt_pty.py --host 192.168.1.10 --port 2222 --user alice --shell\n")
        print("2) Exécution d'une commande :")
        print("   python ssh_clt_pty.py --host 192.168.1.10 --user bob --cmd \"ls -al\"\n")
        print("3) Utilisation d'une clé privée :")
        print("   python ssh_clt_pty.py --host serveur --user root --key id_rsa --cmd \"whoami\"\n")
        print("4) Port personnalisé :")
        print("   python ssh_clt_pty.py --host cible --port 2200 --user admin --shell\n")
        print("5) Timeout personnalisé :")
        print("   python ssh_clt_pty.py --host 192.168.1.50 --user test --timeout 10 --cmd \"uname -a\"\n")
        sys.exit(0)

    # Vérification des arguments fonctionnels
    if not args.cmd and not args.shell:
        print("Utilise --cmd ou --shell (ou fournis une clé via --key).")
        return

    sshclient = paramiko.SSHClient()
    load_host_keys_policy(sshclient, args.known_hosts)

    # socket + Transport
    try:
        sock = socket.create_connection((args.host, args.port), timeout=args.timeout)
    except Exception as e:
        print("Échec connexion socket :", e)
        return

    transport = paramiko.Transport(sock)

    # Début client SSH
    try:
        transport.start_client(timeout=args.timeout)
    except Exception as e:
        print("Échec negotiation SSH (start_client) :", e)
        transport.close()
        return

    # Auth par clé si fournie
    authenticated = False
    if args.key:
        try:
            try:
                pkey = paramiko.RSAKey.from_private_key_file(args.key)
            except paramiko.PasswordRequiredException:
                pw = getpass.getpass("Passphrase clé privée: ")
                pkey = paramiko.RSAKey.from_private_key_file(args.key, password=pw)
            transport.auth_publickey(args.user, pkey)
            authenticated = transport.is_authenticated()
        except Exception as e:
            print("Authentification par clé échouée:", e)
            authenticated = False

    # Auth par mot de passe si clé absente ou échouée
    if not authenticated:
        pwd = getpass.getpass(f"Mot de passe pour {args.user}@{args.host}: ")
        try:
            transport.auth_password(username=args.user, password=pwd)
            authenticated = transport.is_authenticated()
        except Exception as e:
            print("Authentification par mot de passe échouée:", e)
            authenticated = False

    if not authenticated:
        print("Échec d'authentification.")
        try: transport.close()
        except Exception: pass
        return

    # Vérification transport actif
    if not transport.is_active():
        print("Transport SSH inactif après auth.")
        transport.close()
        return

    # Exécution commande ou shell
    try:
        if args.cmd:
            code, out, err = run_exec_via_channel(transport, args.cmd)
            if out:
                print(out, end="")
            if err:
                print(err, end="", file=sys.stderr)
            print(f"[exit code: {code}]")

        elif args.shell:
            chan = transport.open_session()
            chan.get_pty()
            chan.invoke_shell()
            interactive_shell_threaded(chan)
            try:
                chan.close()
            except Exception:
                pass

    finally:
        try:
            transport.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
