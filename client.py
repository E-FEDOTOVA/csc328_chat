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
from datetime import datetime
from library import make_word_packet, send_message, read_message

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
#   nickname - nickname to be sent
def send_name(sock, name):
    try:
        sock.sendall(name)
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
                nickname = input("Enter your nickname: ")
                send_name(sock, len(nickname).to_bytes(2, 'big') + nickname.encode())

                while True:
                    response = get_message(sock)
                    if response:
                        if response.strip() == "READY":
                            print("Nickname accepted. Start chatting.")
                            break
                        elif response.strip() == "RETRY":
                            print("Nickname already taken. Choose another.")
                            nickname = input("Enter your nickname: ") 
                            send_name(sock, len(nickname).to_bytes(2, 'big') + nickname.encode())
                
                while True:
                    message = input(f"{nickname} [You]: ")
                    send_message(sock, nickname, message)

        except KeyboardInterrupt:
            print("Exiting...")
            sock.close()
    else:
        print("Connection failed. Exiting.")

if __name__ == "__main__":
    main()
