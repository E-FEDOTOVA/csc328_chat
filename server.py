#!/usr/bin/env python3

import json
import sys
import socket
import random
import signal
import library
import os
import time

#Function name: really_read
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

#Function name: receive_chats
#Description: This function will receive all neccessay component of communication in this server
#              to messages between the client and server.
#Parameters: conn -- the client who will be sending chats to the server
#            nickname -- the unique nickname that each message will be corresponded to. 
#            all_nicks -- list of all nicknames that are connected to the server
#            all_socks -- list of all connections from clients 

def receive_chats(conn, nickname, all_nicks, all_socks):
        try:
            chat_message = library.read_message(conn)
            if chat_message:
                print(chat_message['nickname'] + ": " + chat_message['nickname'])

            if chat_message['message'] == "BYE":
                conn.close()
                all_nicks.remove(nickname)
                # child process stuff?
            else:
                #print(f"Received from {chat_message[nickname]}: {chat_message[message]}")
                j = 0
                for nick in all_nicks:
                    if nick != nickname and all_socks[j].fileno() != 0:
                        library.send_message(all_socks[j], nickname, chat_message) 
                        j += 1
                    else:
                        j += 1
        except (ConnectionResetError, json.JSONDecodeError) as e:
            print(f"Error receiving message: {e}")
#            break

def main():
    all_nicks = []
    all_socks = []
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
                    unique = 0
                    conn.sendall(len("NICK").to_bytes(2, 'big') + "NICK".encode())

                    while unique == 0:
                        word_length = int.from_bytes(really_read(conn, 2), 'big')
                        nickname = really_read(conn, word_length).decode()

                        if nickname in all_nicks:
                            conn.sendall(len("RETRY").to_bytes(2, 'big') + "RETRY".encode())

                        else:
                            conn.sendall(len("READY").to_bytes(2, 'big') + "READY".encode())
                            all_socks.append(conn)
                            all_nicks.append(nickname)
                            unique = 1

                    unique = 0
                    '''
                          for i in all_nicks:
                            if i != nickname:
                                unique += 1
                            if unique == len(all_nicks):
                                conn.sendall(len("READY").to_bytes(2, 'big') + "READY".encode())
                                break 
                            conn.sendall(len("RETRY").to_bytes(2, 'big') + "RETRY".encode())
                    '''

                    check = os.fork()
                    if check == 0:
                        receive_chats(conn, nickname, all_nicks, all_socks)

                        #os.wait()
                        #all_nicks.remove(nickname)
                        #all_socks.remove(conn)
                    #elif os.fork() > 0:
                        #receive_chats(conn, nickname, all_clients)
                        #all_clients.remove((nickname, conn))
 

 
    except OSError as e:
        exit(e)
    except KeyboardInterrupt:
        print("DONE")

if __name__ == "__main__":
    main()
