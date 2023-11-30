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
#import library  

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

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP socket
        sock.connect((host, port))  # Connecting to the server using the provided host and port
        return sock  # Returning the connected socket object
    except Exception as e:
        print("Could not connect to socket: {}".format(str(e)))  # Handling connection errors
        return None

# Function name: send_message
# Description: sends a message through the socket
# Parameters:
#   sock - connected socket object
#   message - message to be sent
def send_message(sock, message):
    try:
        sock.sendall(message.encode())  # Sending the encoded??? message through the socket
    except Exception as e:
        print("Failed to send message: {}".format(str(e)))  # Handling message sending errors

# Function name: get_message
# Description: receives a message from the socket
# Parameters:
#   sock - connected socket object
# Return Value:
#   received message if successful, otherwise None
def get_message(sock):
    try:
        data = sock.recv(1024)  # Receiving data from the socket
        if data:
            return data.decode()  # Returning the decoded received data
        else:
            return None
    except Exception as e:
        print("Failed to receive message: {}".format(str(e)))  # Handling message receiving errors
        return None

# Function name: main
# Description: main function of the client program
def main():
    if len(sys.argv) != 3:  # Checking if the number of command-line arguments is correct
        print("Wrong number of command-line arguments, provide <host> <port>")
        return

    host = sys.argv[1]  # Retrieving host from command-line arguments
    port = int(sys.argv[2])  # Retrieving port from command-line arguments

    sock = connect_to_server(host, port)  # Connecting to the server

    if sock:
        try:
            # Connection established
            print("Connected to chat server")

            # Receive HELLO from server
            hello_msg = get_message(sock)  # Receiving initial message from server
            if hello_msg.strip() == "HELLO":  # Checking if the received message is "HELLO"
                nickname = input("Enter your nickname: ")  # Prompting user for a nickname
                send_message(sock, json.dumps({"NICK": nickname}))  # Sending nickname to the server

                # Wait for server response
                while True:
                    response = get_message(sock)  # Receiving response from the server
                    if response:
                        response_data = json.loads(response)  # Loading received JSON data
                        if "RETRY" in response_data:  # Checking if the server requests a new nickname
                            print("Nickname already taken. Choose another.")
                            nickname = input("Enter your nickname: ")  # Prompting for a new nickname
                            send_message(sock, json.dumps({"NICK": nickname}))  # Sending new nickname
                        elif "READY" in response_data:  # Checking if the nickname is accepted
                            print("Nickname accepted. Start chatting.")
                            break  # Breaking the loop when nickname is accepted

                # Chat loop
                while True:
                    #do stuff

if __name__ == "__main__":
    main()
                        