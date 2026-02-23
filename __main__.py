from compiler import COMPILE, Compiler_exception
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from config import CONFIG
import clipboard


def main():
    root = tk.Tk()
    root.withdraw()

    if not CONFIG["Ask for files ?"]:
        input_path = CONFIG["Default in file ?"]
        output_path = CONFIG["Default out file ?"]
    else:
        input_path = ""
        output_path = ""

    if input_path == "": input_path = filedialog.askopenfilename(
        title="Select BRANESIC file.",
        defaultextension=".brans",
    )
    output_text = ""
    try:
        output_text = COMPILE(input_path)
    except Compiler_exception as e:
        tk.messagebox.showerror("Compilation error !",e)
        print(str(type(e))+": "+str(e))
        return "error"
    
    if output_path == "" and CONFIG["Output to file ?"]: output_path = filedialog.asksaveasfile(
        title="It is done. Where to put it ?"
    ).name

    if CONFIG["Copy output to clipboard ?"]:clipboard.copy
    if CONFIG["Output to file ?"]: open(output_path, "w").write(output_text)

if __name__ == "__main__":
    main()