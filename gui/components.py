"""
components
"""

import tkinter as tk
from tkinter import ttk
import math

class LightningLogo(tk.Canvas):
    def __init__(self, parent, width, height, colors, **kwargs):
        kwargs.update({
            'width': width,
            'height': height,
            'bg': colors['bg_dark'],
            'highlightthickness': 0
        })
        super().__init__(parent, **kwargs)
        self.colors = colors
        self.draw_lightning_logo()
        
    def draw_lightning_logo(self):
        width, height = self.winfo_reqwidth(), self.winfo_reqheight()
        
        # Lightning bolt coordinates - thanks, Claude!
        # Starting from top, going down in a zigzag pattern
        bolt_points = [
            width * 0.45, height * 0.15,  # Top point
            width * 0.25, height * 0.5,   # Middle left
            width * 0.45, height * 0.5,   # Middle center
            width * 0.28, height * 0.85,  # Bottom point
            width * 0.55, height * 0.45,  # Lower middle right
            width * 0.4, height * 0.45,   # Lower middle center
            width * 0.6, height * 0.15    # Back to top right
        ]
        
        # Draw the main bolt shape
        self.create_polygon(
            bolt_points,
            fill=self.colors['accent_blue'],
            outline="",
            smooth=False
        )
        
        # Add a subtle highlight/gradient effect
        highlight_points = [
            width * 0.45, height * 0.15,  # Top point
            width * 0.25, height * 0.5,   # Middle left
            width * 0.38, height * 0.48,  # Middle center (adjusted)
            width * 0.32, height * 0.7,   # Lower point (adjusted)
            width * 0.45, height * 0.45,  # Lower middle (adjusted)
        ]
        
        self.create_polygon(
            highlight_points,
            fill=self.colors['accent_light'],
            outline="",
            smooth=False
        )

def create_styled_button(parent, text, command, style_type='primary', colors=None, ui_font=None):
    if not colors:
        colors = {
            'accent_blue': '#0A84FF',
            'accent_light': '#4CA2FF',
            'bg_dark': '#1E1E1E',
            'bg_card': '#2C2C2E',
            'bg_lighter': '#3A3A3C',
            'text_primary': '#FFFFFF',
        }
    
    if not ui_font:
        ui_font = 'TkDefaultFont'
    
    button_styles = {
        'primary': {
            'bg': colors['accent_blue'],
            'fg': colors['text_primary'],
            'activebackground': colors['accent_light'],
            'activeforeground': colors['text_primary'],
            'font': (ui_font, 10, 'bold'),
            'padx': 20,
            'pady': 12,
        },
        'secondary': {
            'bg': colors['bg_lighter'],
            'fg': colors['text_primary'],
            'activebackground': '#4A4A4C',
            'activeforeground': colors['text_primary'],
            'font': (ui_font, 10, 'bold'),
            'padx': 20,
            'pady': 12,
        },
        'text': {
            'bg': colors['bg_dark'],
            'fg': colors['accent_blue'],
            'activebackground': colors['bg_dark'],
            'activeforeground': colors['accent_light'],
            'font': (ui_font, 10, 'bold'),
            'padx': 10,
            'pady': 8,
        }
    }
    
    style = button_styles.get(style_type, button_styles['primary'])
    
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=style['font'],
        bg=style['bg'],
        fg=style['fg'],
        activebackground=style['activebackground'],
        activeforeground=style['activeforeground'],
        borderwidth=0,
        padx=style['padx'],
        pady=style['pady'],
        cursor="hand2",
        highlightthickness=0,
        relief=tk.FLAT
    )
    
    if style_type != 'text':
        button.configure(padx=style['padx'] + 5)
    
    button.bind("<Enter>", lambda e: _on_button_hover(e, button, style))
    button.bind("<Leave>", lambda e: _on_button_leave(e, button, style))
    
    return button

def _on_button_hover(event, button, style):
    if 'bg' in style:
        current_bg = style['bg']
        r, g, b = int(current_bg[1:3], 16), int(current_bg[3:5], 16), int(current_bg[5:7], 16)
        
        r = min(255, r + 15)
        g = min(255, g + 15)
        b = min(255, b + 15)
        
        hover_bg = f'#{r:02x}{g:02x}{b:02x}'
        button.config(bg=hover_bg)

def _on_button_leave(event, button, style):
    if 'bg' in style:
        button.config(bg=style['bg'])