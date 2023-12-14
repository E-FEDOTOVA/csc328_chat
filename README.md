# Chat Server - CSC328
# Team members:

 - Zachary Andruchowitz - server 
 - Lauren Engel - library 
 - Kate Fedotova -  client

# BUILD CLIENT & SERVER

### BUILD SERVER

    python3 server.py <port number>
    
### BUILD CLIENT

    python3 client.py <host> <port number>

# MANIFEST
Server: server.py
Client: client.py
Library Functions: library.py


# RESPONSIBILITY MATRIX 
| **Group Member** | Server | Client | Library | README |
|------------------|--------|--------|---------|--------|
| Zachary          | R       |        |   C       |   P (Application Protocol)     |
| Lauren           |     C    |     C    |     R    |        |
| Kate             |        |    R    |         |    R    |

> R - Primary responsible
> C - Consulted

# Tasks & Times
### Server
1.  **Initialize and Listen to socket**
    
    -   Setting up the server socket to listen for incoming connections.
    -   Time Taken: 
2.  **Handling Connection Requests**
    
    -   Managing incoming connection requests from clients and sending initial messages.
    -   Time Taken: 
3.  **Nickname Validation**
    
    -   Validate unique nicknames for clients.
    -   Time Taken: 
4.  **Sending and Receiving Messages**
    
    -   Send and receive messages to clients.
    -   Time Taken: 
5.  **Forking Child Processes**
    
    -   Implementing child processes to manage message reception for multiple clients simultaneously.
    -   Time Taken:
### Notes on server:
more here

### Library
1.  **send_message Function**
    
    -   Create a function to enable a socket to send a word packet containing a message.
    -   Time Taken: 
2.  **really_read Function**
    
    -   Function to read all bytes of a word packet.
    -   Time Taken: 
3.  **read_message Function**

    -   Function to allow a socket to read a word packet containing a message.
    -   Time Taken: 
5.  **make_word_packet Function**
    
    -   Function to create a word packet in a JSON format.
    -   Time Taken: 

### Notes on library:
more here

### Client
1.  **Connecting to a Server**
    
    -   Function to establish a TCP socket connection with the server.
    -   Time Taken: 10 minutes
2.  **Sending a Nickname**
    
    -   Function to send a chosen nickname through the socket.
    -   Time Taken: 60 minutes
3.  **Receiving Messages**
    
    -   Functionality to receive messages from the connected socket.
    -   Time Taken: - 
4.  **Reading Incoming Messages Process**
    
    -   Child process to read incoming messages.
    -   Time Taken: 
5.  **Sending Messages Process**
    
    -   Parent process to send messages through the socket.
    -   Time Taken: 30 minutes

### Notes on Client
  more here

# APPLICATION PROTOCOL 


# ASSUMPTIONS 
– clearly list and describe any assumptions made about running the application or how the application works

# Discussion on your development process
 including any decisions and/or major problems you encountered and your solution for each

# STATUS 
– current status of applications in terms of specifications, and any known issues with the application
