#!/usr/bin/env python3

import sys
import socket
import random
import signal
import library

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


def main():
    all_clients = []
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
                    # conn.sendall(len("Enter a nickname").to_bytes(2, 'big') + x.encode())
                    # word_length = int.from_bytes(really_read(s, 2), 'big')
                    #   if word_length == 0: break
                    #nickname = really_read(s, word_length)                    
                    # for i in all_clients:
                    #   if i != nickname:

                    unique = 0                
                    while True:                        
                        conn.sendall(len("NICK").to_bytes(2, 'big') + "NICK".encode())
                        word_length = int.from_bytes(really_read(conn, 2), 'big')
                        nickname = really_read(conn, word_length).decode()
                        for i in all_clients:
                            if i != nickname: 
                                unique += 1                                     
                        if unique == len(all_clients):
                            conn.sendall(len("READY").to_bytes(2, 'big') + "READY".encode())
                            break 
                        conn.sendall(len("RETRY").to_bytes(2, 'big') + "RETRY".encode())

                    all_clients.append(nickname)
              

                    

 
    except OSError as e:
        exit(e)
    except KeyboardInterrupt:
        print("DONE")

if __name__ == "__main__":
    main()
