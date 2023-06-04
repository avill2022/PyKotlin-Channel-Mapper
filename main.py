import tkinter
from tkinter import *
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

import os
import json

import pyperclip
#pip install pyperclip

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

selected_tab=0

api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=os.getenv("YOUTUBE_API_KEY"))



class ChannelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Channel):
            return {
                "channel_id": obj.channel_id,
                "channel_name": obj.channel_name,
                "channel_description": obj.channel_description,
                "channel_thumb": obj.channel_thumb,
                "channel_videos": obj.channel_videos
            }
        elif isinstance(obj, Video):
            return {
                "video_id": obj.video_id,
                "video_name": obj.video_name,
                "video_description": obj.video_description,
                "video_thumb": obj.video_thumb,
                "current": obj.current,
                "duration": obj.duration,
                "views": obj.views
            }
        return super().default(obj)

class Video:
    def __init__(self, video_id, video_name, video_description, video_thumb,current,duration,views):
        self.video_id = video_id
        self.video_name = video_name
        self.video_description = video_description
        self.video_thumb = video_thumb
        self.current = current
        self.duration = duration
        self.views = views

class Channel:
    def __init__(self, channel_id, channel_name, channel_description, channel_thumb, channel_videos):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_description = channel_description
        self.channel_thumb = channel_thumb
        self.channel_videos = channel_videos

def tab_changed(event):
    global selected_tab
    selected_tab = event.widget.index("current")
    #print("Selected Tab:", selected_tab)

# Function to copy text to clipboard
def copy_to_clipboard():
    global selected_tab
    text=""
    if(selected_tab ==0):
        text = text_box_classes.get("1.0", END).strip()
    if(selected_tab ==1):
        text = text_box_json.get("1.0", END).strip()
    pyperclip.copy(text)

def parse_json(channel):

    json_string = json.dumps(channel, cls=ChannelEncoder)
    text_box_json.insert("0.0", json_string.strip())

    file_path = channel.channel_id+".json"

    with open(file_path, "w") as file:
        file.write(json_string)

def get_channel_info(channel_id):
    try:
        # Get the channel details
        channels_request = youtube.channels().list(
            part="snippet",
            id=channel_id
        )
        channels_response = channels_request.execute()
        channel_name = channels_response["items"][0]["snippet"]["title"]
        channel_thumbnail = channels_response["items"][0]["snippet"]["thumbnails"]["medium"]["url"]
        channel_description = channels_response["items"][0]["snippet"]["description"]

        return channel_name, channel_thumbnail, channel_description

    except HttpError as e:
        print("An error occurred while retrieving channel info:", e)
        return None, None, None

def get_playlist_videos(play_list):
    try:
        # Retrieve the videos from the uploads playlist
        playlist_items  = []
        next_page_token = None
        while True:
            playlist_items_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=play_list,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            playlist_items.extend(playlist_items_response['items'])

            next_page_token = playlist_items_response.get('nextPageToken')
            if not next_page_token:
                break
        return playlist_items
    except HttpError as e:
        print("An error occurred while retrieving playlist videos:", e)
        return []

def set_videos_to_controls(playlist_items,channel_name,channel_id,channel_description,channel_thumb):
    # Process the retrieved videos
    videos_string="Channel(\""+channel_id+"\",\""+channel_name+"\",\"\",\""+channel_thumb+"\",ArrayList(listOf("
    videos_ = []  # Existing list

    for video in playlist_items:
        video_id = video['snippet']['resourceId']['videoId']
        video_name = video['snippet']['title']
        video_description = "" #video['snippet']['description']
        video_thumbnail = video['snippet']['thumbnails']['default']['url']
        videos_string+="Video(\""+video_id+"\",\""+video_name+"\",\""+video_description+"\",\""+video_thumbnail+"\",0.0,0.0,0),\n"
        video = Video(video_id,video_name, video_description, video_thumbnail,0.0,0.0,0)
        videos_.append(video) 

    videos_string+="))"

    text_box_classes.insert("0.0", videos_string.strip()) 

    # Create Channel instance with the videos
    channel = Channel(channel_name,channel_id, channel_description, channel_thumb,videos_)

    parse_json(channel)

def get_videos_from_channel(channel_id):
    # Retrieve channel information
    channel_name, channel_thumb, channel_description = get_channel_info(channel_id)

    # Retrieve the uploads playlist ID for the channel
    channels_response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()
    play_list = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    playlist_items = get_playlist_videos(play_list)

    set_videos_to_controls(playlist_items,channel_name,channel_id,channel_description,channel_thumb)

def get_videos_from_play_list(channel_id,play_list):
    # Retrieve channel information
    channel_name, channel_thumb, channel_description = get_channel_info(channel_id)
    playlist_items = get_playlist_videos(play_list)
    set_videos_to_controls(playlist_items,channel_name,channel_id,channel_description,channel_thumb)


def get_channel_videos_from_chanenl(json_string):
    # Parse the JSON string
    data = json.loads(json_string)

def start_function():
    text_box_classes.delete("1.0", END)
    text_box_json.delete("1.0", END)

    text_channel = IDChannelEntry.get()  # Retrieve the text from the Entry widget
    if len(text_channel) == 0:
        messagebox.showinfo("Error", "Add the ID channel into the entry box!")
    else:
        text_play_list = IDPlayListEntry.get()  # Retrieve the text from the Entry widget
        if len(text_play_list) == 0:
            get_videos_from_channel(text_channel)
        else:
            get_videos_from_play_list(text_channel,text_play_list)

root = ctk.CTk()
root.geometry("800x500")
root.title("Chatbot")
ctk.set_appearance_mode("dark")

slideBar = ctk.CTkFrame(root)
slideBar.pack(side="left", padx=10, pady=10)

#open Project
openProject = ctk.CTkFrame(slideBar)
openProject.grid(row=0,column=0,pady=5, padx=5, sticky='NSWE')

IDPlayListEntry = ctk.CTkEntry(master=openProject, placeholder_text="ID PLAYLIST",width=290)
IDPlayListEntry.grid(row=1,column=0,pady=5, padx=5, sticky='NSWE')
IDPlayListEntry.insert(0, "")

IDChannelEntry = ctk.CTkEntry(master=openProject, placeholder_text="ID CHANNEL",width=290)
IDChannelEntry.grid(row=2,column=0,pady=5, padx=5, sticky='NSWE')
IDChannelEntry.insert(0, "")

copy_content = ctk.CTkButton(master=slideBar, text="Copy Classes!",command=copy_to_clipboard, fg_color=("#DB3E39", "#821D1A"))
copy_content.grid(row=3,column=0,pady=5, padx=5, sticky='NSWE')


# Tab Layout
my_notebook = ttk.Notebook(root)
my_notebook.pack(expand=tkinter.YES,side="left" ,fill=tkinter.BOTH)
# Bind the callback function to the NotebookTabChanged event
my_notebook.bind("<<NotebookTabChanged>>", tab_changed)

# Tab Layout Classes
my_frame1 = Frame(my_notebook,width=500,heigh=500,bg="grey")
my_frame1.pack(fill="both",expand=1)
my_notebook.add(my_frame1,text="Classes kotlin")

text_box_classes = ctk.CTkTextbox(my_frame1,font=ctk.CTkFont(size=15),wrap="none")
text_box_classes.pack(pady=3,fill="both",padx=3,expand="true")


# Tab Layout JSON
my_frame2 = Frame(my_notebook,width=500,heigh=500,bg="grey")
my_frame2.pack(fill="both",expand=1)
my_notebook.add(my_frame2,text="Json")

text_box_json = ctk.CTkTextbox(my_frame2,font=ctk.CTkFont(size=15),wrap="none")
text_box_json.pack(pady=3,fill="both",padx=3,expand="true")

start = ctk.CTkButton(master=openProject, text="Start request",command=start_function)
start.grid(row=3,column=0,pady=5, padx=5, sticky='NSWE')

root.mainloop()