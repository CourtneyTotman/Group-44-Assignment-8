import socket

def menu(): 
    print("\n---*---*---*---*---*---*---*---*---*---*---")
    print("\nPlease enter a number:")
    print("1. What is the average moisture inside my kitchen fridge in the past three hours?")
    print("2. What is the average water consumption per cycle in my smart dishwasher?")
    print("3. Which device consumed more electricity among my IoT devices (two refrigerators and a dishwasher)?")
    print("4. Exit")
    print("---*---*---*---*---*---*---*---*---*---*---")

def main():
    print("----------BEGINNING CLIENT----------\n")

    try:
        # User input server IP and Port
        print("INPUT SERVER INFORMATION")
        server_ip = str(input("Enter the server IP address: "))
        server_port = int(input("Enter the server port number: "))
        print()
        
        # Create client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect client to server
            client_socket.connect((server_ip, server_port))
            print("CONNECTION!")
            print(f"Connected to IP: {server_ip}")
            print(f"Connected to Port: {server_port} \n")
            
            # While user wants to query
            while True:
                # Display the menu directly
                menu()

                # Get user choice
                try:
                    user_choice = int(input("\nENTER A NUMBER: "))
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 5.")
                    continue

                # Menu choice: Exit
                if user_choice == 4: 
                    print("\nExiting...\n")
                    break

                # Incorrect menu choice (outside of 1 - 3 or 5)
                elif user_choice not in [1, 2, 3, 5]: 
                    print("Sorry, this query cannot be processed. Please select a query 1 - 3, 5, or 4 to exit.")

                # User chose a valid option
                else:
                    # Send user choice to the server
                    client_socket.send(bytearray(str(user_choice), encoding='utf-8'))
                    # Wait for server response
                    server_response = client_socket.recv(3015)
                    # Print server response
                    print(f"SERVER RESPONSE:\n\n{server_response.decode('utf-8')}")                

            # Close socket once user is done
            client_socket.close()
            print("\nCONNECTION CLOSED\n")
        
        # If client cannot connect to server, throw exception
        except (socket.gaierror, socket.error) as e:
            print(f"\nERROR: Server unable to connect. {e}\n")
    
    # If user inputs invalid port number, handle exception
    except ValueError:
        print("\nERROR: Invalid port number\nPlease enter a valid integer.\n")

    print("----------END OF CLIENT----------\n")

if __name__ == "__main__":
    main()
