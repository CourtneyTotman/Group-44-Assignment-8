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
    Retrieves water consumption data for a smart dishwasher and calculates the average.
    """
    try:
        dishwasher = metadata_collection.find_one({"customAttributes.name": "Smart Dishwasher"})
        if not dishwasher:
            return "Error: Smart Dishwasher not found in metadata database."

        parent_asset_uid = dishwasher['assetUid']
        data = virtual_collection.find({"payload.parent_asset_uid": parent_asset_uid})

        water_readings = [
            float(entry["payload"]["Water Consumption Sensor"])
            for entry in data if "payload" in entry and "Water Consumption Sensor" in entry["payload"]
        ]

        if not water_readings:
            return "No water consumption data found."

        avg_consumption = sum(water_readings) / len(water_readings)
        return f"Average Water Consumption per Cycle: {avg_consumption:.2f} Liters"

    except Exception as e:
        return f"Error in query_two: {e}"

def query_three():
    """
    Analyzes electricity consumption by devices and identifies the device with the highest usage.
    """
    try:
        # Fetch all metadata to map assetUid to their names
        metadata = metadata_collection.find()
        asset_name_map = {entry["assetUid"]: entry["customAttributes"]["name"] for entry in metadata}

        # Fetch virtual collection data
        data = virtual_collection.find()

        # Calculate consumption totals
        consumption_totals = {}
        for entry in data:
            if "payload" in entry:
                payload = entry["payload"]
                parent_uid = payload.get("parent_asset_uid")
                current = (
                    float(payload.get("Ammeter", 0)) or
                    float(payload.get("Ammeter 2", 0)) or
                    float(payload.get("Ammeter (dishwasher)", 0))
                )

                if parent_uid and current:
                    consumption_totals[parent_uid] = consumption_totals.get(parent_uid, 0) + current

        if not consumption_totals:
            return "No electricity consumption data available."

        # Find device with the highest consumption
        max_device = max(consumption_totals, key=consumption_totals.get)
        max_consumption = consumption_totals[max_device]

        # Prepare result with device names
        result = "Electricity consumption by device (in Amperes):\n"
        result += "\n".join(
            f"{asset_name_map.get(uid, uid)}: {total:.2f} Amperes"
            for uid, total in consumption_totals.items()
        )
        result += f"\n\nDevice with the highest consumption: {asset_name_map.get(max_device, max_device)} ({max_consumption:.2f} Amperes)"
        return result

    except Exception as e:
        return f"Error in query_three: {e}"

def main():
    print("----------BEGINNING SERVER----------\n")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("SERVER INFORMATION")
    server_ip = str(input("Enter server IP Address: "))
    server_port = int(input("Enter port: "))
    server_socket.bind((server_ip, server_port))
    server_socket.listen()

    print("LISTENING FOR A CONNECTION\n")
    client_Socket, client_Address = server_socket.accept()
    print(f"Connected to IP: {client_Address}\n")

    try:
        while True:
            query_choice = client_Socket.recv(1024)
            if not query_choice:
                print("Client disconnected.")
                break

            query_choice = int(query_choice.decode('utf-8'))
            print(f"User chose: {query_choice}\n")

            if query_choice == 1:
                response = query_one()
            elif query_choice == 2:
                response = query_two()
            elif query_choice == 3:
                response = query_three()
            elif query_choice == 5:
                response = example_query()
            else:
                response = "Invalid query choice."

            client_Socket.send(response.encode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_Socket.close()
        server_socket.close()
        print("Connection closed.\n")

if __name__ == "__main__": 
    main()
