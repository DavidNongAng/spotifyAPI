from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv('CLIENT_SECRET')

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["artists"]['items']
    if len(json_result) == 0:
        print("no artist with this name...")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=CA"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def search_artist():
    artist_name = search_entry.get()
    result = search_for_artist(token, artist_name)
    if result:
        artist_name_label.config(text=result["name"])
        artist_id = result["id"]
        songs = get_songs_by_artist(token, artist_id)
        song_listbox.delete(0,tk.END)
        for idx, song in enumerate(songs):
            song_listbox.insert(tk.END, f"{idx+1}. {song['name']}")
    else:
        artist_name_label.config(text = "No artist Found")
                     
token = get_token()

root = tk.Tk()
root.title("Spotify Artist Search")

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_entry = ttk.Entry(search_frame, width=40)
search_entry.grid(row=0, column=0, padx=5)

search_button = ttk.Button(search_frame, text="Search", command=search_artist)
search_button.grid(row=0, column=1, padx=5)

artist_name_label = ttk.Label(root, text="")
artist_name_label.pack(pady=10)

song_listbox = tk.Listbox(root, width=50)
song_listbox.pack(pady=10)

root.mainloop()
    
    