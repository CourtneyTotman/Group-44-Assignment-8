# Group-44-Assignment-8
GROUP 44 : Courtney and Taiki's repo for Assignment 8 for CECS 327

## How to run program
### 1. Server
##### a) Download server file and locate it's location within the Virtual Machine.
##### b) In terminal, change the directory to the file's location.
##### c) Be sure to install pymongo for the server to work correctly.
##### d) Enter py server.py in the terminal.
##### e) Enter the internal IP address of the Virtual Machine the code is being ran on, then the port number you would like to work on (suggestion: 3000). (To find the internal ip address, type "ipconfig" on the command prompt. You will be usings the IPv4 Address. 

<img src = "https://github.com/CourtneyTotman/Group-44-Assignment-8/blob/1aac927f1c2d87772ca670a2fd37e2d6a70d6ca8/README%20extras/IPConfig.png" > 

##### f) After entering this information, the server will wait for the client's connection.

### 2. Client
##### a) Download client file and locate it's location.
##### b) In terminal, change the directory to the file's location.
##### c) Enter py client.py in the terminal.
##### d) Enter the external IP address of the server's Virtual Machine, then the port number the server is working on. (To find the external Ip address, it will be either at the top of the server's Virtual Machine, or within the Google Cloud)

<img src="https://github.com/CourtneyTotman/Group-44-Assignment-8/blob/1aac927f1c2d87772ca670a2fd37e2d6a70d6ca8/README%20extras/External%20IP.png">

##### e) After entering this information, the client should connect to server. If not, there is an error. 
##### f) Once connected, User is able to enter if they would like the menu displayed.
##### g) Then the user is asked to enter which query they would like to run.
##### f) The user will enter 4 if they would like to exit.

### 3. Exiting program
##### a) Once the user enters 4 on the client terminal, the client will stop the connection with the server on the client end.
##### b) The server will notice the inactivity of the client and stop the connection on the server end. 
##### c) Both server and client will terminate.

