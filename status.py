from mcstatus import JavaServer
import json
import time
import os

server = "mc.danmyers.net:25565"
file = "status.json"


def CheckStatus(server):
    server = JavaServer.lookup(server)
    status = server.status()
    return status.players.online

def OpenFile(file):
    if os.path.exists(file):
        with open(file, "r") as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    return existing_data  

if __name__ == "__main__":
    player_count = CheckStatus(server)
    
    new_record = [
        time.strftime("%Y-%m-%d %H:%M:%S"),
        player_count
    ]
    existing_data = OpenFile(file)
    existing_data.append(new_record)
    
    # Write the updated data to the JSON file
    with open(file, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)
