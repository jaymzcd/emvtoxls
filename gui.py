#!/usr/bin/env python
import time
import os
import Tkinter as tk
import threading
import Queue
import ttk
from tkFileDialog import askopenfilename
from convert import parse


class Data(object):
    filename = None


class App(tk.Frame):

    PAD = 5
    nodata_val = None

    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master)
        self.parent = master
        self.filename_svar = tk.StringVar()
        self.outputname_svar = tk.StringVar()
        self.data = Data()
        self.queue = Queue.Queue()

        if self.parent is not None:
            self.parent.title('EMV XML to XLS Convertor')
            icon = tk.Image('photo', file='icon.gif')
            self.tk.call('wm', 'iconphoto', self.parent._w, icon)

        self.init_ui()

    def process_file(self):
        # Lets not let several jobs kick off now we're dealing with threads
        self.process_btn.config(state='disabled')
        name = self.outputname_svar.get()
        # lets be nice and prepend extensions if none given
        outfile = name if '.xls' in name else '{}.xls'.format(name)
        # Now point it to desktop - windows or linux huzzah
        outfile = os.path.expanduser('~/Desktop/{}'.format(outfile))
        infile = self.data.filename

        self.thread = ThreadedClient(self.queue, infile, outfile, self.nodata)
        self.thread.start()
        self.periodiccall()

    def periodiccall(self):
        self.checkqueue()
        if self.thread.is_alive():
            # Poll the queue to see if we need to update anything
            self.after(100, self.periodiccall)
        else:
            # Otherwise we're done so reactivate our button
            self.process_btn.config(state="active")

    def openfile(self):
       filename = askopenfilename(parent=self.parent, defaultextension="*.xml", filetypes=[('XML', '.xml'), ('Text', '*.txt'), ('All', '*')])
       self.filename_svar.set('File: {}'.format(os.path.basename(filename)))
       self.data.filename = filename

    def create_menu(self):
        menubar = tk.Menu(self.parent)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.openfile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.parent.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.about_dialog)
        menubar.add_cascade(label="Help", menu=helpmenu)

        return menubar

    def about_dialog(self):
        pass

    @property
    def nodata(self):
        val = self.nodata_val.get(tk.ACTIVE)
        if val == "Blank":
            return ''
        return val

    def add(self, elem, row=0, column=0, sticky=tk.N + tk.W, padx=PAD, pady=PAD, **kwargs):
        elem.grid(row=row, column=column, padx=self.PAD, pady=self.PAD, sticky=sticky, **kwargs)

    def init_ui(self):
        self.parent.minsize(300, 300)

        menu = self.create_menu()

        infile_label = tk.Label(self.parent, text="Input file:")
        self.add(infile_label)

        outfile_label = tk.Label(self.parent, text="Output name:")
        self.add(outfile_label, row=1)

        nodata_label = tk.Label(self.parent, text="When no data use this:")
        self.add(nodata_label, row=2)

        self.filename_svar.set("")
        infile_name = tk.Label(self.parent, textvariable=self.filename_svar, relief=tk.RAISED)
        self.add(infile_name, column=1)

        outputname_entry = tk.Entry(self.parent, textvariable=self.outputname_svar)
        self.add(outputname_entry, row=1, column=1, sticky=tk.E + tk.W)

        self.nodata_val = tk.Listbox(self.parent)
        self.add(self.nodata_val, row=2, column=1, sticky=tk.E + tk.W)

        for item in ["Blank", "N/A", "No data", "0", "False"]:
            self.nodata_val.insert(tk.END, item)

        self.progressbar = ttk.Progressbar(self.parent, orient='horizontal', length=300, mode='determinate')
        self.add(self.progressbar, row=3, columnspan=2, padx=20, pady=20, sticky=tk.W + tk.E)

        self.process_btn = tk.Button(self.parent, text="Process", command=self.process_file)
        self.add(self.process_btn, row=4, sticky=tk.W + tk.E)

        quit_btn = tk.Button(self.parent, text="Exit", command=self.parent.quit)
        self.add(quit_btn, row=4, column=1, sticky=tk.W + tk.E)

        self.parent.config(menu=menu)

    def checkqueue(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.filename_svar.set(msg)

                if 'entries' in msg:
                    self.progressbar.step(99)
                else:
                    self.progressbar.step(1)

            except Queue.Empty:
                pass


class ThreadedClient(threading.Thread):
    def __init__(self, queue, infile, outfile, nodata):
        threading.Thread.__init__(self)
        self.queue = queue
        self.infile = infile
        self.outfile = outfile
        self.nodata = nodata

    def run(self):

        def cb(count):
            self.queue.put('Processed {}'.format(count))

        process_output = parse(self.infile, self.outfile, nodata=self.nodata, callback=cb)
        self.queue.put(process_output)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()
