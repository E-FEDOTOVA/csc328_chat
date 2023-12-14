#!/usr/bin/env python3

# Author: Kate Fedotova
# Major: Computer Science
# Due Date: December 14, 2023
# Course: CSC328-010
# Professor Name: Dr. Schwesinger
# Filename: client.py
# Purpose: client program for a chat server that connects 
# to a chat server, and after a nickname is chosen, sends, 
# and gets messages

import socket
import sys
import json
import os
from datetime import datetime
import library
import time
import logging

# Function name: connect_to_server
# Description: connect to a remote server using a TCP socket
# Parameters:
#   host - IP address of the server to connect to
#   port - port number on the server to establish the connection
# Return Value:
#   sock - connected socket object if the connection is successful or none if failed
def connect_to_server(host, port):
    try:
        if not (10000 <= port <= 65535):
            raise ValueError("Port number must be between 10000 and 65535")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock
    except Exception as e:
        print("Could not connect to socket: {}".format(str(e)))
        return None

# Function name: send_name
# Description: sends a nickname through the socket
# Parameters:
#   sock - connected socket object
#   name - nickname to be sent
def send_name(sock, name):
    try:
        nickname_length = len(name).to_bytes(2, 'big')
        sock.sendall(nickname_length + name)
    except Exception as e:
        print("Failed to send nickname: {}".format(str(e)))

# Function name: get_message 
# Description: receives a message from the socket
# Parameters:
#   sock - connected socket object
# Return Value:
#   received message if successful, otherwise None
def get_message(sock):
    while True:
        data = sock.recv(2)
        if not data:
            break

        str_len = int.from_bytes(data, "big")
        data = sock.recv(str_len)
        return data.decode()
        
#Function name: read_messages
#Description: listens to incoming messages from the connected socket in a child process.
#    prints received messages from other clients and prompts for sending new messages.
#Parameters:
#    sock - connected socket object
#    nickname - the nickname of the current user
def read_messages(sock, nickname):
    #while True:
    other_client_message = get_message(sock);
    if other_client_message is None:
        pass
    else:
        print(other_client_message)
    #other_client_message = library.read_message(sock)
    #if not other_client_message:
    #    send_messages(sock, nickname)
    #else:
    #    print("\x1b[32m" + other_client_message['nickname'] + "\x1b[0m: " + other_client_message['message'])
    #    send_messages(sock, nickname)

#Function name: send_messages
#Description: takes user input for messages and sends them to the server through the socket.
#Parameters:
#    sock - connected socket object
#    nickname - the nickname of the current user
def send_messages(sock, nickname):
    while True:
        message = input("\033[36m" + f"{nickname} [You]: " + "\033[0m")
        if message.strip():
            library.send_message(sock, nickname, message)
        else:
            print("Message cannot be empty. Please enter a valid message.")


def main():
    if len(sys.argv) != 3:
        print("Wrong number of command-line arguments, provide <host> <port>")
        return 

    host = sys.argv[1]
    port = int(sys.argv[2])

    sock = connect_to_server(host, port)

    if sock:
        try:
            print("Connected to chat server")

            hello_msg = get_message(sock)
            if hello_msg.strip() == "HELLO":
                # Wait for server to send NICK
                nick_msg = get_message(sock)
                if nick_msg.strip() == "NICK":
                    while True:
                        nickname = input("Enter your nickname: ")
                        if nickname.strip():  #
                            send_name(sock, len(nickname).to_bytes(2, 'big') + nickname.encode())

                            response = get_message(sock)
                            if response.strip() == "READY":
                                print("Nickname accepted. Start chatting.")
                                break
                            elif response.strip() == "RETRY":
                                print("Nickname already taken. Choose another.")
                        else:
                            print("Nickname cannot be empty. Please enter a valid nickname.")

                    pid = os.fork()
                    if pid == 0:  # child process
                        #input(" ")
                        print(" ")
                        read_messages(sock, nickname)  # incoming messages
                    else:
                        send_messages(sock, nickname)  # send messages

        except KeyboardInterrupt:
            library.send_message(sock, nickname, "BYE")
            sock.close()
    else:
        print("Connection failed. Exiting.")

if __name__ == "__main__":
    main()
