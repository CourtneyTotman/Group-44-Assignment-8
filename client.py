
import socket

def main():
    print("----------BEGINNING CLIENT----------\n")

    try:
        #User input server IP and Port
        print("INPUT SERVER INFORMATION")
        server_ip = str(input("Enter the server IP address: "))
        server_port = int(input("Enter the server port number: "))
        print()
        
        #create client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #try program
        try:
            #connect to client to server
            client_socket.connect((server_ip, server_port))
            print("CONNECTION!")
            print(f"Connected to ip: {server_ip}")
            print(f"Connected to port: {server_port} \n")
            
            while True:
                #user inputs message to send to server
                message = input("ENTER A MESSAGE TO SEND TO THE SERVER (type 'exit' to quit):")
                print()

                #if user inputs 'exit' program will close
                if message.lower() == 'exit':
                    print("YOU ENTERED EXIT\nCLOSING CONNECTION\n")
                    break
                
                #client socket sends message
                client_socket.send(bytearray(str(message), encoding='utf-8'))
                
                #server responds with capitalized message
                new_message = client_socket.recv(3015)
                print(f"SERVER HAS RESPONDED!\nServer response: {new_message.decode('utf-8')}\n")

            #close socket once user is done
            client_socket.close()
            print("CONNECTION CLOSED\n")
        
        #if client cannot connect to server, throw exception
        except (socket.gaierror, socket.error) as e:
            print(f"ERROR: Server unable to connect. {e}\n")
    
    #if user inputs invalid port number, have user try again
    except ValueError:
        print("ERROR: Invalid port number\nPlease enter a valid integer.\n")

    print("----------END OF CLIENT----------\n")

if __name__ == "__main__":
    main()