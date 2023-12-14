#!/usr/bin/env python3

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

def really_read(s, n):
    bytes = b''
    while len(bytes) != n:
        curr_read = s.recv(n - len(bytes))
        bytes += curr_read
        if len(curr_read) == 0: break
    return bytes

#createWordPacket(word_list):
    '''
    Function name: createWordPacket
    Description: This function will receive a list of words and decide a random
                    word from the list and create a word packet 
    Parameters: string word_list -- a list of random words
    Return: A word packet that uses a random word from the given list
    '''

#   rand_index = random.randint(0, (len(word_list)-1))
#   word_pack = word_list[rand_index].encode()
#   length = len(word_pack).to_bytes(2, byteorder='big')
#   return(length+word_pack)

def send_chats(conn, nickname, all_clients):
        data = conn.recv(2)
        if data:
            for i in all_clients:
                if i != nickname:
                    print('good')

def receive_chats(conn, nickname, all_nicks, all_socks):
    try:
        while True:
            chat_message = library.read_message(conn)
            if chat_message:
                print(f"Received from {chat_message['nickname']}: {chat_message['message']}")
                #print(conn.fileno())
            if chat_message['message'] == "BYE":
                conn.close()
                all_nicks.remove(nickname)
                all_socks.remove(conn)
                break
            else:
                for sock in all_socks:
                    if sock != conn and sock.fileno() != -1:
                        library.send_message(sock, nickname, chat_message)
    except (ConnectionResetError, json.JSONDecodeError) as e:
        print(f"Error receiving message: {e}")
        conn.close()
        all_nicks.remove(nickname)
        all_socks.remove(conn)

def main():
    if len(sys.argv) != 2:
        exit("Usage: server <port>")
    try:
        with socket.socket() as s:
            s.bind(('', int(sys.argv[1])))
            s.listen(1)
            #print(s.fileno())
            while True:
                conn, _ = s.accept()
                #print(conn.fileno())
                with conn:
                    conn.sendall(len("HELLO").to_bytes(2, 'big') + "HELLO".encode()) 
                    conn.sendall(len("NICK").to_bytes(2, 'big') + "NICK".encode())
                    
                    while True:
                        word_length = int.from_bytes(really_read(conn, 2), 'big')
                        nickname = really_read(conn, word_length).decode()

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
                        library.send_message(conn, "another_person", "hello!")
                        receive_chats(conn, nickname, all_nicks, all_socks)
                        exit()  # exit child process 

    except OSError as e:
        exit(e)
    except KeyboardInterrupt:
        print("DONE")

if __name__ == "__main__":
    main()
