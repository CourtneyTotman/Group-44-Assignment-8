from doctest import Example
import socket
import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta

CONNECTION_STRING = f"mongodb+srv://group44assignment8:group44assignment8@group44assignment8.ymcwi.mongodb.net/"
DATABASE_NAME = "test"
COLLECTION_VIRTUAL= "assignment8_virtual"
COLLECTION_METADATA = "assignment8_metadata"

client = MongoClient(CONNECTION_STRING)
db = client[DATABASE_NAME]
virtual_collection = db[COLLECTION_VIRTUAL]
metadata_collection = db[COLLECTION_METADATA]

class Node: 
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key 

class BinarySearchTree:
    def __init__(self):
        self.root = None 

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key < node.val: 
            if node.left is None: 
                node.left = Node(key)
            else:
                self._insert_recursive(node.left, key)
        else: 
            if node.right is None: 
                node.right = Node(key)
            else: 
                self._insert_recursive(node.right, key)

    def in_order_traversal(self, node):
        result = []
        if node: 
            result.extend(self.in_order_traversal(node.left))
            result.append(node.val)
            result.extend(self.in_order_traversal(node.right))
        return result

def example_query():
    query = {"topic": "assignment8"}
    documents = virtual_collection.find(query)
    bst = BinarySearchTree()
    for document in documents:
    # Extract the desired value (e.g., "Ammeter 2" from the payload)
        ammeter_value = document['payload'].get('Ammeter 2')  # Change to another field if needed
    
        if ammeter_value is not None:
        # Insert the extracted value into the BST
            bst.insert(ammeter_value)

    # Perform an inorder traversal to get the values in sorted order
    sorted_values = bst.inorder()

    # Print the sorted values
    return("Sorted Ammeter 2 Values from 'assignment8' topic:", sorted_values)

def query_one():
    fridge_metadata = metadata_collection.find_one({"customAttributes.name": "Second Smart Refrigerator"})

    if fridge_metadata:
        fridge_asset_uid = fridge_metadata["assetUid"]
    else: 
        raise Exception("Fridge asset not found in metadata")

    three_hours_ago = datetime.now() - timedelta(hours = 3)

    query = {
        "topic": "assignment8",
        "payload.parent_asset_uid": fridge_asset_uid, 
        "time":  {"$gte": three_hours_ago}
        }

    documents = virtual_collection.find(query)

    query_one_bst = BinarySearchTree()

    for document in documents:
        moisture_value = document['payload'].get('Moisture meter 2')

        if moisture_value is not None: 
            moisture_value = float(moisture_value)
            query_one_bst.insert(moisture_value)

    moisture_values = query_one_bst.in_order_traversal(query_one_bst.root)

    if moisture_values: 
        average_moisture = sum(moisture_values) / len(moisture_values)
        return f"The average moisture inside the kitchen fridge in the past three hours is: {average_moisture} %"

    else: 
        return "No moisture readings were found in the past 3 hours."

def query_two():
    """
    Retrieves data for the past 24 hours and computes the maximum temperature reading
    from a specific asset in the 'assignment8' topic.
    """
    asset_metadata = metadata_collection.find_one({"customAttributes.name": "Temperature Sensor"})

    if asset_metadata:
        asset_uid = asset_metadata["assetUid"]
    else:
        raise Exception("Temperature Sensor asset not found in metadata")

    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)

    query = {
        "topic": "assignment8",
        "payload.parent_asset_uid": asset_uid,
        "time": {"$gte": twenty_four_hours_ago}
    }

    documents = virtual_collection.find(query)

    max_temperature = None
    for document in documents:
        temperature_value = document['payload'].get('Temperature Sensor')

        if temperature_value is not None:
            temperature_value = float(temperature_value)
            if max_temperature is None or temperature_value > max_temperature:
                max_temperature = temperature_value

    if max_temperature is not None:
        return f"The maximum temperature reading in the past 24 hours is: {max_temperature}°C"
    else:
        return "No temperature readings were found in the past 24 hours."


def query_three():
    """
    Fetches data for the past 7 days to compute the total energy consumption from
    a specific asset in the 'assignment8' topic.
    """
    asset_metadata = metadata_collection.find_one({"customAttributes.name": "Energy Meter"})

    if asset_metadata:
        asset_uid = asset_metadata["assetUid"]
    else:
        raise Exception("Energy Meter asset not found in metadata")

    seven_days_ago = datetime.now() - timedelta(days=7)

    query = {
        "topic": "assignment8",
        "payload.parent_asset_uid": asset_uid,
        "time": {"$gte": seven_days_ago}
    }

    documents = virtual_collection.find(query)

    total_energy_consumption = 0
    for document in documents:
        energy_value = document['payload'].get('Energy Consumption')

        if energy_value is not None:
            total_energy_consumption += float(energy_value)

    if total_energy_consumption > 0:
        return f"The total energy consumption in the past 7 days is: {total_energy_consumption} kWh"
    else:
        return "No energy consumption data was found in the past 7 days."

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
            elif query_choice == 5: 
                response = example_query()
            
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

