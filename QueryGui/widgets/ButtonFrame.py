from unfi_api.QueryGui.tkCompat import *


class ButtonFrame(ttk.Frame):
    def __init__(self, parent, controller,
                 labeltext=None, labelargs=None, labelpack=None,
                 buttonpack=None, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.labelargs = labelargs
        self.lablepack = labelpack
        self.button = ttk.Button(self, **kwargs)

        if labeltext:
            if labelargs:
                label = ttk.Label(self, text=labeltext, **labelargs)
            else:
                label = ttk.Label(self, text=labeltext)

            if labelpack:
                label.pack(**labelpack)
            else:
                label.pack()

        if buttonpack:
            self.button.pack(**buttonpack)
        else:
            self.button.pack()
