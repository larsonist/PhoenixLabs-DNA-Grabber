"""
gui impl
"""

import tkinter as tk
from tkinter import ttk, messagebox, Text
from tkinter.font import Font, families
import sys
import os
from typing import Optional, List

from gui.styles import GUIStyles
from gui.components import LightningLogo, create_styled_button
from gui.rounded_widgets import RoundedContainer, create_rounded_button
from core.dna_grabber import DNAGrabber

class LarsonistDNAGrabberGUI:
    def __init__(self, dna_grabber: DNAGrabber):
        self.dna_grabber = dna_grabber
        self.dna_grabber.set_debug_callback(self.log_debug)
        
        self.window = tk.Tk()
        self.window.title("Larsonist's DNA Grabber")
        self.window.geometry("800x340")  
        self.window.resizable(False, False)

        icon_path = self.resource_path("larsonist.ico")
        try:
            self.window.iconbitmap(icon_path)
        except:
            pass
        
        available_fonts = list(families())
        self.ui_font = self.get_best_font(['SF Pro', 'Helvetica Neue', 'Segoe UI', 'Arial', 'Helvetica', 'Tahoma'])
        self.mono_font = self.get_best_font(['SF Mono', 'Menlo', 'Cascadia Code', 'Consolas', 'Courier New', 'Courier'])
        
        self.styles = GUIStyles(self.ui_font, self.mono_font)
        self.colors = self.styles.colors
        
        self.window.configure(bg=self.colors['bg_dark'])
        
        self.styles.apply_styles()
        
        self.debug_visible = False
        
        self.build_ui()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def get_best_font(self, font_list):
        available_fonts = list(families())
        for font in font_list:
            if font in available_fonts:
                return font
        return font_list[-1]

    def build_ui(self):
        self.main_container = ttk.Frame(self.window, style='Main.TFrame')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.build_header()
        
        self.build_mode_selection()
        
        self.build_dna_display()
        
        self.build_buttons()
        
        spacer = ttk.Frame(self.main_container, height=15, style='Main.TFrame')
        spacer.pack(fill=tk.X)
        
        self.build_debug_console()

    def build_header(self):
        header_frame = ttk.Frame(self.main_container, style='Main.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        logo = LightningLogo(header_frame, 35, 35, self.colors)
        logo.pack(side=tk.LEFT)
        
        title_frame = ttk.Frame(header_frame, style='Main.TFrame')
        title_frame.pack(side=tk.LEFT, padx=10)
        
        title_label = ttk.Label(
            title_frame, 
            text="Larsonist's DNA Grabber", 
            style='Title.TLabel'
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(
            title_frame, 
            text="FPGA Device Identification Tool", 
            style='Subtitle.TLabel'
        )
        subtitle_label.pack(anchor=tk.W)
        
        self.debug_toggle = create_styled_button(
            header_frame, "SHOW DEBUG", self.toggle_debug, 'text', self.colors, self.ui_font
        )
        self.debug_toggle.pack(side=tk.RIGHT)

    def build_mode_selection(self):
        mode_frame = ttk.Frame(self.main_container, style='Main.TFrame')
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        mode_label = ttk.Label(mode_frame, text="Operation Mode:", style='SectionTitle.TLabel')
        mode_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.mode_var = tk.StringVar(value="auto")
        
        rb_auto = ttk.Radiobutton(
            mode_frame, 
            text="Auto Detect", 
            value="auto", 
            variable=self.mode_var,
            style='Mode.TRadiobutton'
        )
        rb_auto.pack(side=tk.LEFT, padx=10)
        
        rb_ch347 = ttk.Radiobutton(
            mode_frame, 
            text="CH347 Adapter", 
            value="ch347", 
            variable=self.mode_var,
            style='Mode.TRadiobutton'
        )
        rb_ch347.pack(side=tk.LEFT, padx=10)
        
        rb_ftdi = ttk.Radiobutton(
            mode_frame, 
            text="FTDI Adapter", 
            value="ftdi", 
            variable=self.mode_var,
            style='Mode.TRadiobutton'
        )
        rb_ftdi.pack(side=tk.LEFT, padx=10)

    def build_dna_display(self):
        container_frame = ttk.Frame(self.main_container, style='Main.TFrame', height=100)
        container_frame.pack(fill=tk.X, pady=(0, 15))
        container_frame.pack_propagate(False)  # force the frame to stay
        
        dna_container = RoundedContainer(
            container_frame, 
            self.colors['bg_card'], 
            corner_radius=10,
            padding=10
        )
        dna_container.pack(fill=tk.BOTH, expand=True)
        
        dna_inner = dna_container.inner_frame
        
        dna_header = ttk.Frame(dna_inner, style='CardInner.TFrame')
        dna_header.pack(fill=tk.X, pady=(0, 2))
        
        dna_label = ttk.Label(dna_header, text="DEVICE DNA", style='CardTitle.TLabel')
        dna_label.pack(side=tk.LEFT)
        
        self.status_frame = ttk.Frame(dna_header, style='Status.TFrame')
        self.status_frame.pack(side=tk.RIGHT)
        
        self.status_indicator = tk.Canvas(self.status_frame, width=10, height=10,
                                      bg=self.colors['bg_card'],
                                      highlightthickness=0)
        self.status_indicator.pack(side=tk.LEFT)
        self.status_indicator.create_oval(2, 2, 8, 8, fill=self.colors['text_muted'], outline="")
        
        self.status_label = ttk.Label(self.status_frame, text="No data", style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=(3, 0))
        
        self.dna_var = tk.StringVar()
        
        dna_content_frame = ttk.Frame(dna_inner, style='CardInner.TFrame', height=45)
        dna_content_frame.pack(fill=tk.X)
        dna_content_frame.pack_propagate(False)
        
        self.dna_label = ttk.Label(
            dna_content_frame, 
            textvariable=self.dna_var, 
            style='DNA.TLabel',
            justify=tk.CENTER,
            anchor=tk.CENTER
        )
        self.dna_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def build_buttons(self):
        button_frame = ttk.Frame(self.main_container, style='Main.TFrame')
        button_frame.pack(fill=tk.X, pady=15)
    
        button_center = ttk.Frame(button_frame, style='Main.TFrame')
        button_center.pack(anchor=tk.CENTER)
    
        self.read_button = tk.Button(
            button_center, 
            text="READ DNA",
            command=self.read_dna,
            font=(self.ui_font, 11, 'bold'),
            bg=self.colors['accent_blue'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent_light'],
            activeforeground=self.colors['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.read_button.pack(side=tk.LEFT, padx=15)
    
        self.copy_button = tk.Button(
            button_center, 
            text="COPY TO CLIPBOARD",
            command=self.copy_to_clipboard,
            font=(self.ui_font, 11, 'bold'),
            bg=self.colors['bg_lighter'],
            fg=self.colors['text_primary'],
            activebackground='#4A4A4C',
            activeforeground=self.colors['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.copy_button.pack(side=tk.LEFT, padx=15)
    
        def on_enter(e, button, hover_color):
            button.config(bg=hover_color)
    
        def on_leave(e, button, normal_color):
            button.config(bg=normal_color)
        
        self.read_button.bind("<Enter>", lambda e: on_enter(e, self.read_button, self.colors['accent_light']))
        self.read_button.bind("<Leave>", lambda e: on_leave(e, self.read_button, self.colors['accent_blue']))
    
        self.copy_button.bind("<Enter>", lambda e: on_enter(e, self.copy_button, '#4A4A4C'))
        self.copy_button.bind("<Leave>", lambda e: on_leave(e, self.copy_button, self.colors['bg_lighter']))

    def build_debug_console(self):
        self.debug_frame = ttk.Frame(self.main_container, style='Card.TFrame')
        
        debug_container = RoundedContainer(
            self.debug_frame, 
            self.colors['bg_card'], 
            corner_radius=12,
            padding=10
        )
        debug_container.pack(fill=tk.BOTH, expand=True)
        
        debug_inner = debug_container.inner_frame
        
        debug_header = ttk.Frame(debug_inner, style='CardInner.TFrame')
        debug_header.pack(fill=tk.X, pady=(0, 5))
        
        debug_label = ttk.Label(debug_header, text="DEBUG CONSOLE", style='CardTitle.TLabel')
        debug_label.pack(side=tk.LEFT)
        
        self.debug_text = Text(
            debug_inner,
            height=15,
            wrap=tk.WORD,
            font=(self.mono_font, 10),
            bg=self.colors['bg_darker'],
            fg=self.colors['text_secondary'],
            insertbackground=self.colors['accent_light'],
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.debug_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar_frame = ttk.Frame(debug_inner)
        scrollbar_frame.place(relx=1.0, rely=0, relheight=1, anchor='ne')
        
        scrollbar = ttk.Scrollbar(
            scrollbar_frame, 
            orient="vertical", 
            command=self.debug_text.yview,
            style='Custom.Vertical.TScrollbar'
        )
        scrollbar.pack(fill=tk.Y, expand=True)
        self.debug_text.configure(yscrollcommand=scrollbar.set)
        
        self.debug_text.config(highlightthickness=0)

    def toggle_debug(self):
        if self.debug_visible:
            self.debug_frame.pack_forget()
            self.debug_toggle.configure(text="SHOW DEBUG")
            self.window.geometry("800x340")
        else:
            self.debug_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 0))
            self.debug_toggle.configure(text="HIDE DEBUG")
            self.window.geometry("800x650")
        self.debug_visible = not self.debug_visible

    def log_debug(self, message: str):
        self.debug_text.insert(tk.END, f"{message}\n")
        self.debug_text.see(tk.END)
        self.window.update()

    def update_status(self, has_dna=False):
        if has_dna:
            self.status_indicator.create_oval(2, 2, 8, 8, fill=self.colors['success_green'], outline="")
            self.status_label.configure(text="DNA detected")
        else:
            self.status_indicator.create_oval(2, 2, 8, 8, fill=self.colors['text_muted'], outline="")
            self.status_label.configure(text="No data")

    def read_dna(self):
        self.debug_text.delete(1.0, tk.END)
        self.dna_var.set("")
        self.update_status(False)
        self.window.update()
        
        mode = self.mode_var.get()
        
        success, dna_text, error_msg = self.dna_grabber.read_dna(mode)
        
        if success and dna_text:
            self.dna_var.set(dna_text)
            self.update_status(True)
        elif error_msg:
            messagebox.showerror("Error", error_msg)

    def copy_to_clipboard(self):
        dna_text = self.dna_var.get()
        if dna_text:
            self.window.clipboard_clear()
            self.window.clipboard_append(dna_text)
            self.log_debug("DNA copied to clipboard")
            
            notification = tk.Toplevel(self.window)
            notification.overrideredirect(True)
            notification.attributes("-alpha", 0.0)
            notification.configure(bg=self.colors['bg_dark'])
            
            x = self.window.winfo_rootx() + (self.window.winfo_width() // 2) - 120
            y = self.window.winfo_rooty() + 40
            notification.geometry(f"240x50+{x}+{y}")
            
            notif_canvas = tk.Canvas(
                notification,
                bg=self.colors['bg_dark'],
                highlightthickness=0,
                bd=0,
                width=240,
                height=50
            )
            notif_canvas.pack(fill=tk.BOTH, expand=True)
            
            radius = 12
            width, height = 240, 50
            
            points = [
                radius, 0,
                width - radius, 0,
                width, 0,
                width, radius,
                width, height - radius,
                width, height,
                width - radius, height,
                radius, height,
                0, height,
                0, height - radius,
                0, radius,
                0, 0
            ]
            
            notif_canvas.create_polygon(
                points, 
                fill=self.colors['bg_card'], 
                outline="", 
                smooth=True
            )
            
            check_size = 20
            check_x = 30
            check_y = height//2
            
            notif_canvas.create_oval(
                check_x - check_size//2, 
                check_y - check_size//2,
                check_x + check_size//2, 
                check_y + check_size//2,
                fill=self.colors['success_green'],
                outline=""
            )
            
            checkmark_points = [
                check_x - 6, check_y,
                check_x - 2, check_y + 4,
                check_x + 6, check_y - 4
            ]
            notif_canvas.create_line(
                checkmark_points,
                fill="white",
                width=2,
                smooth=False,
                joinstyle=tk.ROUND,
                capstyle=tk.ROUND
            )
            
            label = tk.Label(
                notif_canvas, 
                text="Copied to clipboard", 
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary'],
                font=(self.ui_font, 11)
            )
            label.place(x=check_x + check_size + 10, y=height//2, anchor=tk.W)
            
            for i in range(1, 11):
                notification.attributes("-alpha", i/10)
                notification.update()
                notification.after(20)
            
            def fade_out():
                for i in range(10, -1, -1):
                    notification.attributes("-alpha", i/10)
                    notification.update()
                    notification.after(20)
                notification.destroy()
                
            self.window.after(1500, fade_out)
        else:
            self.log_debug("No DNA value to copy")

    def run(self):
        self.window.mainloop()