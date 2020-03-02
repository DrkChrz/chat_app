import socket as soc
from threading import Thread
import sys
import pickle
from time import strftime, gmtime


class ClientClass:
    """
    Class made for communication with client
    """

    def __init__(self):
        """"
        Init object
        """

        self.HOST = "127.0.0.1"
        self.PORT = 1234
        self.s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        self.flag = True
        self.run_client()

    def receive_msg(self):
        """
        Receives messages from server.
        :return: None
        """
        try:
            while True:
                received = self.s.recv(1024)
                received_msg = pickle.loads(received)

                if received_msg[1].strip() == "quit":
                    break
                elif received_msg[0] is None:
                    sys.stdout.write(received_msg[1])
                    sys.stdout.flush()
                else:
                    sys.stdout.write(f"<{received_msg[0]}> {strftime('%H:%M:%S', gmtime())}: ")
                    sys.stdout.write(received_msg[1])
                    sys.stdout.flush()

        except Exception as e:
            print("Exception w client receive:", e)

    def send_msg(self):
        """
        Send messages to server.
        :return: None
        """
        try:
            while True:
                msg = sys.stdin.readline()

                if msg.strip() == "quit":
                    self.s.send(msg.encode())
                    break
                else:
                    sys.stdout.write(f"<You> {strftime('%H:%M:%S', gmtime())}: ")
                    self.s.send(msg.encode())
                    sys.stdout.write(msg)
                    sys.stdout.flush()

        except Exception as e:
            print("exception w client send", e)

    def run_client(self):
        """
        Connects to the server on a given IP address and Port. Starts threads for sending and receiving messages
        :return: None
        """
        try:
            self.s.connect((self.HOST, self.PORT))
            msg = self.s.recv(1024).decode()
            inp = input(msg)
            self.s.send(inp.encode())
            send_thread = Thread(target=self.send_msg)
            receive_thread = Thread(target=self.receive_msg)
            send_thread.start()
            receive_thread.start()
            receive_thread.join()
            self.s.close()
            print("You have been disconnected")

        except Exception as e:
            print("Exception w client main", e)


if __name__ == "__main__":
    ClientClass()
