import numpy as np
import tkinter as tk
from tkinter import ttk
import ttkwidgets as ttkw


class App:

    def __init__(self):

        master = tk.Tk()
        self.init_ui(master)

        master.mainloop()


    def init_ui(self, master):
        master.title("FPGA Controller")
        master.resizable(0, 0)

        #Configure style for tick sliders
        style = ttk.Style(master)
        style.configure("my.Vertical.TScale", background='#363636', foreground='#FFFFFF')

        #The size is just for reference. The window/outline Frame are auto-resized
        outline = tk.Frame(master, width=900, height=500, bg='#363636')

        #Draws an OS native menu for Save and Load. Change to dropdown "File" in future
        menubar = tk.Menu(master)
        menubar.add_command(label="Load", command=App.load_settings)
        menubar.add_command(label="Save", command=App.save_settings)
        menubar.add_command(label="Reset", command=lambda: App.reset_settings(self, master))
        menubar.add_command(label="Exit", command=lambda: App.exit(self, master))
        master.config(menu=menubar)


        #OUTPUT FRAME:
        #For further work in the future
        output_frame = tk.Frame(outline, width=150, height=150, bg='#191B1B')
        output_frame.grid(row=0, column=0, columnspan=2, padx=(375, 375), pady=(50, 25))


        #NOTEBAR FRAME
        notebar_frame = tk.Frame(outline, width=840, height=55, bg='#5B5B5B')
        notebar_frame.grid(row=1, column=0, padx=(30, 30), pady=(25, 30))
        self.fill_noteframe(notebar_frame)


        #CONTROL FRAME
        control_frame = tk.Frame(outline, width=840, height=200, bg='#363636')
        control_frame.grid(row=4, column=0, columnspan=2, padx=(30, 30), pady=(0, 20))

        #TOGGLE FRAME [CONTROL FRAME]
        toggle_frame = tk.Frame(control_frame, width=100, height=200, bg='#5B5B5B')
        toggle_frame.grid_propagate(0)
        self.fill_toggle_frame(toggle_frame)
        toggle_frame.grid(row=0, column=0, padx=(0, 15))

        #SLIDER FRAME [CONTROL FRAME]
        slider_frame = tk.Frame(control_frame, width=700, height=200, bg='#5B5B5B')
        slider_frame.grid_propagate(0)
        self.fill_slider_frame(slider_frame)
        slider_frame.grid(row=0, column=1, padx=(15, 0))


        outline.pack()



    def fill_toggle_frame(self, toggle_frame):
        def majorbox_click(event):
            self.serial_major(majorbox.curselection()[0])


        majorbox = tk.Listbox(toggle_frame, selectmode=tk.SINGLE, width=10, height=2, bg='#363636', fg="#FFFFFF",
                              borderwidth=0)
        majorbox.insert(tk.END, "Major")
        majorbox.insert(tk.END, "Minor")
        majorbox.selection_set(0)
        majorbox.bind("<<ListboxSelect>>", majorbox_click)
        majorbox.grid(row=0, column=0, padx=(20, 20), pady=(20, 20))

    def fill_slider_frame(self, slider_frame):

        octave_frame = tk.Frame(slider_frame, width=100, height=180, bg='#363636')
        octave_frame.grid_propagate(0)
        octave_frame.grid(row=0, column=0, padx=(20, 0), pady=10)

        octave_titletop = tk.Label(octave_frame, text="\u03948vb", bg='#363636', fg="#FFFFFF")
        octave_titletop.grid(row=0, column=0, padx=(32, 0))
        octave_slider = ttkw.TickScale(octave_frame, resolution=1, from_=-2, to_=2, orient='vertical',
                                       style="my.Vertical.TScale", length=130, value=0.0, tickinterval=-1, tickpos="w",
                                       showvalue=False, command = self.serial_octave)
        octave_slider.grid(row=1, column=0, padx=(20, 0))
        octave_titlebot = tk.Label(octave_frame, text="\u03948va", bg='#363636', fg="#FFFFFF")
        octave_titlebot.grid(row=2, column=0, padx=(32, 0))

        drywet_frame = tk.Frame(slider_frame, width=100, height=180, bg='#363636')
        drywet_frame.grid_propagate(0)
        drywet_frame.grid(row=0, column=1, padx=(20, 0), pady=10)

        drywet_titletop = tk.Label(drywet_frame, text="WET", bg='#363636', fg="#FFFFFF")
        drywet_titletop.grid(row=0, column=0, padx=(32, 0))
        drywet_slider = ttkw.TickScale(drywet_frame, resolution=1, from_=32, to_=0, orient='vertical',
                                       style="my.Vertical.TScale", length=130, value=0.0, tickinterval=0, command = self.serial_wet)
        drywet_slider.grid(row=1, column=0, padx=(16, 0))
        drywet_titlebot = tk.Label(drywet_frame, text="DRY", bg='#363636', fg="#FFFFFF")
        drywet_titlebot.grid(row=2, column=0, padx=(32, 0))

        speed_frame = tk.Frame(slider_frame, width=100, height=180, bg='#363636')
        speed_frame.grid_propagate(0)
        speed_frame.grid(row=0, column=2, padx=(20, 0), pady=10)

        speed_titletop = tk.Label(speed_frame, text="FAST", bg='#363636', fg="#FFFFFF")
        speed_titletop.grid(row=0, column=0, padx=(32, 0))
        speed_slider = ttkw.TickScale(speed_frame, resolution=1, from_=32, to_=0, orient='vertical',
                                      style="my.Vertical.TScale", length=130, value=0.0, tickinterval=0, command = self.serial_speed)
        speed_slider.grid(row=1, column=0, padx=(16, 0))
        speed_titlebot = tk.Label(speed_frame, text="SLOW", bg='#363636', fg="#FFFFFF")
        speed_titlebot.grid(row=2, column=0, padx=(32, 0))

        dist_frame = tk.Frame(slider_frame, width=100, height=180, bg='#363636')
        dist_frame.grid_propagate(0)
        dist_frame.grid(row=0, column=3, padx=(20, 0), pady=10)

        dist_titletop = tk.Label(dist_frame, text="DISTORT", bg='#363636', fg="#FFFFFF")
        dist_titletop.grid(row=0, column=0, padx=(26, 0))
        dist_slider = ttkw.TickScale(dist_frame, resolution=1, from_=32, to_=0, orient='vertical',
                                     style="my.Vertical.TScale", length=130, value=0.0, tickinterval=0, command = self.serial_distort)
        dist_slider.grid(row=1, column=0, padx=(12, 0))
        dist_titlebot = tk.Label(dist_frame, text="NONE", bg='#363636', fg="#FFFFFF")
        dist_titlebot.grid(row=2, column=0, padx=(28, 0))




    def fill_noteframe(self, notebar):
            notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
            def note_command(note):
                self.serial_note(note)
                for i in range(0, 12):
                    note_frames[i].configure(bg="#363636")
                    note_labels[i].configure(bg="#363636")
                note_frames[note].configure(bg="#199FFF")
                note_labels[note].configure(bg="#199FFF")



            note_command_list = [lambda event: note_command(0), lambda event: note_command(1), lambda event: note_command(2), lambda event: note_command(3),
                                lambda event: note_command(4), lambda event: note_command(5), lambda event: note_command(6), lambda event: note_command(7),
                                lambda event: note_command(8), lambda event: note_command(9), lambda event: note_command(10), lambda event: note_command(11)]
            note_frames = []
            note_labels = []


            for note in range(0, 12):
                note_frames.append(tk.Frame(notebar, width=60, height=42.5, bg="#363636"))
                note_frames[note].pack_propagate(0)
                if note == 11:
                    note_frames[note].grid(row=0, column=note, padx=(10, 10), pady=5)
                else:
                    note_frames[note].grid(row=0, column=note, padx=(10, 0), pady=5)
                note_frames[note].bind("<Button-1>", note_command_list[note])


                note_labels.append(tk.Label(note_frames[note], text=notes[note], bg="#363636", fg="#FFFFFF", font=("Calibri", 20)))
                note_labels[note].pack(pady=2)
                note_labels[note].bind("<Button-1>", note_command_list[note])




    def note_command(self, note):
        print

    def load_settings(self):
        print("Hello!")

    def save_settings(self):
        pass

    def reset_settings(self, master):
        master.destroy()
        master = tk.Tk()
        self.init_ui(master)

        master.mainloop()

    def exit(self, master):
        master.destroy()


    #NB: The Slider serials are likely going to need a debounce to prevent too many values from being gathered as the slider is adjusted.

    def serial_note(self, note):
        #Function to send serial data, runs whenever the user picks a new note
        #The argument note is an int from 0-11, corresponding to C C# D D# E F F# G G# A A# B
        pass

    def serial_major(self, major):
        #Function to send serial data, runs whenever the user changes the major/minor selection
        #The argument major is an int, with 1 for major and 0 for minor
        pass

    def serial_octave(self, octave):
        #Function to send serial data, runs whenever the user adjusts the octave shift slider
        #The argument octave is a float, chosen by the user as an int from -2 to 2
        pass

    def serial_wet(self, wet):
        #Function to send serial data, runs whenever the user adjusts the dry/wet slider
        #The argument wet is a float, chosen by the user as an int from 0 (dry) to 32 (wet)
        pass

    def serial_speed(self, speed):
        #Function to send serial data, runs whenever the user adjusts the slow/fast slider
        #The argument speed is a float, chosen by the user as an int from 0 (slow) to 32 (fast)
        pass

    def serial_distort(self, distort):
        #Function to send serial data, runs whenever the user adjusts the distortion slider
        #The argument distort is a float, chosen by the user as an int from 0 (none) to 32 (distorted)
        pass





app = App()