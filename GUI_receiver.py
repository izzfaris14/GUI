# gui_receiver.py
import tkinter as tk
import cv2
from PIL import Image, ImageTk

import mock_setup  # TOMORROW: Change this to import real_script


class GatekeeperGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Attire Check System")

        # Lock to Kiosk Mode
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", lambda e: self.destroy())  # PRESS ESC TO QUIT

        # Configure 80/20 Layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)

        # Video Label
        self.video_label = tk.Label(self, bg="black")
        self.video_label.grid(row=0, column=0, sticky="nsew")

        # Status Label
        self.status_label = tk.Label(self, text="System Initializing...",
                                     font=("Helvetica", 48, "bold"), bg="gray", fg="white")
        self.status_label.grid(row=1, column=0, sticky="nsew")

        # Start the video engine
        self.update_frame()

    def update_frame(self):
        # 1. Ask the AI script for the newest annotated picture and text
        # TOMORROW: frame, text, color = real_script.get_processed_frame()
        frame, status_text, color = mock_setup.get_processed_frame()

        if frame is not None:
            # 2. Convert OpenCV format (BGR) to Tkinter format (RGB)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            # 3. Slap the image and the text onto the screen
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            self.status_label.config(text=status_text, bg=color)

        # 4. Repeat this loop every 10 milliseconds without freezing the app
        self.after(10, self.update_frame)


if __name__ == "__main__":
    app = GatekeeperGUI()
    app.mainloop()