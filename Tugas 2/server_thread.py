from socket import *
import socket
import threading
import logging
from time import gmtime, strftime
import sys

class CommandHandler:
    @staticmethod
    def time_command(connection):
        message = f"JAM {strftime('%H:%M:%S', gmtime())}\r\n"
        connection.sendall(message.encode('utf-8'))

    @staticmethod
    def quit_command(connection):
        message = "QUIT MESSAGE BERHASIL DITERIMA\r\n"
        connection.sendall(message.encode('utf-8'))
        connection.close()

    @staticmethod
    def unknown_command(connection):
        message = "WARNING: COMMAND TIDAK DAPAT DIKENAL\r\n"
        connection.sendall(message.encode('utf-8'))

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.address = address

    def run(self):
        while True:
            try:
                data = self.connection.recv(32)
                if data:
                    command = data.decode('utf-8').strip()
                    logging.warning(f"Data received: {command} from client {self.address}.")
                    if command.startswith('TIME') and command.endswith('\r\n'):
                        logging.warning(f"Received TIME command from client {self.address}.")
                        CommandHandler.time_command(self.connection)
                    elif command.startswith('QUIT') and command.endswith('\r\n'):
                        logging.warning(f"Received QUIT command from client {self.address}.")
                        CommandHandler.quit_command(self.connection)
                        break
                    else:
                        logging.warning(f"Unknown command {command} from client {self.address}.")
                        CommandHandler.unknown_command(self.connection)
                else:
                    break
            except OSError:
                break
        self.connection.close()

class Server(threading.Thread):
    def __init__(self, host='0.0.0.0', port=45000):
        super().__init__()
        self.host = host
        self.port = port
        self.clients = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        logging.warning(f"Server listening on {self.host}:{self.port}")

        while True:
            connection, client_address = self.socket.accept()
            logging.warning(f"Connection from {client_address}")

            client_thread = ProcessTheClient(connection, client_address)
            client_thread.start()
            self.clients.append(client_thread)

def main():
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
    server = Server()
    server.start()

if __name__ == "__main__":
    main()
