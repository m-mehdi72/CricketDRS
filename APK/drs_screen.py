import tkinter as tk
import threading
import cv2
from PIL import Image, ImageTk
from functools import partial
import os
import time

SET_WIDTH = 650
SET_HEIGHT = 368

class DRSScreen(tk.Tk):
    
    def play(self, speed, cap):
        self.speed = speed
        print(f"Speed is: {self.speed}")
        
        # Get the current frame position
        frame1 = cap.get(cv2.CAP_PROP_POS_FRAMES)
        
        # Set the frame position to the next frame based on the speed
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

        # Read the frame
        success, img = cap.read()
        
        # Convert the NumPy array to PIL Image
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        # Resize the image
        img_resized = self.resize_image(img_pil, SET_WIDTH, SET_HEIGHT)
        
        # Create a PhotoImage from the resized image
        photo = ImageTk.PhotoImage(image=img_resized)
        self.photo = photo
        
        # Calculate the coordinates to center the image
        x = (SET_WIDTH - img_resized.width) // 2
        y = (SET_HEIGHT - img_resized.height) // 2
        
        # Display the image on the canvas
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo)

    def pending(self, decision):
        image = Image.open("decision_pending.png")
        image = self.resize_image(image, SET_WIDTH, SET_HEIGHT)
        photo = ImageTk.PhotoImage(image=image)
        self.photo = photo
        x = (SET_WIDTH - image.width) // 2
        y = (SET_HEIGHT - image.height) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo)
        time.sleep(4)

        path = "Media"
        mylist = os.listdir(path)
        for img in mylist:
            Cur_img = cv2.imread(f"{path}/{img}")
            img_pil = Image.fromarray(cv2.cvtColor(Cur_img, cv2.COLOR_BGR2RGB))
            img_resized = self.resize_image(img_pil, SET_WIDTH, SET_HEIGHT)
            photo = ImageTk.PhotoImage(image=img_resized)
            self.photo = photo
            x = (SET_WIDTH - img_resized.width) // 2
            y = (SET_HEIGHT - img_resized.height) // 2
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo)
            time.sleep(0.1)

        if decision == 'out':
            Cur_img = cv2.imread("out.jpg")
            img_pil = Image.fromarray(cv2.cvtColor(Cur_img, cv2.COLOR_BGR2RGB))
            img_resized = self.resize_image(img_pil, SET_WIDTH, SET_HEIGHT)
            photo = ImageTk.PhotoImage(image=img_resized)
            self.photo = photo
            x = (SET_WIDTH - img_resized.width) // 2
            y = (SET_HEIGHT - img_resized.height) // 2
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo)
        else:
            Cur_img = cv2.imread("not_out.jpg")
            img_pil = Image.fromarray(cv2.cvtColor(Cur_img, cv2.COLOR_BGR2RGB))
            img_resized = self.resize_image(img_pil, SET_WIDTH, SET_HEIGHT)
            photo = ImageTk.PhotoImage(image=img_resized)
            self.photo = photo
            x = (SET_WIDTH - img_resized.width) // 2
            y = (SET_HEIGHT - img_resized.height) // 2
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo)            

    def out(self):
        thread = threading.Thread(target=self.pending, args=("out",))
        thread.daemon = 1
        thread.start()
        print("Player is Out")
        

    def not_out(self):
        thread = threading.Thread(target=self.pending, args=("not out",))
        thread.daemon = 1
        thread.start()
        print("Player is Not Out")
        

    def __init__(self, option_text, loc):
        super().__init__()
        self.title("DRS Screen")

        cap = cv2.VideoCapture(loc)

        self.label = tk.Label(self, text=f"You selected: {option_text}")
        self.label.pack()

        self.canvas = tk.Canvas(self, width=SET_WIDTH, height=SET_HEIGHT)
        self.canvas.pack()

        image_path = "stadium.jpg"

        # Load the image using PIL
        image = Image.open(image_path)

        # Resize the image while maintaining aspect ratio
        image = self.resize_image(image, SET_WIDTH, SET_HEIGHT)

        # Create a PhotoImage object from the resized image
        photo = ImageTk.PhotoImage(image=image)

        # Store the photo as an attribute
        self.photo = photo

        # Calculate the coordinates to center the image
        x = (SET_WIDTH - image.width) // 2
        y = (SET_HEIGHT - image.height) // 2

        # Display the image on the canvas
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        prev_fast_button = tk.Button(button_frame, text="<< Previous (fast)", width=50, command=partial (self.play,-20, cap))
        prev_fast_button.pack()

        prev_slow_button = tk.Button(button_frame, text="<< Previous (slow)", width=50, command=partial (self.play,-2, cap))
        prev_slow_button.pack()

        next_slow_button = tk.Button(button_frame, text="Next (slow) >>", width=50, command=partial (self.play,1, cap))
        next_slow_button.pack()

        next_fast_button = tk.Button(button_frame, text="Next (fast) >>", width=50, command=partial (self.play,20, cap))
        next_fast_button.pack()

        give_out_button = tk.Button(button_frame, text="Give Out", width=50,command=self.out)
        give_out_button.pack()

        give_not_out_button = tk.Button(button_frame, text="Give Not Out", width=50,command=self.not_out)
        give_not_out_button.pack()

    def resize_image(self, image, width, height):
        aspect_ratio = min(width / image.width, height / image.height)
        new_width = int(image.width * aspect_ratio)
        new_height = int(image.height * aspect_ratio)
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        return resized_image
