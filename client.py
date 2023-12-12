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
import time
from datetime import datetime 
import library   

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
        sock.sendall(message)  # Sending the encoded??? message through the socket
    except Exception as e:
        print("Failed to send message: {}".format(str(e)))  # Handling message sending errors

# Function name: get_message
# Description: receives a message from the socket
# Parameters:
#   sock - connected socket object
# Return Value:
#   received message if successful, otherwise None
def get_message(sock):               
    while True:
            data = sock.recv(2)  # receive word packets in 2 byte increments
            if not data:
                break

            str_len = int.from_bytes(data, "big")  # bytes to integers big-endian
            data = sock.recv(str_len)
            print(data.decode())  # decode word packets and print it
            return data.decode()  # return received message
        

#def really_read(s, n):
#    bytes = b''
#    while len(bytes) != n:
#        curr_read = s.recv(n - len(bytes))
#        bytes += curr_read
#        if len(curr_read) == 0: break
#    return bytes


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
            print("Connected to chat server")

            # Receive HELLO from server
            hello_msg = get_message(sock)
            if hello_msg.strip() == "HELLO":
                nick_word = get_message(sock) # receive the NICK word from server
                nickname = input("Enter your nickname: ")
                send_message(sock, library.make_word_packet("NICK", nickname))

                while True:
                    response = get_message(sock)
                    if response:
                        response_data = json.loads(response)
                        if "RETRY" in response_data:
                            print("Nickname already taken. Choose another.")
                            nickname = input("Enter your nickname: ")
                            send_message(sock, library.make_word_packet("NICK", nickname))
                        elif "READY" in response_data:
                            print("Nickname accepted. Start chatting.")
                            break

                while True:
                    message = input("Enter message: ")

                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    send_data = {
                        "NICK": nickname, "TIME": timestamp, "MESSAGE": message
                    }
                    send_message(sock, library.make_word_packet("MSG", json.dumps(send_data)))

                    print(f"{nickname}({timestamp}): {message}")

                    received_data = get_message(sock)
                    if received_data:
                        received_data = json.loads(received_data)
                        received_nick = received_data.get("NICK", "")
                        received_time = received_data.get("TIME", "")
                        received_message = received_data.get("MESSAGE", "")
                        print(f"{received_nick}({received_time}): {received_message}")

        except KeyboardInterrupt:
            confirm = input("Are you sure you want to exit? (y/n)")
            if confirm.lower() == 'y':
                send_message(sock, library.make_word_packet("BYE", "Disconnecting..."))
                time.sleep(1)  #delay before closing
                sock.close()
                print("Connection closed")
            else:
                print("Okay! Keep chatting")
    else:
        print("Connection failed. Exiting.")

if __name__ == "__main__":
    main()
