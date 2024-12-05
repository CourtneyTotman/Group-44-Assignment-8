#from doctest import Example
import socket
import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone

#Connecting to MongoDB Atlas
CONNECTION_STRING = f"mongodb+srv://group44assignment8:group44assignment8@group44assignment8.ymcwi.mongodb.net/"
DATABASE_NAME = "test"
COLLECTION_VIRTUAL= "assignment8_virtual"
COLLECTION_METADATA = "assignment8_metadata"

#Connecting to database
client = MongoClient(CONNECTION_STRING)
db = client[DATABASE_NAME]
virtual_collection = db[COLLECTION_VIRTUAL]
metadata_collection = db[COLLECTION_METADATA]

#Node for Binary Search Tree
class Node: 
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

class BinarySearchTree:
    def __init__(self):
        self.root = None 

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value: 
            if node.left is None: 
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else: 
            if node.right is None: 
                node.right = Node(value)
            else: 
                self._insert_recursive(node.right, value)

    def in_order_traversal(self, node, result):
        if node: 
            self.in_order_traversal(node.left, result)
            result.append(node.value)
            self.in_order_traversal(node.right, result)

    def get_sorted_values(self):
        result = []
        self.in_order_traversal(self.root, result)
        return result


#Find the average moisture inside the kitchen fridge in the past three hours
def query_one():
     #find the dataset of the smart fridge's metadata
    fridge_metadata = metadata_collection.find_one({"customAttributes.name": "Smart Refrigerator"})

    #find the assetUid of the fridge
    if fridge_metadata:
        fridge_asset_uid = fridge_metadata["assetUid"]
    else: 
        raise Exception("Fridge asset not found in metadata")

    #what is the time 3 hours ago
    current_utc_time = datetime.now(timezone.utc)
    three_hours_ago = current_utc_time - timedelta(hours=3)
    
    #find the datasets that match fridge's asset Uid in the past 3 hours
    query = {
        "topic": "assignment8",
        "payload.parent_asset_uid": fridge_asset_uid, 
        "time":  {"$gte": three_hours_ago}
        }

    #collect all the datasets that match the query
    documents = virtual_collection.find(query)

    query_one_bst = BinarySearchTree()

    #in each dataset, collect the moisture meter reading and place into binary search tree
    for document in documents:
        moisture_value = document['payload'].get('Moisture Meter - Moisture meter')
        print(document.get('time'))

        if moisture_value is not None: 
            moisture_value = float(moisture_value)
            query_one_bst.insert(moisture_value)

    moisture_values = query_one_bst.get_sorted_values()

    #using the binary search tree of all readings, find the average (sum of all readings / length of binary search tree)
    if moisture_values: 
        average_moisture = sum(moisture_values) / len(moisture_values)
        #final_value = (average_moisture / )
        #return string + average value to client
        return f"The average moisture inside the kitchen fridge in the past three hours is: {average_moisture} RH%"
    else: 
        return "No moisture readings were found in the past 3 hours."


def query_two():
    """
    Find the average water consumption per cycle in my smart dishwasher
    """
    try:
        #find the dataset from metadata that matches smart dishwasher
        dishwasher = metadata_collection.find_one({"customAttributes.name": "Smart Dishwasher"})

        if not dishwasher:
            return "Error: Smart Dishwasher not found in metadata database."

        #find the asset Uid of the dishwasher
        parent_asset_uid = dishwasher['assetUid']

        #find all datasets in virtual that match the asset Uid of dishwasher
        data = virtual_collection.find({"payload.parent_asset_uid": parent_asset_uid})

        query_two_bst = BinarySearchTree()

        for entry in data: 
            if "payload" in entry and "Water Consumption Sensor" in entry["payload"]:
                try:
                    water_reading = float(entry["payload"]["Water Consumption Sensor"])
                    query_two_bst.insert(water_reading)
                except ValueError: 
                    continue

        sorted_readings = query_two_bst.get_sorted_values()

        if not sorted_readings: 
            return "No water consumption data found."


        avg_consumption = sum(sorted_readings) / len(sorted_readings)

        converstion_to_gallons = avg_consumption * 0.264172

        return f"Average Water Consumption per Cycle: {converstion_to_gallons:.2f} Gallons."

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

        #average voltage of a refrigerator and dishwasher
        voltage = 120

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

                #converting to kwh and finding consumption total
                if parent_uid and current:
                    power_watts = current * voltage
                    energy_kwh = (power_watts * 1) / 1000
                    consumption_totals[parent_uid] = consumption_totals.get(parent_uid, 0) + energy_kwh

        if not consumption_totals:
            return "No electricity consumption data available."

        # Find device with the highest consumption
        max_device = max(consumption_totals, key=consumption_totals.get)
        max_consumption = consumption_totals[max_device]

        # Prepare result with device names
        result = "Electricity consumption by device (in kWh):\n"
        result += "\n".join(
            f"{asset_name_map.get(uid, uid)}: {total:.2f} kWh"
            for uid, total in consumption_totals.items()
        )
        result += f"\n\nDevice with the highest consumption: {asset_name_map.get(max_device, max_device)} ({max_consumption:.2f} kWh)"
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

    print("\nLISTENING FOR A CONNECTION\n")
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
            else:
                response = "Invalid query choice."

            client_Socket.send(response.encode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_Socket.close()
        server_socket.close()
        print("Connection closed.\n")
        print("----------END OF SERVER----------\n")

if __name__ == "__main__": 
    main()
