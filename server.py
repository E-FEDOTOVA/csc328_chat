#!/usr/bin/env python3

import sys
import socket
import random
import signal
import library
import os
import time

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
    while True:
        data = conn.recv(2)
        if data:
            for i in all_clients:
                if i != nickname:
                    print('good')          

def receive_chats(conn, nickname, all_nicks, all_socks):
    while True:
        chat_message = library.read_message(conn)
        if chat_message:
            j=0
            for i in all_nicks:
                if i != nickname:
                    library.send_message(all_socks[j], nickname, chat_message) 
                    j+=1
                else:     
                    j+=1
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
                    #Send hello to connecting client
                    conn.sendall(len("HELLO").to_bytes(2, 'big') + "HELLO".encode()) 

                    unique = 0                
                    conn.sendall(len("NICK").to_bytes(2, 'big') + "NICK".encode())
                    while True:                        
                        word_length = int.from_bytes(really_read(conn, 2), 'big')
                        nickname = really_read(conn, word_length).decode()
                        for i in all_nicks:
                            if i != nickname: 
                                unique += 1                                     
                        if unique == len(all_nicks):
                            conn.sendall(len("READY").to_bytes(2, 'big') + "READY".encode())
                            break 
                        conn.sendall(len("RETRY").to_bytes(2, 'big') + "RETRY".encode())
                    unique = 0
                    all_socks.append(conn)
                    all_nicks.append(nickname)
               
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
