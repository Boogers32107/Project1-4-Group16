import json
from pathlib import Path #Imports

folder = Path(__file__).resolve().parent

def load_leaderboard(): #Tells it to check for file first
    try:
        with open(Path(folder, "data.json"), "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []  # If file doesn't exist or is empty, start with an empty list

    if not isinstance(data, list):
        data = [data]

    return data

def save_leaderboard(data): #Tells it to save the updated file
    with open(Path(folder, "data.json"), "w") as file:
        json.dump(data, file, indent=4)

def update_score(user, score): #Will create User if the User was not found
    data = load_leaderboard()
    found = False
    for entry in data:
        if entry.get("name") == user:
            entry["score"] = int(entry["score"]) + score
            found = True
            break

    if not found:
        data.append({"name": user, "score": score})

    save_leaderboard(data)

def get_leaderboard(): 
    data = load_leaderboard()
    sorted_data = sorted(data, key=lambda x: x["score"], reverse=True)
    return sorted_data