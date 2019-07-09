try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox as mb
    from tkinter import simpledialog
    import tkcalendar
except ImportError:
    import Tkinter as tk
    from Tkinter import ttk
    from Tkinter import calendar as tkcalendar
    import tkMessageBox as mb
    import tkSimpleDialog as simpledialog
