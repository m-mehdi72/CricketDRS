import tkinter as tk
from tkinter import messagebox, filedialog
from drs_screen import DRSScreen
from lbw import LBW

class CricketDRSApp(tk.Tk):

    def addFile(self):
        filename = filedialog.askopenfilename(initialdir="/", title = "Select file", 
        filetypes=(("MP4", "*.mp4"),("MOV", "*.mov"),("MKV ", "*.mkv"), ("All Files", "*.*")))
        return filename

    def __init__(self):
        super().__init__()
        self.title("Cricket DRS by ")
        self.geometry("300x400")

        # self.openFile = tk.Button(self, text = "Locate File", padx =10, pady = 5, fg = "#000000", bg = "#82E0AA", command=self.addFile)
        # self.openFile.pack()

        self.label = tk.Label(self, text="What do you want to check?",  pady = 5)
        self.label.pack()

        self.var = tk.IntVar()

        self.radio_low_catch = tk.Radiobutton(self, text="Low Catch",  pady = 5,variable=self.var, value=1)
        self.radio_low_catch.pack()

        self.radio_run_out = tk.Radiobutton(self, text="Run Out", pady = 5, variable=self.var, value=2)
        self.radio_run_out.pack()

        self.radio_stump_out = tk.Radiobutton(self, text="Stump Out",  pady = 5,variable=self.var, value=3)
        self.radio_stump_out.pack()

        self.radio_lbw = tk.Radiobutton(self, text="LBW", pady = 5, variable=self.var, value=4)
        self.radio_lbw.pack()

        self.radio_boundary_check = tk.Radiobutton(self, text="Boundary check", pady = 5, variable=self.var, value=5)
        self.radio_boundary_check.pack()

        self.check_button = tk.Button(self, text="Locate & Check",padx =10, pady = 5, fg = "#000000", bg = "#82E0AA", command=self.check_drs)
        self.check_button.pack()
    def check_drs(self):
        selected_option = self.var.get()

        if selected_option == 1:
            option_text = "Low Catch"
        elif selected_option == 2:
            option_text = "Run Out"
        elif selected_option == 3:
            option_text = "Stump Out"
        elif selected_option == 4:
            option_text = "LBW"
        elif selected_option == 5:
            option_text = "Boundary check"
        else:
            messagebox.showinfo("Error", "Please select an option.")
            return

        filename = self.addFile()  # Call addFile to get the filename

        self.destroy()

        if selected_option == 4:
            drs_app = LBW(option_text, filename)
            drs_app.mainloop()
        else:
            drs_app = DRSScreen(option_text, filename)  # Pass filename as a parameter
            drs_app.mainloop()


app = CricketDRSApp()
app.mainloop()
