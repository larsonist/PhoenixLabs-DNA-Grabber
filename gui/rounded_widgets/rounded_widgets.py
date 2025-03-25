"""
prob not gonna use
"""

import tkinter as tk
from tkinter import ttk

class RoundedContainer:
    def __init__(self, parent, bg_color, corner_radius=10, padding=15):
        self.parent = parent
        self.bg_color = bg_color
        self.corner_radius = corner_radius
        self.padding = padding
        
        self.outer_frame = ttk.Frame(parent)
        
        parent_bg = self._get_safe_bg(parent)
        
        self.canvas = tk.Canvas(
            self.outer_frame,
            bg=parent_bg,
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.inner_frame = ttk.Frame(self.canvas, style='CardInner.TFrame')
        
        self.canvas.bind("<Configure>", self._on_resize)
    
    def _get_safe_bg(self, widget):
        try:
            return widget.cget('bg')
        except:
            try:
                if isinstance(widget, ttk.Widget):
                    style_name = widget.cget('style')
                    if not style_name:
                        widget_class = widget.winfo_class()
                        style_name = widget_class
                    
                    style = ttk.Style()
                    return style.lookup(style_name, 'background')
            except:
                pass
        
        return '#1E1E1E'
        
    def _on_resize(self, event):
        width, height = event.width, event.height
        
        self.canvas.delete("all")
        
        self._create_rounded_rect(
            0, 0, width, height, 
            self.corner_radius, 
            fill=self.bg_color, 
            outline=""
        )
        
        self.canvas.create_window(
            self.padding, 
            self.padding, 
            anchor=tk.NW, 
            window=self.inner_frame, 
            width=width - 2*self.padding, 
            height=height - 2*self.padding
        )
    
    def _create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1, 
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1,
        ]
        
        return self.canvas.create_polygon(points, **kwargs, smooth=True)
        
    def pack(self, **kwargs):
        self.outer_frame.pack(**kwargs)
        
    def grid(self, **kwargs):
        self.outer_frame.grid(**kwargs)
        
    def place(self, **kwargs):
        self.outer_frame.place(**kwargs)

def create_rounded_button(parent, text, command, bg_color, fg_color, hover_color, 
                         active_color, font, padx=20, pady=10, corner_radius=8,
                         width=None, height=None):
    parent_bg = _get_safe_bg(parent)
    
    frame = tk.Frame(parent, bg=parent_bg)
    
    canvas = tk.Canvas(
        frame,
        width=width or 120,
        height=height or 40,
        bg=parent_bg,
        highlightthickness=0,
        bd=0
    )
    canvas.pack(fill=tk.BOTH, expand=True)
    
    button = tk.Button(
        frame,
        text=text,
        command=command,
        font=font,
        bg=bg_color,
        fg=fg_color,
        activebackground=active_color,
        activeforeground=fg_color,
        borderwidth=0,
        padx=padx,
        pady=pady,
        cursor="hand2",
        highlightthickness=0,
        relief=tk.FLAT
    )
    
    frame.is_rounded = True
    button.hover_color = hover_color
    button.normal_color = bg_color
    
    def update_canvas(event=None):
        w, h = button.winfo_width(), button.winfo_height()
        canvas.configure(width=w, height=h)
        canvas.delete("rounded_rect")
        
        x0, y0, x1, y1 = 0, 0, w, h
        radius = min(corner_radius, w/2, h/2)
        
        points = [
            x0+radius, y0,
            x1-radius, y0,
            x1, y0,
            x1, y0+radius,
            x1, y1-radius,
            x1, y1,
            x1-radius, y1,
            x0+radius, y1,
            x0, y1,
            x0, y1-radius,
            x0, y0+radius,
            x0, y0,
        ]
        
        canvas.create_polygon(points, fill=button.cget('bg'), outline="", smooth=True, tags="rounded_rect")
    
    button.bind("<Configure>", update_canvas)
    button.bind("<Map>", update_canvas)
    
    def on_enter(e):
        button.config(bg=button.hover_color)
        update_canvas()
    
    def on_leave(e):
        button.config(bg=button.normal_color)
        update_canvas()
    
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    
    button_window = canvas.create_window(0, 0, anchor=tk.NW, window=button)
    
    def on_canvas_resize(event):
        canvas.coords(button_window, 0, 0)
        canvas.itemconfig(button_window, width=event.width, height=event.height)
    
    canvas.bind("<Configure>", on_canvas_resize)
    
    canvas.update_idletasks()
    update_canvas()
    
    return frame

def _get_safe_bg(widget):
    try:
        return widget.cget('bg')
    except:
        try:
            if isinstance(widget, ttk.Widget):
                style_name = widget.cget('style')
                if not style_name:
                    widget_class = widget.winfo_class()
                    style_name = widget_class
                
                style = ttk.Style()
                return style.lookup(style_name, 'background')
        except:
            pass
    
    return '#1E1E1E'