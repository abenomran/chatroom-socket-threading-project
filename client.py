import argparse
import socket
import sys
import json
import threading

class Client:
    def __init__(self, host, port, data):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.data = data

    def connect(self):
        # connect to socket on local host at the given port
        self.socket.connect((self.host, self.port))

        # send user/pass details to server
        self.socket.sendall(json.dumps(self.data).encode())
        server_response = self.socket.recv(1024).decode()
        print(server_response)
        sys.stdout.flush()
        if server_response == "Incorrect passcode":
            return
        
        # now connected to server
        # create client thread to handle oncoming client messages
        self.disconnection_event = threading.Event()
        receiver_thread = threading.Thread(target=self.handle_server, args=(), daemon=True)
        receiver_thread.start()

        while not self.disconnection_event.is_set():
            user_input = input()
            self.socket.sendall(user_input.encode())
        self.close()

    def handle_server(self):
        while True:
            data = self.socket.recv(1024)
            if not data:
                break

            print(data.decode())
            sys.stdout.flush()
        self.disconnection_event.set()

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # create args
    parser.add_argument("-host")
    parser.add_argument("-join", action="store_true")
    parser.add_argument("-username")
    parser.add_argument("-passcode")
    parser.add_argument("-port", type=int)

    # parse args
    args = parser.parse_args()
    host = args.host
    port = args.port
    data = {
        "username": args.username,
        "passcode": args.passcode
    }

    client = Client(host, port, data)
    client.connect()


