import tkinter as tk
from tkinter import Variable, ttk
from tkinter import messagebox





            
# three page ui for Search, Download Progress, Save/Run Again

class MainContainer(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("UNFI File Search")
        self.geometry("600x400")
        self.resizable(False, False)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, SearchPage, DownloadPage, SavePage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def register_frame(self, frame):
        self.frames[frame] = frame

    def unregister_frame(self, frame):
        del self.frames[frame]

    def run(self):
        self.mainloop()

        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome to UNFI File Search", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Search", command=lambda: controller.show_frame(SearchPage))
        button1.pack()
        button2 = ttk.Button(self, text="Download", command=lambda: controller.show_frame(DownloadPage))
        button2.pack()
        button3 = ttk.Button(self, text="Save", command=lambda: controller.show_frame(SavePage))
        button3.pack()


class SearchPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Search", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        # search entry box. multi line
        self.search_entry = tk.Text(self, height=5, width=50)
        self.search_entry.pack()
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Search", command=lambda: controller.show_frame(DownloadPage))
        button2.pack()
        button3 = ttk.Button(self, text="Save", command=lambda: controller.show_frame(SavePage))
        button3.pack()
    
    def do_search(self):
        # do search
        pass


class DownloadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Download", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        # progress bar to show product download progress
        # label progress bar as Download Progress %



        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()


        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Search", command=lambda: controller.show_frame(SearchPage))
        button2.pack()
        button3 = ttk.Button(self, text="Save", command=lambda: controller.show_frame(SavePage))
        button3.pack()
    

class SavePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Save", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        # filename entry box defaults to "F:\POS\unfi\query.xlsx"
        self.filename_variable = tk.StringVar()
        self.filename_variable.set("F:\POS\unfi\query.xlsx")
        self.filename_entry = tk.Entry(self, width=50, textvariable=self.filename_variable)
        self.filename_entry.pack()

        # run again button to run again with new query
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Search", command=lambda: controller.show_frame(SearchPage))
        button2.pack()
        button3 = ttk.Button(self, text="Download", command=lambda: controller.show_frame(DownloadPage))
        button3.pack()





