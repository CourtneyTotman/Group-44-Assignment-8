import socket

def main(): 
    print("----------BEGINNING SERVER----------\n")

    
    #server_socket information (ip and port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("SERVER INFORMATION")
    #User will enter IP address and port
    server_ip = str(input("Enter server IP Address: "))
    server_port = int(input("Enter port: "))
    print()

    #bind server socket ip and port
    server_socket.bind((server_ip, server_port))

    #server begins to listen for client connection
    print("LISTENING FOR A CONNECTION\n")
    server_socket.listen()

    #once found that connection, save client socket and client address and accept
    client_Socket, client_Address = server_socket.accept()
    print("CONNECTION!")
    print(f"Connected to ip and address {client_Address} \n")


    #try program
    try: 

        while True: 
            #recieve message from client on 1024
            message = client_Socket.recv(server_port)

            #if there is no message then close connection
            if not message: 
                print("CLOSING CONNECTION DUE TO NO MORE DATA FROM CLIENT\n")
                break

            #decode message
            message = message.decode('utf-8')
            print(f"Received from client: {message}")

            #new message turns message to all capitals 
            new_message = message.upper()

            #send new message to client
            client_Socket.send(bytearray(str(new_message), encoding='utf-8'))
            print(f"Sent back to client: {new_message} \n")
            
    #if try does not work, throw exception
    except Exception as e: 
        print(f"Error occurred: {e}\n")

    #in the end, close client socket connection
    finally: 
        client_Socket.close()
        print("CONNECTION CLOSED\n")

    #close server_socket
    server_socket.close()
    print("----------END OF SERVER----------\n")

if __name__ == "__main__": 
    main()

