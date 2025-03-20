import socket
import select
from datetime import datetime
import logging
from User import User
from message import Message
from chat import Chat, PrivateChat, GroupChat

class Server:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.open_client_sockets = []
        self.open_users_sockets = []
        self.messages_to_send = []
        self.managers = ['@mgr1', '@mgr2', '@mgr3']
        self.users = []
        self.silent_users = []
        self.delimiter = ';'
        logging.basicConfig(filename='server.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        print("Server is up")

    def send_waiting_messages(self, wlist):
        for message in self.messages_to_send:
            (client_socket, data) = message
            if client_socket in wlist:
                client_socket.send(data)
                self.messages_to_send.remove(message)

    def append_messages_to_send_all(self, from_socket, data):
        if not self.is_silent_socket(from_socket):
            for soc in self.open_client_sockets:
                if soc != from_socket:
                    self.messages_to_send.append((soc, data))

    def append_messages_to_send(self, to_user, data):
        to_socket = self.get_client_socket(to_user)
        self.messages_to_send.append((to_socket, data))

    def notify_open_clients(self, user):
        message = self.build_message(user, "1", "has left the chat!")
        for soc in self.open_client_sockets:
            self.messages_to_send.append((soc, message))

    def build_message(self, user, cmd, addition):
        now = datetime.now()
        time = now.strftime("%H:%M")
        message = f"{time}{self.delimiter}{user}{self.delimiter}{cmd}{self.delimiter}{addition}"
        return message.encode()

    def register_user(self, user, socket):
        if not any(u == user for u, s in self.open_users_sockets):
            self.open_users_sockets.append((user, socket))

    def unregister_user(self, user, socket):
        self.open_users_sockets.remove((user, socket))

    def get_client_socket(self, user):
        for u, s in self.open_users_sockets:
            if u == user:
                return s
        return None

    def is_silent_socket(self, soc):
        return any(soc == s for u, s in self.silent_users)

    def reply_to_client(self, user, cmd, reply):
        if cmd != 0:
            client_soc = self.get_client_socket(user)
            msg = self.build_message(user, str(cmd), reply)
            self.messages_to_send.append((client_soc, msg))

    def handle_command(self, socket, data):
        parts = data.split(self.delimiter)
        if len(parts) < 4:
            print('handle_command: Illegal command')
            return False
        else:
            r_time, user, cmd, info = parts[0], parts[1], int(parts[2]), parts[3]
            self.register_user(user, socket)
            if cmd == 0:  # login
                self.verify_user(socket, user)
            elif cmd == 1:  # send message
                self.append_messages_to_send_all(socket, data.encode())
            elif cmd == 2:  # appoint new manager
                mgr = info
                if mgr[0] == '@' and mgr not in self.managers:
                    self.managers.append(mgr)
                    print(f"{mgr} added as manager")
                    message = self.build_message(user, "2", f"{mgr} added as manager")
                    self.append_messages_to_send(user, message)
            elif cmd == 3:  # kick off user
                if user[0] == '@':  # if manager
                    usr = info
                    soc = self.get_client_socket(usr)
                    if soc:
                        self.open_client_sockets.remove(soc)
                        self.unregister_user(usr, soc)
                        soc.close()
                        self.notify_open_clients(usr)
                        print("Connection with client closed. Kick off")
                else:
                    print('User not allowed to kick off other user')
            elif cmd == 4:  # silent user
                if user[0] == '@':  # if manager
                    usr = info
                    soc = self.get_client_socket(usr)
                    if soc:
                        self.silent_users.append((usr, soc))
                        print(f"{usr} is silent")
                        self.reply_to_client(usr, str(cmd), f"{usr} is silent")
                else:
                    print('User not allowed to silent other user')
            elif cmd == 5:  # private message
                to_usr, m = info.split(':')
                message = self.build_message(user, "5", m)
                logging.debug(message)
                self.append_messages_to_send(to_usr, message)
            elif cmd == 6:  # view managers
                mgr_list = '\n'.join(self.managers)
                message = self.build_message(user, "6", mgr_list)
                self.append_messages_to_send(user, message)
            elif cmd == 7:  # unsilent user
                if user[0] == '@':  # if manager
                    usr = info
                    soc = self.get_client_socket(usr)
                    if (usr, soc) in self.silent_users:
                        self.silent_users.remove((usr, soc))
                        print(f"{usr} is unsilent")
                else:
                    print('User not allowed to unsilent other user')
            elif cmd == 8:  # quit
                self.open_client_sockets.remove(socket)
                self.unregister_user(user, socket)
                socket.close()
                self.notify_open_clients(user)
                print("Connection with client closed.")
            else:
                print("Unhandled command")

    def verify_user(self, socket, user):
        now = datetime.now()
        time = now.strftime("%H:%M")
        header = f"{time}{self.delimiter}{user}{self.delimiter}0{self.delimiter}".encode()

        if user[0] == '@':
            if user in self.managers and (user, socket) not in self.users:
                self.users.append((user, socket))
                message = header + b'2'
            else:
                message = header + b'0'
        elif (user, socket) not in self.users:
            self.users.append((user, socket))
            message = header + b'2'
        else:
            message = header + b'0'

        self.messages_to_send.append((socket, message))

    def run(self):
        while True:
            rlist, wlist, xlist = select.select([self.server_socket] + self.open_client_sockets, self.open_client_sockets, [])
            for current_socket in rlist:
                if current_socket is self.server_socket:
                    new_socket, address = self.server_socket.accept()
                    self.open_client_sockets.append(new_socket)
                else:
                    data = current_socket.recv(1024).decode()
                    print(data)
                    self.handle_command(current_socket, data)
            self.send_waiting_messages(wlist)

if __name__ == "__main__":
    server = Server()
    server.run()