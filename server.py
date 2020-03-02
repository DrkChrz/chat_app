import socket as soc
from threading import Thread
from guest import Guest
from time import gmtime, strftime
import pickle

# GLOBAL CONSTANTS
PORT = 1234
HOST = "127.0.0.1"

# GLOBAL VARIABLES
list_of_guests = []         # gathers data of users joining server


def server_input():
    """
    Thread waiting for input from user to server.
    Showing simple user stats.
    :param: None
    :return: None
    """
    while True:
        server_inp = input()
        if server_inp == "help":
            print("To see user stats type stats 'user_name'")
        elif server_inp.split()[0] == "stats":             # checking if input consists of first part of command
            for guest in list_of_guests:                   # if so check if second part is one of users using the server
                if server_inp.split()[1] == guest.get_name():
                    print(f"User: {guest.get_name()} | joined server: {guest.when_joined}\n")
            continue


def say_to_all(msg, conn, name=None):
    """
    Takes message from user and send it to other users. Name can be None if welcoming message is being send to all users
    by server. Data can be send over socket if it is bytes so list of [name, message] is serialized.
    :param msg: msg to be send to other users
    :type msg: str
    :param conn: sending user's socket
    :type conn : socket
    :param name: name of the user who sent the message. Message will not be sent to that user
        (default is None)
    :type name: str
    :return: None
    """
    tab_to_send = pickle.dumps([name, msg])                 # serializing data for sending over socket

    for guest in list_of_guests:
        if guest.get_connection() is not conn:              # condition checking if message was send by this user
            guest.get_connection().send(tab_to_send)
        else:                                               # if was send by this user it will continue to the next user
            continue


def communication(guest):
    """
    thread receiving messages and controlling communication. Closing socket if requested.
    :param guest: user's object
    :type guest: Guest
    :return: None
    """
    try:
        while True:
            msg = guest.get_connection().recv(1024).decode()        # waiting to receive msg from users
            """ socket.recv() is blocking socket. To close connection with user requesting to quit, it's sending quit
            message back to him/her to unblock this socket and than close it in this side. """
            if msg.strip() == "quit":
                close_response = pickle.dumps(["server", "quit"])   # serializing data to be send back to user
                guest.get_connection().send(close_response)
                guest.get_connection().close()                      # closing connection on this side
                """sending farewell message to everyone on the server"""
                say_to_all(f"{guest.get_name()} has left chat. Time: {strftime('%Y-%m-%d %H:%M:%S', gmtime())}\n",
                           guest.get_connection())
                list_of_guests.remove(guest)                        # removing user that quit from list of current users
                print("...user left...")
                print(f"{guest.get_name()} has left chat. Time: {strftime('%Y-%m-%d %H:%M:%S', gmtime())}\n", )
                break
            else:
                """ if message is not to "quit" it's sending it to other users on the server"""
                say_to_all(msg, guest.get_connection(), guest.get_name())
    except Exception as e:
        print("Exception in server - communication: ", e)


def run_server():
    """
    Setting up server. Wait for connection from new clients, starts server_input thread and communication thread.
    Socket with context manager is used to close socket automatically when it finish it's job
    :return: None
    """
    with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
        s.bind((HOST, PORT))                                      # set up server
        print("...server started...\n")
        Thread(target=server_input).start()                       # starting thread to get input from user to the server
        s.listen(10)                                              # open server to listen for connections
        while True:
            try:
                conn, addr = s.accept()                              # wait for any for connections
                print("...new user connected...")
                conn.send("Please provide your name: ".encode())     # server to provide name for identification
                name = conn.recv(1024).decode()                      # first message received is always the persons name
                when_joined = strftime('%Y-%m-%d %H:%M:%S', gmtime())

                """creates a new guest object and adds it to the list of guest """
                list_of_guests.append(Guest(conn, addr, when_joined))
                list_of_guests[-1].set_name(name)                    # sets the name for a new guest object

                """sending welcome message to every user on the server but the one that joined"""
                welcome = f"{list_of_guests[-1].get_name()} just joined! Time: {when_joined}\n"
                say_to_all(welcome, list_of_guests[-1].get_connection())
                print(f"connection from: {addr[0]}, port: {addr[1]}. Hello {list_of_guests[-1].get_name()}"
                      f". Time: {strftime('%Y-%m-%d %H:%M:%S', gmtime())}\n")

                Thread(target=communication, args=(list_of_guests[-1],)).start()    # starts communication thread

            except Exception as e:
                print("Exception in server - run server: ", e)


def main():
    run_server()
    print("Server shut down")


if __name__ == "__main__":
    main()
