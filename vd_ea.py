import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import yt_dlp
import cv2
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import threading

class MediaToolkitApp:
# # Constructor to initialize the main application window
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader & editing Application")
        self.root.geometry("900x650")
        self.root.config(bg="#2E2E2E")
        self.video_path = None
        self.audio_path = None
        self.video_path_for_frame = None
        self.video_label_widget = None  # To display video preview
        self.playing = False
        self.language = "en"  # Default language is English
        self.setup_ui()
    # Function to translate text keys based on the selected language
    def translate(self, key):
        """Translate the key based on the selected language."""
        LANGUAGES = {
            "en": {
                # Translation keys for English
                "header": "Video Downloader & Editing Application",
                "tools": "Tools",
                "download_video": "Download Video",
                "download_audio": "Download Audio",
                "download_playlist": "Download Playlist",
                "download_facebook_video": "Download Facebook Video",
                "extract_image": "Extract Image",
                "cut_audio": "Cut Audio",
                "load_show_video": "Load & Show Video",
                "load_play_video": "Load & Play Video",
                "status_log": "Status Log",
                "error": "Error",
                "success": "Success",
                "processing": "Please wait... Processing your request",
                "select_video": "Select Video",
                "select_audio": "Select Audio",
                "download": "Download",
                "download_playlist": "Download Playlist",
                "cut_audio": "Cut Audio",
                "enter_time_for_image": "Enter Time for Image (seconds):",
                "enter_video_file": "Enter Video File:",
                "enter_mp3" : "Enter a YouTube URL to Download Audio:",
                "enter_playlist" : "Enter Playlist URL:",
                "enter_Facebook Video" : "Enter Facebook Video URL:",
                "no_select" : "No video selected.",
                "enter_Audio_File" : "Enter Audio File:",
                "start_time" : "Start Time (seconds):",
                "end_time" : "End Time (seconds):",
                "play_video" : "Play Video"
                
            },
            "kh": {
                # Translation keys for Khmer
                "header": "កម្មវិធីទាញយកវីដេអូ & កែសម្រួល",
                "tools": "ឧបករណ៍",
                "download_video": "ទាញយកវីដេអូ",
                "download_audio": "ទាញយកអូឌីយូ",
                "download_playlist": "ទាញយកបញ្ជីផ្សាយ",
                "download_facebook_video": "ទាញយកវីដេអូFacebook",
                "extract_image": "ចេញរូបភាព",
                "cut_audio": "កាត់អូឌីយូ",
                "load_show_video": "ផ្ទុក & បង្ហាញវីដេអូ",
                "load_play_video": "ផ្ទុក & លេងវីដេអូ",
                "status_log": "កំណត់ត្រាស្ថានភាព",
                "error": "កំហុស",
                "success": "ជោគជ័យ",
                "processing": "សូមរង់ចាំ... កំពុងបំពេញសំណើរបស់អ្នក",
                "select_video": "ជ្រើសវីដេអូ",
                "select_audio": "ជ្រើសអូឌីយូ",
                "download": "ទាញយក",
                "download_playlist": "ទាញយកបញ្ជីផ្សាយ",
                "cut_audio": "កាត់អូឌីយូ",
                "enter_time_for_image": "បញ្ចូលពេលវេលាសម្រាប់រូបភាព (វិនាទី):",
                "enter_video_file": "បញ្ចូលឯកសារវីដេអូ:",
                "enter_mp3" :"បញ្ចូលឯកសារអូឌីយូ:",
                "enter_playlist" :"បញ្ចូលកម្រងវីដេអូ" ,
                "enter_Facebook_Video" : "បញ្ចូលវីដេអូFacebook",
                "no_select" : "គ្មានវីដេអូជ្រើស",
                "enter_Audio_File" : "បញ្ចូលឯកសារអូឌីយូ",
                "start_time" : "ពេលវេលាចាប់ផ្តើម (វិនាទី)",
                "end_time" : "ពេលវេលាបញ្ចប់ (វិនាទី):",
                "play_video" : "វីដេអូដំណើរការ",
            }
        }
        return LANGUAGES[self.language].get(key, key)
    # Function to set up the user interface
    def setup_ui(self):
        self.create_header()
        self.create_side_panel()
        self.create_main_area()

    # Function to create the header section of the application
    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#333", height=50)
        header_frame.pack(fill="x")
        header_label = tk.Label(
            header_frame, text=self.translate("header"), font=("Arial", 18, "bold"), bg="#333", fg="orange"
        )
        header_label.pack(pady=15)
    # Function to create the side panel with tools and options
    def create_side_panel(self):
        side_panel = tk.Frame(self.root, bg="#444", width=200)
        side_panel.pack(side="left", fill="y")
        tk.Label(side_panel, text=self.translate("tools"), font=("Arial", 14, "bold"), bg="#444", fg="white").pack(pady=10)


        tools = [
            (self.translate("download_video"), self.download_video_ui),
            (self.translate("download_audio"), self.download_audio_ui),
            (self.translate("download_playlist"), self.download_playlist_ui),
            (self.translate("download_facebook_video"), self.download_facebook_video_ui),
            (self.translate("extract_image"), self.extract_image_ui),
            (self.translate("cut_audio"), self.cut_audio_ui),
            (self.translate("load_play_video"), self.load_and_play_video_ui)
        ]
        for tool in tools:
            self.create_side_button(side_panel, tool[0], tool[1])

        # Add a button to switch language
        language_button = tk.Button(
            side_panel, text="Switch to Khmer" if self.language == "en" else "Switch to English",
            command=self.toggle_language, font=("Arial", 12), bg="#4CAF50", fg="white", width=26, pady=10, padx=10, relief="flat", bd=0
        )
        language_button.pack(pady=10, padx=30)
    # Function to toggle the language of the application
    def toggle_language(self):
        """Toggle between English and Khmer."""
        self.language = "kh" if self.language == "en" else "en"
        self.update_language()
    # Function to refresh the UI components with the new language
    def update_language(self):
        """Update the language in all UI components."""
        self.root.title(self.translate("header"))
        # Update the header label
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()  # Rebuild the entire UI with the new language

        self.setup_ui()
    # Function to create buttons in the side panel
    def create_side_button(self, parent, text, command):
        button = tk.Button(
            parent, text = text, command = command, font = ("Arial", 12),
            bg="#4CAF50", fg="white", width=26, pady=10, padx=10, relief="flat", bd=0
        )
        button.pack(pady=10, padx=30)
    # Function to create the main content area
    def create_main_area(self):
        self.main_area = tk.Frame(self.root, bg="#2E2E2E")
        self.main_area.pack(side="right", expand=True, fill="both")
        self.main_area_top = tk.Frame(self.main_area, bg="#3A3A3A", pady=40, padx=20)
        self.main_area_top.pack(expand=True, fill="both")
        # Status log area for displaying detailed logs of actions
        self.status_log_frame = tk.Frame(self.main_area, bg="#3A3A3A", pady=10)
        self.status_log_frame.pack(fill="x", side="bottom")
        self.status_log_label = tk.Label(self.status_log_frame, text="Status Log", font=("Arial", 14, "bold"), bg="#3A3A3A", fg="white")
        self.status_log_label.pack(pady=5)
        self.status_log_text = tk.Text(self.status_log_frame, height=6, width=90, font=("Arial", 10), bg="#333", fg="white")
        self.status_log_text.pack(padx=10, pady=5)
        self.status_log_text.config(state=tk.DISABLED)  # Make it non-editable
    # Function to update the status log with a message
    def update_status_log(self, message):
        """Update the status log area with new message."""
        self.status_log_text.config(state=tk.NORMAL)
        self.status_log_text.insert(tk.END, f"{message}\n")
        self.status_log_text.yview(tk.END)
        self.status_log_text.config(state=tk.DISABLED)