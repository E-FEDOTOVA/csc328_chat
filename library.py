#!/usr/bin/env python3

# Lauren Engel
# CSC 328, Fall 2023, Final Project
# Library Functions

import datetime
import json
import socket
import sys

# Description: Allows a socket to send a word packet containing a message
# Parameters: socket sending_socket - socket sending the message
#             string nickname - name of the client sending the message, or "server" if the server is sending the message
#             string message - message to be sent
# Return Value: None
def send_message(sending_socket, nickname, message):
    packet = make_word_packet(nickname, message)
    sending_socket.sendall(packet)

# Description: Allows a socket to read a word packet containing a message
# Parameters: socket receiving_socket - socket reading the message
#             bytes packet - word packet in bytes
# Return Value: dict_packet - word packet as a dictionary
def read_message(receiving_socket, packet):
    json_packet = packet.decode()
    dict_packet = json.loads(data)
    return dict_packet
#    bytes = b''
#    while len(bytes) != length:
#        curr_read = receiving_socket.recv(length - len(bytes))
#        bytes += curr_read
#        if len(curr_read) == 0: break
#    return bytes

# Description: Makes a word packet in a JSON format
# Parameters: string nickname - name of the client sending the message, or "server" if the server is sending the message
#             string message - message to be sent
# Return Value: json_packet - json word packet in bytes with nickname, message, and length of message
def make_word_packet(nickname, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    packet = {"timestamp": timestamp, "nickname" : nickname, "message" : message}
    json_packet = json.dumps(packet)
    return json_packet.encode()
