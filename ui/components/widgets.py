"""
This module contains reusable widgets for the Testly application.
"""

import tkinter as tk
from tkinter import ttk

def create_button(parent, text, command, style="TButton"):
    """Create a styled button."""
    return ttk.Button(parent, text=text, command=command, style=style)

def create_label(parent, text, style="TLabel"):
    """Create a styled label."""
    return ttk.Label(parent, text=text, style=style)

def create_entry(parent, textvariable, show=None):
    """Create a styled entry widget."""
    return ttk.Entry(parent, textvariable=textvariable, show=show)

def create_progressbar(parent, maximum, style="Horizontal.TProgressbar"):
    """Create a styled progress bar."""
    return ttk.Progressbar(parent, maximum=maximum, style=style)