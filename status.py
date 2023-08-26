from mcstatus import JavaServer
import json
import time
import os

server = "mc.danmyers.net:25565"

def CheckStatus(server):
    server = JavaServer.lookup(server)
    status = server.status()
    return status.players.online

if __name__ == "__main__":
    player_count = CheckStatus(server)
    
    # Create a dictionary for the new data
    new_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "player_count": player_count
    }
    
    json_file_path = "server_status.json"
    
    # Load existing JSON data if the file exists
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    
    # Append the new data to the existing data
    existing_data.append(new_data)
    
    # Write the updated data to the JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)
