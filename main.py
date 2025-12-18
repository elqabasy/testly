"""
Updated main.py to serve as the entry point for the refactored Testly application.
"""

from ui.testly_app import TestlyApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = TestlyApp(root)
    root.mainloop()