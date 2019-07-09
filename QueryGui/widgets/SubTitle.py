from QueryGui.tkCompat import *

from QueryGui.Fonts import SUBTITLE_FONT, LARGE_LBL_ARGS


class SubTitle(ttk.Frame):
    def __init__(self, parent, controller, text, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.heading = ttk.Label(self, text=text, font=SUBTITLE_FONT, anchor='center', **kwargs)
        self.heading.pack(**LARGE_LBL_ARGS)
