from datetime import datetime, timedelta
from mcstatus import JavaServer
import json
import time
import os
import subprocess

server = "mc.danmyers.net:25565"
file = "/home/admin/mc_server_tools/status.json"
stop_server_url = "https://z180pb1pd3.execute-api.us-east-1.amazonaws.com/Prod/mc_start_stop"

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

def CalculateDuration(data):
    if len(data) < 2:
        return timedelta(seconds=0)
    
    last_player_count = data[-1][1]
    same_count_duration = timedelta(seconds=0)
    previous_record_time = datetime.strptime(data[-1][0], "%Y-%m-%d %H:%M:%S")

    for record in reversed(data[:-1]):
        record_time = datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S")
        if record[1] == last_player_count:
            same_count_duration += (previous_record_time - record_time)
            previous_record_time = record_time
        else:
            break
    
    return same_count_duration

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

    same_count_duration = CalculateDuration(existing_data)
    
    if player_count == 0 and same_count_duration >= timedelta(minutes=15):
        # Clear the status.json file
        with open(file, "w") as json_file:
            json_file.write("[]")

        # Send the shutdown signal
        subprocess.run(["curl", "-X", "POST", "-H", "Content-Type: application/json", "-d", '{"action": "stop"}', stop_server_url])
        print("Server stopped due to 0 players for 30 minutes.")
    else:
        print(f"Duration with the same player count: {same_count_duration}")
