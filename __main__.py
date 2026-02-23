from compiler import COMPILE, Compiler_exception
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from config import CONFIG
import clipboard
import traceback


def main():
    root = tk.Tk()
    root.withdraw()

    if ("slef." in open("compiler.py", "r").read()):tk.messagebox.showwarning("slef.", "slef.")

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
    if type(input_path) != str: raise(Exception("User did not input a valid path !"))
    output_text = ""
    try:
        output_text = COMPILE(input_path)
    except Compiler_exception as e:
        tk.messagebox.showerror("Compilation error !",e)
        print(traceback.format_exc())
        print("\n\n"+str(type(e))+": "+str(e))
        return "error"
    
    if output_path == "" and CONFIG["Output to file ?"]:
        output_path = filedialog.asksaveasfile(title="It is done. Where to put it ?").name
        if type(output_path) != str: raise(Exception("User did not input a valid path !"))

    if CONFIG["Copy output to clipboard ?"]:clipboard.copy
    if CONFIG["Output to file ?"]: open(output_path, "w").write(output_text)

if __name__ == "__main__":
    main()
