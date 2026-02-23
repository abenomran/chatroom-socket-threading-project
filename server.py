import argparse
import socket
import sys
import json
import threading
import time

class Server:
    def __init__(self, host, port):
        self.host = host

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()

        self.lock = threading.Lock()

        self.clients = {}

        print(f"Server started on port {port}. Accepting connections")
        sys.stdout.flush()

    def host_server(self):
        while True:
            # accept client
            (clientsocket, address) = self.socket.accept()
            
            # receive client username and passcode 
            data = json.loads(clientsocket.recv(1024).decode())
            client_username, client_passcode = data["username"], data["passcode"]

            # check username and passcode
            if not client_passcode or not client_username:
                continue
            if not self.check_passcode(client_passcode, passcode):
                clientsocket.sendall(b"Incorrect passcode")
                continue
            elif not self.check_username(client_username):
                clientsocket.sendall(b"Username too long")
                continue

            # accept client into chat room
            clientsocket.sendall(f"Connected to {host} on port {port}".encode())
            self.broadcast(f"{client_username} joined the chatroom")
            self.clients[client_username] = clientsocket
            sys.stdout.flush()

            # create client thread to handle oncoming client messages
            client_thread = threading.Thread(target=self.handle_client, args=(client_username, clientsocket), daemon=True)
            client_thread.start()

    def broadcast(self, msg):
        print(msg)
        for client_socket in self.clients.values():
            client_socket.sendall(msg.encode())
        sys.stdout.flush()

    def broadcast_except(self, msg, exception_socket):
        print(msg)
        for client_socket in self.clients.values():
            if client_socket != exception_socket:
                client_socket.sendall(msg.encode())
        sys.stdout.flush()

    def close(self):
        self.broadcast("Server closed")
        for clientsocket in self.clients.values():
            clientsocket.close()
        self.socket.close()

    def check_passcode(self, passcode_input, true_passcode):
        if len(passcode_input) > 5:
            return False
        return passcode_input == true_passcode
    
    def check_username(self, username):
        return len(username) <= 8
    
    def handle_client(self, username, clientsocket):
        while True:
            msg = clientsocket.recv(1024).decode()

            if not msg:
                continue

            self.lock.acquire()

            if msg == ':]':
                self.broadcast_except(username + ": [feeling happy]", clientsocket)
            elif msg == ':[':
                self.broadcast_except(username + ": [feeling sad]", clientsocket)
            elif msg == ":mytime":
                self.broadcast(username + ": " + time.ctime())
            elif msg == ":+1min":
                self.broadcast(username + ": " + time.ctime(time.time() + 60)) # add 60 seconds
            elif msg == ":Users":
                print(username + ": searched up active users")
                sys.stdout.flush()
                userlist_msg = "Active Users: " + ", ".join(self.clients.keys())
                clientsocket.sendall(userlist_msg.encode())
            elif msg.startswith(":dm "):
                dm_command, receiver_username, dm_msg = msg.split(" ", 2)

                dm_msg =  f"[Message from {username}]: {dm_msg}"
                receiver_socket = self.clients[receiver_username]
                receiver_socket.sendall(dm_msg.encode())

                print(username + ": send message to " + receiver_username)
                sys.stdout.flush()
                self.lock.release()
                break
            elif msg == ":Exit":
                clientsocket.close()
                del self.clients[username]
                self.broadcast_except(username + " left the chatroom", clientsocket)
                self.lock.release()
                break
            else:
                self.broadcast_except(username + ": " + msg, clientsocket)
            
            self.lock.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # create args
    parser.add_argument("-start", action="store_true")
    parser.add_argument("-port", type=int)
    parser.add_argument("-passcode")

    # parse args
    args = parser.parse_args()
    port = args.port
    passcode = args.passcode

    host = "127.0.0.1"
    server = Server(host, port)
    try:
        server.host_server()
    finally:
        server.close()
