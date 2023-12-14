#!/usr/bin/env python3

# Zachary Andruchowitz
# CSC 328, Fall 2023, Final Project
# Chat Server

import json
import sys
import socket
import random
import signal
import library
import os
import time

all_nicks = []
all_socks = []

# Remove log file if it exists
try:
    os.remove("log.txt")
except OSError as e:
    pass

# Description: Receives chats from a client and sends it to the other clients
# Parameters: socket conn - originating client connection
#             string nickname - originating client nickname
#             list all_nicks - list of all client nicknames
#             list all_socks - list of all client connections
# Return Value: None
def receive_chats(conn, nickname, all_nicks, all_socks):
    while True:
            chat_message = library.read_message(conn)
            if chat_message:
                print(chat_message['nickname'] + ": " + chat_message['message'])
            else:
                break

            if chat_message['message'] == "BYE":
                conn.close()
                all_nicks.remove(nickname)
                all_socks.remove(conn)
                break
                # child process stuff?
            else:
                with open('log.txt', 'r+') as f:
                    messages = f.read().encode()
                    length = len(messages).to_bytes(2, 'big')
                conn.sendall(length + messages)

                with open('log.txt', 'a') as f:
                    print(str(chat_message) + "\n", file=f)

# Description: Main function. Creates processes for and interacts with client
# Parameters: None
# Return Value: 0 if successful, -1 if error occurred
def main():
    if len(sys.argv) != 2:
        exit("Usage: server <port>")
    try:
        with socket.socket() as s:
            s.bind(('', int(sys.argv[1])))
            s.listen(1)
            while True:
                conn, _ = s.accept()
                with conn:
                    # Send hello to connecting client
                    conn.sendall(len("HELLO").to_bytes(2, 'big') + "HELLO".encode())

                    # Get unique nickname from client
                    # unique = 0
                    conn.sendall(len("NICK").to_bytes(2, 'big') + "NICK".encode())

                    while True:
                        word_length = int.from_bytes(library.really_read(conn, 2), 'big')
                        nickname = library.really_read(conn, word_length).decode()

                        if nickname in all_nicks:
                            conn.sendall(len("RETRY").to_bytes(2, 'big') + "RETRY".encode())
                        else:
                            conn.sendall(len("READY").to_bytes(2, 'big') + "READY".encode())
                            all_socks.append(conn)
                            all_nicks.append(nickname)
                            break
                        time.sleep(1)

                    pid = os.fork()
                    if pid == 0:  # child process
                        while True:
                            if not receive_chats(conn, nickname, all_nicks, all_socks):
                                break
                        exit()  # exit child process
                    elif pid > 0:
                        os.wait()

    except OSError as e:
        exit(e)
    except KeyboardInterrupt:
        print("\nClosing in 5 seconds...")
        message = "Closing in 5 seconds..."
        for sock in all_socks:
            if sock.fileno() != -1:
                library.send_message(sock, nickname, chat_message)
        time.sleep(5)
        exit()

if __name__ == "__main__":
    main()
