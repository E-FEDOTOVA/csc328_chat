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
                    messages = input("Enter message: ")  # Message prompt

                    #Sending message with timestamp
                    timestamp = datetime.now().strftime("") # FINISH the timestamp format
                    send_data = {
                        "NICK": nickname, "TIME": timestamp, "MESSAGE": message
                    }
                    send_message(sock, json.dumps(send_data)) # Send message to server

                    print(f"{nickname}({timestamp}):{message}") # Print the nickname, timestamp, and message

                    # Get and display messages from server
                    received_data = get_message(sock) # Recieving data from the server
                    if received_data:
                        received_data = json.loads(received_data) # Load the data
                        received_nick = received_data.get("NICK", "") # Sender's nickname
                        received_time = received_data.get("TIME", "") # The timestamp
                        received_message = received_data.get("MESSAGE", "") # Message content
                        print(f"{received_nick}({received_time}):{received_message}") # Print the nickname, timestamp, and message

        except KeyboardInterrupt:     
            confirm = input("Are you sure you want to exit? (y/n)")
            if confirm == 'y':
                send_message(sock, json.dumps({"BYE": "Disconnecting..."}))
                sock.close()
                print("Connection closed")
            else:
                print("Okay! Keep chatting")
    else:
        print("Connection failed. Exiting.") # Connection failure

if __name__ == "__main__":
    main()
                        
