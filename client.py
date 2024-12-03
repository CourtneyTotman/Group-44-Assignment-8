
import socket

def menu(): 
    print("Please enter a number 1--4")
    print("1. What is the average moisture inside my kitchen fridge in the past three hours?")
    print("2. What is the average water consumption per cycle in my smart dishwasher?")
    print("3. Which device consumed more electricity among my loT devices (two refrigerators and a dishwasher)?")
    print("4. Exit")
    print("5. Example query\n")


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
            
            #while user wants query
            while True:
                #user is asked to see menu
                user_repeat = input("Would you like to see the menu? (y or n)")
                while (user_repeat != 'y' and user_repeat != 'Y' and user_repeat != 'n' and user_repeat != 'N'):
                    #user must enter y or n
                    user_repeat = input("Please enter either y or n")
                if user_repeat == 'y' or user_repeat == 'Y':
                    menu()
                elif user_repeat == 'n' or user_repeat == 'N':
                    print()
                

                #get user choice
                user_choice = int(input("ENTER A NUMBER: "))

                #menu choice : exit
                if user_choice == 4: 
                    break

                #incorrect menu choice ( outside of 1 - 4 )
                elif user_choice != 1 and user_choice != 2 and user_choice != 3 and user_choice != 5: 
                    print("Sorry, this query cannot be processed. Please select a query 1 - 3 or 4 to exit.")

                #user chose a number between 1 - 3
                else:
                    #send server user choice
                    client_socket.send(bytearray(str(user_choice), encoding='utf-8'))
                    #wait for server response. then recieve from 3015
                    server_response = client_socket.recv(3015)
                    #print server response
                    print(f"SERVER RESPONSE: {server_response.decode('utf-8')}")                
                

            #close socket once user is done
            client_socket.close()
            print("\nCONNECTION CLOSED\n")
        
        #if client cannot connect to server, throw exception
        except (socket.gaierror, socket.error) as e:
            print(f"\nERROR: Server unable to connect. {e}\n")
    
    #if user inputs invalid port number, have user try again
    except ValueError:
        print("\nERROR: Invalid port number\nPlease enter a valid integer.\n")

    print("----------END OF CLIENT----------\n")

if __name__ == "__main__":
    main()