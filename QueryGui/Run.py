from unfi_api.QueryGui.tkCompat import *
from .pages import *


def main():
    app = InvoiceMaster()
    app.mainloop()


class InvoiceMaster(tk.Tk):
    def __init__(self, *args, **kwargs):
        # Init Class Variables
        self.frames = {}
        self.user_input = {}
        self.frame_names = {}

        # Setup Tkinter Instance
        tk.Tk.__init__(self, *args, **kwargs)
        # self.iconbitmap(default=u'clienticon.ico')
        self.wm_title(u"Invoice Master")
        # self.geometry("600x500")
        style = ttk.Style()

        # Init main container
        container = ttk.Frame(self)
        container.pack(side=u"top", fill=u"both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # set default frame to WelcomePage and place it.
        frame = WelcomePage(container, self)
        frame.grid(row=0, column=0, sticky='nsew', pady=20, padx=20)

        # Load page widgets into the controller
        for F in PAGE_FRAMES:
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew', pady=20, padx=20)

        for obj, frm in self.frames.items():
            name = obj.__name__.split('.')[-1]
            self.frame_names[name] = frm
        # raise the main page and run the rest of the app
        self.show_frame(WelcomePage)

    def show_frame(self, cont):
        try:
            frame = self.frames[cont]
            frame.tkraise()
        except KeyError:
            frame = self.frame_names[cont]
            frame.tkraise()

    def get_frame(self, cont):
        try:
            frame = self.frames[cont]
        except KeyError:
            frame = self.frame_names[cont]
        return frame


if __name__ == '__main__':
    main()
