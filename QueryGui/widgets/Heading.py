from QueryGui.tkCompat import *

from QueryGui.Fonts import LARGE_FONT, LARGE_LBL_ARGS


class Heading(ttk.Frame):
    def __init__(self, parent, controller, text):
        ttk.Frame.__init__(self, parent)
        self.heading = ttk.Label(self, text=text, font=LARGE_FONT, anchor='center')
        self.heading.pack(**LARGE_LBL_ARGS)
