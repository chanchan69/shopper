from tkinter import filedialog, Tk
from os import getcwd


def epic_file_dialog(title: str) -> str:
    root = Tk()
    root.attributes('-topmost',True)
    root.withdraw()
    path = filedialog.askopenfilename(title=title, initialdir=getcwd()) 
    return path