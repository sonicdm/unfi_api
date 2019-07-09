from unfi_api.QueryGui.tkCompat import *


class ProgressFrame(ttk.Frame):
    def __init__(self, parent, controller, i, start=0, end=0, labeltemplate=None, labelupdate=True, **kwargs):
        ttk.Frame.__init__(self, parent)

        self.pb = ttk.Progressbar(self, **kwargs)
        self.start = start
        self.end = end
        self.current_val = start
        self.pb["value"] = self.start
        self.pb["maximum"] = self.end
        self.pb.pack(side='top')
        self.labelupdate = True
        if labeltemplate:
            self.labeltext = labeltemplate.format(start=self.start, end=self.end)
            self.label = ttk.Label(self, text=labeltemplate)

    def start_val(self, val):
        self.start = val

    def end_val(self, val):
        self.end = val

    def inc(self, val):
        self.current_val = val
        self.pb['value'] = val

    def start(self, interval=None):
        self.pb.start(interval=interval)

    def stop(self):
        self.current_val = self.pb['value']
        self.pb.stop()
