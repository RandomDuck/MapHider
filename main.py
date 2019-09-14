from hider import room
import tkinter as tk


#init tk loop
root = tk.Tk()
root.resizable(0,0)
root.title("MapHider")
#create canclass
rom=room(root)
#ask for image
rom.newIm()
#loop ending
root.mainloop()
