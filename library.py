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

# Description: Reads all bytes of a word packet (taken from Dr. Schwesinger)
# Parameters: s - socket to read from
#             n - number of bytes to read
# Return Value: bytes - bytes read
def really_read(s, n):
    bytes = b''
    while len(bytes) != n:
        curr_read = s.recv(n - len(bytes))
        bytes += curr_read
        if len(curr_read) == 0: break
    return bytes

# Description: Allows a socket to read a word packet containing a message
# Parameters: socket receiving_socket - socket reading the message
#             bytes packet - word packet in bytes
# Return Value: dict_packet - word packet as a dictionary
def read_message(receiving_socket):
    packet_length = int.from_bytes(really_read(receiving_socket, 2), 'big')
    packet = really_read(receiving_socket, packet_length)
    json_packet = packet.decode()
    dict_packet = json.loads(data)
    return dict_packet

# Description: Makes a word packet in a JSON format
# Parameters: string nickname - name of the client sending the message, or "server" if the server is sending the message
#             string message - message to be sent
# Return Value: full_packet - length of packet in bytes and json word packet in bytes with nickname, message, and length of message
def make_word_packet(nickname, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_packet = json.dumps({"timestamp": timestamp, "nickname" : nickname, "message" : message})
    length = len(json_packet.encode()).to_bytes(2, 'big')
    full_packet = length + json_packet.encode()
    return full_packet
