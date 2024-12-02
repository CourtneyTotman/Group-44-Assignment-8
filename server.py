import socket
import pymongo
from pymongo import MongoClient

CONNECTION_STRING = f"mongodb+srv://group44assignment8:group44assignment8@group44assignment8.ymcwi.mongodb.net/"
DATABASE_NAME = "test"
COLLECTION_NAME = "assignment8_virtual"

client = MongoClient(CONNECTION_STRING)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

#def retrieve_all_data():
#    results = collection.find({})
#    print("\nAll documents in the collection: ")
#    for doc in results:
#        print(doc)


def query_one():
    return "You selected 1"
#    query = {"length": "336"}
#    documents = collection.find(query)
#    print(documents)
#    return str(documents)

def query_two():
    return "You selected 2"

def query_three():
    return "You selected 3"

def main(): 
    print("----------BEGINNING SERVER----------\n")

    
    #server_socket information (ip and port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("SERVER INFORMATION")
    #User will enter IP address and port
    server_ip = str(input("Enter server IP Address: "))
    server_port = int(input("Enter port: "))
    #server_ip = "10.39.18.43"
    #server_port = 1024
    
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

        #while client sent choice
        while True: 

            #recieve query choice from client from server_port
            query_choice = client_Socket.recv(server_port)

            #if there is no query_choice, close connection, break
            if not query_choice: 
                print("CLOSING CONNECTION DUE TO CLIENT INACTIVITY\n")
                break

            #if there is a quer_choice, decode and print the choice number
            query_choice = int(query_choice.decode('utf-8'))
            print("User chose: ", query_choice, "\n")

            #get query depending on selection
            if query_choice == 1: 
                response = query_one()
                #response = retrieve_all_data()
            elif query_choice == 2:
                response = query_two()
            elif query_choice == 3:
                response = query_three()
            
            #send query result to client
            client_Socket.send(bytearray(str(response), encoding='utf-8'))
            
    #if try does not work, throw exception
    except Exception as e: 
        print(f"Error occurred: {e}\n")

    #in the end, close client socket connection
    finally: 
        client.close()
        client_Socket.close()
        print("CONNECTION CLOSED\n")

    #close server_socket
    server_socket.close()
    print("----------END OF SERVER----------\n")


if __name__ == "__main__": 
    main()

