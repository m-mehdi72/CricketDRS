import cv2
import numpy as np
import threading
import os
import time
from functools import partial
from PIL import Image, ImageTk
import tkinter as tk
from cvzone.ColorModule import ColorFinder
from scipy.interpolate import UnivariateSpline
from cvzone.Utils import findContours

SET_WIDTH = 650
SET_HEIGHT = 368

class LBW(tk.Tk):

    def trajectory_t(self, loc):
        thread = threading.Thread(target=self.trajectory, args=(loc,))
        thread.daemon = 1
        thread.start()

    def trajectory(self, loc):
        # Creating colorfinder objects
        myColorFinder = ColorFinder(False)
        hsvVals = {'hmin': 152, 'smin': 157, 'vmin': 192, 'hmax': 179, 'smax': 255, 'vmax': 255}
        # hsvVals = {'hmin': 164, 'smin': 115, 'vmin': 255, 'hmax': 179, 'smax': 248, 'vmax': 255} 


        # Declaring variables
        posList = []

        cap = cv2.VideoCapture(loc)
        last_frame = None

        while True:
            success, img = cap.read()
            if not success:
                break

            # Finding ball color
            imgColor, mask = myColorFinder.update(img, hsvVals)

            # Ball Location
            imgContours, contours = findContours(img, mask, minArea=0.5)

            if contours:
                posList.append(contours[0]['center'])

            img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            img_resized = self.resize_image(img_pil, SET_WIDTH, SET_HEIGHT)
            photo = ImageTk.PhotoImage(image=img_resized)
            self.photo = photo
            x = (SET_WIDTH - img_resized.width) // 2
            y = (SET_HEIGHT - img_resized.height) // 2
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo)

            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1:
                last_frame = img.copy()

        cap.release()
        cv2.destroyAllWindows()

        graph_image = last_frame.copy()

        last_point = posList[-1]
        second_last_point = posList[-4]

        direction_vector = np.array(last_point) - np.array(second_last_point)

        blue_line_extension = 3

        blue_line_endpoint = last_point + blue_line_extension * direction_vector

        image_height, image_width, _ = graph_image.shape

        for i in range(len(posList) - 1):
            cv2.line(graph_image, posList[i], posList[i + 1], (0, 0, 255), 30)
            img_pil = Image.fromarray(cv2.cvtColor(graph_image, cv2.COLOR_BGR2RGB))
            img_resized = self.resize_image(img_pil, SET_WIDTH, SET_HEIGHT)
            photo = ImageTk.PhotoImage(image=img_resized)
            self.photo = photo
            x = (SET_WIDTH - img_resized.width) // 2
            y = (SET_HEIGHT - img_resized.height) // 2
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo)

        cv2.line(graph_image, last_point, tuple(blue_line_endpoint), (255, 0, 0), 30)
        img_pil = Image.fromarray(cv2.cvtColor(graph_image, cv2.COLOR_BGR2RGB))
        img_resized = self.resize_image(img_pil, SET_WIDTH, SET_HEIGHT)
        photo = ImageTk.PhotoImage(image=img_resized)
        self.photo = photo
        x = (SET_WIDTH - img_resized.width) // 2
        y = (SET_HEIGHT - img_resized.height) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo)
        

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
        print(loc)

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

        trajectory_button = tk.Button(button_frame, text="Track Trajectory", width=50, command=partial (self.trajectory_t, loc))
        trajectory_button.pack()

        prev_fast_button = tk.Button(button_frame, text="<< Previous (fast)", width=50, command=partial (self.play,-25, cap))
        prev_fast_button.pack()

        prev_slow_button = tk.Button(button_frame, text="<< Previous (slow)", width=50, command=partial (self.play,-2, cap))
        prev_slow_button.pack()

        next_slow_button = tk.Button(button_frame, text="Next (slow) >>", width=50, command=partial (self.play,2, cap))
        next_slow_button.pack()

        next_fast_button = tk.Button(button_frame, text="Next (fast) >>", width=50, command=partial (self.play,40, cap))
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
