from unfi_api.QueryGui.tkCompat import *


class NavButtons(ttk.Frame):
    """
    A prebuilt class to easily unify controls across the app.
    """

    def __init__(self, parent, b1config=None, b2config=None, expand=None, fill=None, **kwargs):
        ttk.Frame.__init__(self, parent)
        text1 = None
        text2 = None
        if b1config:
            text1 = b1config.pop('text', None)
        else:
            b1config = {}
        if b2config:
            text2 = b2config.pop('text', None)
        else:
            b2config = {}

        if not text1:
            text1 = "Back"
        if not text2:
            text2 = "Next"
        button1 = ttk.Button(self, text=text1, **b1config)
        button2 = ttk.Button(self, text=text2, **b2config)
        button1.pack(side='left', pady=10, padx=10, expand=expand, fill=fill, **kwargs)
        button2.pack(side='right', pady=10, padx=10, expand=expand, fill=fill, **kwargs)
