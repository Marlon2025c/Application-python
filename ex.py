import tkinter as tk
from tkinter import messagebox as tkMessageBox

def click():
    name = entry.get()
    hello.config(text="Bonjour "+ name)
    tkMessageBox.showinfo("Hello", "Bonjour " + name)


window = tk.Tk()
window.title("Premier APP en Python")
window.geometry("400x400")

hello = tk.Label(window, text="Hello World", bg="red", fg="white")
hello.pack()

frame = tk.Frame(window, width=400, height=25)
frame.pack()

entry = tk.Entry(window)
entry.pack()

frame = tk.Frame(window, width=400, height=25)
frame.pack()

button = tk.Button(window, text="Cliquez ici", command=click)
button.pack()

window.mainloop()
