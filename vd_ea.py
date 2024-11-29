 
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

    def show_processing_message(self):      # Show a message box to indicate processing is ongoing.
        self.processing_window = tk.Toplevel(self.root)
        self.processing_window.title("Processing")
        self.processing_window.geometry("300x150")
        self.processing_window.config(bg="#2E2E2E")
        self.processing_label = tk.Label(self.processing_window, text="Please wait...\nProcessing your request", font=("Arial", 14), bg="#2E2E2E", fg="white")
        self.processing_label.pack(expand=True)

    def close_processing_message(self):     # Close the processing message window.
        self.processing_window.destroy()

    def load_and_play_video_ui(self):       # Allow the user to load and play a video in the interface.
        self.clear_main_area_top()
        self.create_input_field(self.main_area_top,self.translate ("enter_video_file"))
        video_button = tk.Button(self.main_area_top, text=self.translate ("select_video"), command=self.select_video, font=("Arial", 12), bg="#4CAF50", fg="white", width=20, pady=10)
        video_button.pack(pady=10)

        self.video_label = tk.Label(self.main_area_top, text=self.translate ("no_select"), font=("Arial", 12), bg="#3A3A3A", fg="white")
        self.video_label.pack(pady=10)

        def play_video():       # Play the selected video in the Tkinter window.
            if not self.video_path:
                messagebox.showerror("Error", "Please select a video first.")
                return

            if not self.playing:
                self.playing = True
                self.video_capture = cv2.VideoCapture(self.video_path)
                self.play_video_stream()

        self.create_action_button(self.main_area_top,self.translate ("play_video"), play_video)

    # Modify all the function labels to use the `self.translate()` method
    def download_video_ui(self):
        self.clear_main_area_top()
        self.create_input_field(self.main_area_top, self.translate("enter_video_file"))
        url_entry = self.create_url_entry(self.main_area_top)

        def download_video():       # Download Video from YouTube
            url = url_entry.get()
            if not url:
                messagebox.showerror(self.translate("error"), self.translate("error") + " Please enter a YouTube URL!")
                return
            download_path = filedialog.askdirectory()
            if not download_path:
                return

            self.show_processing_message()
            self.update_status_log(self.translate("download"))
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
            }

            threading.Thread(target=self.download_media, args=(url, ydl_opts)).start()


        self.create_action_button(self.main_area_top, self.translate("download"), download_video)

    def download_audio_ui(self):        # Download Audio from YouTube and save as mp3
        self.clear_main_area_top()
        self.create_input_field(self.main_area_top,self.translate ("enter_mp3"))
        url_entry = self.create_url_entry(self.main_area_top)

        def download_audio():
            url = url_entry.get()
            if not url:
                messagebox.showerror(self.translate("error"), self.translate("error") + " Please enter a YouTube URL!")
                return
            download_path = filedialog.askdirectory()
            if not download_path:
                return

            self.show_processing_message()
            self.update_status_log(self.translate("download"))
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            threading.Thread(target=self.download_media, args=(url, ydl_opts)).start()


        self.create_action_button(self.main_area_top, self.translate("download"), download_audio)


    def download_playlist_ui(self):     # Download Playlist from YouTube 
        self.clear_main_area_top()
        self.create_input_field(self.main_area_top,self.translate ("enter_playlist"))
        url_entry = self.create_url_entry(self.main_area_top)

        def download_playlist():
            url = url_entry.get()
            if not url:
                messagebox.showerror(self.translate("error"), self.translate("error") + " Please enter a playlist URL!")
                return
            download_path = filedialog.askdirectory()
            if not download_path:
                return

            self.show_processing_message()
            self.update_status_log(self.translate ,("download"))
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
            }

            threading.Thread(target=self.download_media, args=(url, ydl_opts)).start()

        self.create_action_button(self.main_area_top,self.translate("download"), download_playlist)

    def download_facebook_video_ui(self):       # Download Video from Facebook
        self.clear_main_area_top()
        self.create_input_field(self.main_area_top,self.translate ("enter_Facebook_Video"))
        url_entry = self.create_url_entry(self.main_area_top)

        def download_facebook_video():
            url = url_entry.get()
            if not url:
                messagebox.showerror(self.translate("error"), self.translate("error") + "Please enter a Facebook video URL!")
                return
            download_path = filedialog.askdirectory()
            if not download_path:
                return

            self.show_processing_message()
            self.update_status_log(self.translate,("Starting Facebook video download..."))
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
            }

            threading.Thread(target=self.download_media, args=(url, ydl_opts)).start()

        self.create_action_button(self.main_area_top,self.translate ("download"), download_facebook_video)

    def download_media(self, url, ydl_opts):        # Handle downloading media (audio/video).
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                self.close_processing_message()
                messagebox.showinfo("Success", "Download complete!")
                self.update_status_log("Download complete.")
        except Exception as e:
            self.close_processing_message()
            messagebox.showerror("Error", f"Error during download: {e}")
            self.update_status_log(f"Error: {e}")


    def progress_hook(self, d):     # Callback function for download progress.
        if d['status'] == 'downloading':
            self.update_status_log(f"Downloading: {d['filename']} - {d['downloaded_bytes'] / 1024 / 1024:.2f} MB")
    # --- Extract Image from Video ---
    def extract_image_ui(self):
        self.clear_main_area_top()
        self.create_input_field(self.main_area_top,self.translate ("enter_video_file"))
        video_button = tk.Button(self.main_area_top, 
        text= self.translate ("select_video"),
            command=self.select_video, 
            font=("Arial", 12),
            bg="#4CAF50", 
            fg="white", 
            width=20, 
            pady=10)
        video_button.pack(pady=10)

        self.video_label = tk.Label(self.main_area_top, text=self.translate ("no_select"), font=("Arial", 12), bg="#3A3A3A", fg="white")
        self.video_label.pack(pady=10)

        time_label = tk.Label(self.main_area_top, text= self.translate ("enter_time_for_image"), font=("Arial", 12), bg="#3A3A3A", fg="white")
        time_label.pack(pady=5)

        self.time_entry = tk.Entry(self.main_area_top, font=("Arial", 12))
        self.time_entry.pack(pady=10)


        def extract_image():  
            time = self.time_entry.get()
            if not time:
                messagebox.showerror("Error",messagebox.showerror(self.translate("error"), self.translate("error") + "Please enter a valid time."))
                return


            try:
                time = float(time)
            except ValueError:
                messagebox.showerror("Error",messagebox.showerror(self.translate("error"), self.translate("error") + "Time must be a number."))
                return

            output_path = filedialog.askdirectory()
            if not output_path:
                return

            self.show_processing_message()
            self.update_status_log(self.translate ("extract_image"))

            threading.Thread(target=self.extract_image_task, args=(output_path, time)).start()

        self.create_action_button(self.main_area_top,self.translate ("extract_image"), extract_image)
    def extract_image_task(self, output_path, time):
        """Extract an image at the given time from the video."""
        try:
            # Load the video from the specified path
            video_clip = cv2.VideoCapture(self.video_path_for_frame)
            
            # Get frames per second (FPS) to calculate the frame number for the given time
            fps = video_clip.get(cv2.CAP_PROP_FPS)
            frame_number = int(fps * time)

            # Set the video position to the desired frame
            video_clip.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            success, image = video_clip.read()  # Read the frame at the specified time

            if success:
                # Save the extracted image at the specified output path
                image_path = f"{output_path}/extracted_image_{time}.png"
                cv2.imwrite(image_path, image)
                
                # Close the processing message and show success notification
                self.close_processing_message()
                messagebox.showinfo("Success", f"Image extracted successfully at {time}s!")
                
                # Update the status log with the success message
                self.update_status_log(f"Image extracted at {time}s!")
            else:
                # Handle the case where the image extraction fails
                self.close_processing_message()
                messagebox.showerror("Error", "Error extracting image.")
        except Exception as e:
            # Handle unexpected exceptions and log the error message
            self.close_processing_message()
            messagebox.showerror("Error", f"Error during image extraction: {e}")
            self.update_status_log(f"Error: {e}")

    # --- Cut Audio ---
    def cut_audio_ui(self):
        """Create the UI for cutting audio."""
        self.clear_main_area_top()  # Clear the UI area before adding new widgets

        # Create input field for selecting the audio file
        self.create_input_field(self.main_area_top, self.translate("enter_Audio_File"))

        # Button to select the audio file
        audio_button = tk.Button(
            self.main_area_top,
            text=self.translate("select_video"),
            command=self.select_audio,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            width=20,
            pady=10
        )
        audio_button.pack(pady=10)

        # Label to display the selected audio file
        self.audio_label = tk.Label(
            self.main_area_top,
            text=self.translate("no_select"),
            font=("Arial", 12),
            bg="#3A3A3A",
            fg="white"
        )
        self.audio_label.pack(pady=10)

        # Label and input field for start time
        start_time_label = tk.Label(
            self.main_area_top,
            text=self.translate("start_time"),
            font=("Arial", 12),
            bg="#3A3A3A",
            fg="white"
        )
        start_time_label.pack(pady=5)

        self.start_time_entry = tk.Entry(self.main_area_top, font=("Arial", 12))
        self.start_time_entry.pack(pady=10)

        # Label and input field for end time
        end_time_label = tk.Label(
            self.main_area_top,
            text=self.translate("end_time"),
            font=("Arial", 12),
            bg="#3A3A3A",
            fg="white"
        )
        end_time_label.pack(pady=5)

        self.end_time_entry = tk.Entry(self.main_area_top, font=("Arial", 12))
        self.end_time_entry.pack(pady=10)

        def cut_audio():
            """Callback to cut the audio based on the provided times."""
            start_time = self.start_time_entry.get()
            end_time = self.end_time_entry.get()

            if not start_time or not end_time:
                # Show error if times are not specified
                messagebox.showerror(
                    self.translate("error"),
                    self.translate("error") + " Please specify both start and end time."
                )
                return


            try:
                # Convert the input times to float values
                start_time = float(start_time)
                end_time = float(end_time)
            except ValueError:
                # Show error if input values are not valid numbers
                messagebox.showerror(
                    self.translate("error"),
                    self.translate("error") + " Start and End times must be numbers."
                )
                return

            # Ask the user for the output directory
            output_path = filedialog.askdirectory()
            if not output_path:
                return  # Exit if no output path is selected

            # Show processing message and log the cutting process
            self.show_processing_message()
            self.update_status_log(self.translate("cut_audio"))

            # Start the audio cutting in a separate thread
            threading.Thread(target=self.cut_audio_task, args=(output_path, start_time, end_time)).start()

        # Create a button to trigger the audio cutting
        self.create_action_button(self.main_area_top, self.translate("cut_audio"), cut_audio)

    def cut_audio_task(self, output_path, start_time, end_time):
        """Cut audio from the selected audio file."""
        try:
            # Load the audio file using moviepy
            audio_clip = AudioFileClip(self.audio_path)
            
            # Extract the audio subclip from start_time to end_time
            audio_clip = audio_clip.subclip(start_time, end_time)
            
            # Save the cut audio to the specified output path
            audio_clip.write_audiofile(f"{output_path}/cut_audio.mp3")
            
            # Close the processing message and show success notification
            self.close_processing_message()
            messagebox.showinfo("Success", "Audio cut successfully!")
            
            # Update the status log with the completion message
            self.update_status_log("Audio cutting complete.")
        except Exception as e:
            # Handle unexpected exceptions and log the error message
            self.close_processing_message()
            messagebox.showerror("Error", f"Error during audio cutting: {e}")
            self.update_status_log(f"Error: {e}")
    def select_audio(self):
        """Allow user to select an audio file."""
        # Open file dialog to select audio file (mp3 or wav)
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.mp3 *.wav"), ("All Files", "*.*")]
        )
        if file_path:
            # Save the selected audio file path and update the label with the file name
            self.audio_path = file_path
            self.audio_label.config(text=f"Audio selected: {os.path.basename(file_path)}")

    def select_video(self):
        """Allow user to select a video file."""
        # Open file dialog to select video file (mp4)
        file_path = filedialog.askopenfilename(
            filetypes=[("MP4 Files", "*.mp4"), ("All Files", "*.*")]
        )
        if file_path:
            # Save the selected video file path
            self.video_path = file_path
            self.video_path_for_frame = file_path
            
            # Update the label with the selected video file name
            self.video_label.config(text=f"Video selected: {os.path.basename(file_path)}")

    def create_input_field(self, parent, text):
        """Create an input field with a label for user input."""
        # Create a label with the given text and add it to the parent widget
        label = tk.Label(
            parent, text=text, font=("Arial", 14), bg="#3A3A3A", fg="white"
        )
        label.pack(pady=20)  # Add padding for better spacing

    def create_url_entry(self, parent):
        """Create URL entry field."""
        # Create an entry field for entering URLs
        url_entry = tk.Entry(parent, font=("Arial", 16), width=30)
        url_entry.pack(pady=12)  # Add padding for better spacing
        return url_entry  # Return the entry widget for later use

    def create_action_button(self, parent, text, command):
        """Create an action button for tasks."""
        # Create a button with the given text and command, then add it to the parent widget
        button = tk.Button(
            parent, text=text, command=command, font=("Arial", 12),
            bg="green", fg="white", width=22, pady=10
        )
        button.pack(pady=16)  # Add padding for better spacing

    def clear_main_area_top(self):
        """Clear the main area for new UI components."""
        # Destroy all child widgets in the main_area_top to clear the UI
        for widget in self.main_area_top.winfo_children():
            widget.destroy()

    def play_video_stream(self):
        """Play the video stream by continuously updating the video frames."""
        if self.video_capture.isOpened():  # Check if the video capture is opened
            ret, frame = self.video_capture.read()  # Read the next frame
            if ret:
                # Convert the frame from BGR to RGB (OpenCV uses BGR by default)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert the frame to a PIL image and then to a format suitable for Tkinter
                frame_image = Image.fromarray(frame_rgb)
                frame_tk = ImageTk.PhotoImage(frame_image)

                if self.video_label_widget:
                    # Update the existing label with the new frame
                    self.video_label_widget.config(image=frame_tk)
                    self.video_label_widget.image = frame_tk  # Keep a reference to avoid garbage collection
                else:
                    # Create a new label if it doesn't exist and display the frame
                    self.video_label_widget = tk.Label(self.main_area_top, image=frame_tk)
                    self.video_label_widget.image = frame_tk  # Keep a reference
                    self.video_label_widget.pack(pady=10)

                # Schedule the function to be called again after a short delay (10ms)
                self.video_label_widget.after(10, self.play_video_stream)
            else:
                # Release the video capture when there are no more frames to read
                self.video_capture.release()
                self.playing = False  # Mark the video as stopped
    # Check if the current script is the main program being executed
if __name__ == "__main__":
    # Create an instance of the Tkinter main window (root window)
    root = tk.Tk()
    
    # Instantiate the MediaToolkitApp class with the root window as its parent
    # This is likely the main application class that defines the GUI
    app = MediaToolkitApp(root)
    
    # Enter the Tkinter event loop to keep the application running and responsive
    root.mainloop()
