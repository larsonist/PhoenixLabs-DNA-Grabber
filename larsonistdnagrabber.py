import subprocess
import sys
import re
import os
import tempfile
import shutil
from typing import Optional, Tuple
import tkinter as tk
from tkinter import ttk, messagebox, Text, scrolledtext
from tkinter.font import Font, families

class LarsonistDNAGrabber:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Larsonist's DNA Grabber")
        self.window.geometry("800x450")
        self.window.resizable(False, False)

        icon_path = self.resource_path("larsonist.ico")
        try:
            self.window.iconbitmap(icon_path)
        except:
            pass
        
        available_fonts = list(families())
        self.ui_font = self.get_best_font(['Segoe UI', 'Arial', 'Helvetica', 'Tahoma'])
        self.mono_font = self.get_best_font(['Consolas', 'Courier New', 'Courier', 'monospace'])
        
        self.colors = {
            'bg_dark': '#0F0F0F',
            'bg_darker': '#080808',
            'bg_lighter': '#1E1E1E',
            'accent_blue': '#2D5AF8', 
            'accent_light': '#3D7EFB',
            'accent_dark': '#1D3ED9',
            'text_primary': '#FFFFFF',
            'text_secondary': '#A0A0A0',
            'success_green': '#00DC82',
            'error_red': '#FF3366'
        }
        
        self.window.configure(bg=self.colors['bg_dark'])
        
        self.setup_styles()
        
        self.main_container = ttk.Frame(self.window, padding="30", style='Main.TFrame')
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        title_label = ttk.Label(
            self.main_container, 
            text="Larsonist's DNA Grabber", 
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, sticky="", pady=(0, 30))
        
        dna_frame = ttk.Frame(self.main_container, style='Card.TFrame')
        dna_frame.grid(row=1, column=0, sticky="ew", pady=(0, 25), padx=20)
        
        dna_label = ttk.Label(dna_frame, text="DEVICE DNA", style='CardTitle.TLabel')
        dna_label.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        
        self.dna_var = tk.StringVar()
        self.dna_label = ttk.Label(dna_frame, textvariable=self.dna_var, style='DNA.TLabel')
        self.dna_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 20))
        
        button_frame = ttk.Frame(self.main_container, style='Buttons.TFrame')
        button_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(4, weight=1)
        
        self.create_button = self.create_styled_button(
            button_frame, "READ DNA", self.read_dna
        )
        self.create_button.grid(row=0, column=1, padx=10)
        
        self.copy_button = self.create_styled_button(
            button_frame, "COPY TO CLIPBOARD", self.copy_to_clipboard
        )
        self.copy_button.grid(row=0, column=2, padx=10)
        
        self.debug_visible = False
        
        self.debug_toggle = self.create_styled_button(
            button_frame, "SHOW DEBUG", self.toggle_debug
        )
        self.debug_toggle.grid(row=0, column=3, padx=10)
        
        self.debug_frame = ttk.Frame(self.main_container, style='Card.TFrame')
        
        debug_label = ttk.Label(self.debug_frame, text="DEBUG CONSOLE", style='CardTitle.TLabel')
        debug_label.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        
        self.debug_text = Text(
            self.debug_frame,
            height=12,
            wrap=tk.WORD,
            font=(self.mono_font, 10),
            bg=self.colors['bg_darker'],
            fg=self.colors['text_secondary'],
            insertbackground=self.colors['accent_light'],
            borderwidth=0,
            padx=15,
            pady=15
        )
        self.debug_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(5, 20))
        
        scrollbar = ttk.Scrollbar(
            self.debug_frame, 
            orient="vertical", 
            command=self.debug_text.yview,
            style='Custom.Vertical.TScrollbar'
        )
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(5, 20))
        self.debug_text.configure(yscrollcommand=scrollbar.set)
        
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.debug_frame.grid_columnconfigure(0, weight=1)
        
        self.debug_text.config(highlightthickness=0)

    def get_best_font(self, font_list):
        available_fonts = list(families())
        for font in font_list:
            if font in available_fonts:
                return font
        return font_list[-1]

    def create_styled_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=(self.ui_font, 10, 'bold'),
            bg=self.colors['accent_light'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent_blue'],
            activeforeground=self.colors['text_primary'],
            borderwidth=0,
            padx=20,
            pady=12,
            cursor="hand2"
        )

    def setup_styles(self):
        style = ttk.Style()
        
        style.configure('Main.TFrame', 
                       background=self.colors['bg_dark'])
        
        style.configure('Title.TLabel',
                       font=(self.ui_font, 28, 'bold'),
                       background=self.colors['bg_dark'],
                       foreground=self.colors['text_primary'])
        
        style.configure('Card.TFrame', 
                       background=self.colors['bg_lighter'])
        
        style.configure('CardTitle.TLabel',
                       font=(self.ui_font, 11, 'bold'),
                       background=self.colors['bg_lighter'],
                       foreground=self.colors['accent_light'])
        
        style.configure('DNA.TLabel',
                       font=(self.mono_font, 12),
                       background=self.colors['bg_lighter'],
                       foreground=self.colors['text_primary'])
        
        style.configure('Buttons.TFrame', 
                       background=self.colors['bg_dark'])
        
        style.configure('Custom.Vertical.TScrollbar',
                       background=self.colors['bg_darker'],
                       troughcolor=self.colors['bg_darker'],
                       borderwidth=0,
                       arrowsize=12)

    def create_temp_config(self, base_config: str) -> Tuple[str, str]:
        temp_dir = tempfile.mkdtemp()
    
        required_files = [
            "xilinx-dna.cfg",
            "xilinx-xc7.cfg",
            "jtagspi.cfg"
        ]
    
        for file in required_files:
            src = self.resource_path(file)
            dst = os.path.join(temp_dir, file)
            shutil.copy2(src, dst)
    
        temp_dir_escaped = temp_dir.replace('\\', '/')
        config_content = f"""
adapter driver ch347
ch347 vid_pid 0x1a86 0x55dd 
adapter speed 10000
reset_config none

source "{temp_dir_escaped}/xilinx-dna.cfg"
source "{temp_dir_escaped}/xilinx-xc7.cfg"
source "{temp_dir_escaped}/jtagspi.cfg"
adapter_khz 10000

proc fpga_program {{}} {{
    global _CHIPNAME
    set dna [xc7_get_dna $_CHIPNAME.tap]
    xilinx_print_dna $dna
}}

init
fpga_program
shutdown
"""
        config_path = os.path.join(temp_dir, "temp_config.cfg")
        with open(config_path, "w") as f:
            f.write(config_content)
            
        return config_path, temp_dir
    
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def toggle_debug(self):
        if self.debug_visible:
            self.debug_frame.grid_remove()
            self.debug_toggle.configure(text="SHOW DEBUG")
            self.window.geometry("800x450")
        else:
            self.debug_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 20))
            self.debug_toggle.configure(text="HIDE DEBUG")
            self.window.geometry("800x700")
        self.debug_visible = not self.debug_visible

    def log_debug(self, message: str):
        self.debug_text.insert(tk.END, f"{message}\n")
        self.debug_text.see(tk.END)
        self.window.update()

    def _try_read_dna(self, config_file: str) -> bool:
        temp_config = None
        temp_dir = None
        
        try:
            self.log_debug(f"\nPreparing configuration...")
            temp_config, temp_dir = self.create_temp_config(config_file)
            
            cmd = [self.resource_path("patched_openocd.exe"), "-f", temp_config]
            self.log_debug(f"Command: {' '.join(cmd)}")
            
            CREATE_NO_WINDOW = 0x08000000
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                creationflags=CREATE_NO_WINDOW
            )
            
            full_output = result.stdout + result.stderr
            self.log_debug("\nOpenOCD Output:")
            self.log_debug(full_output)
            self.log_debug(f"\nReturn code: {result.returncode}")
            
            for line in full_output.split('\n'):
                if line.strip().startswith("DNA ="):
                    self.log_debug("Found DNA line!")
                    dna_text = line.split("DNA =")[1].strip()
                    parts = dna_text.split('(')
                    if len(parts) >= 2:
                        dna_binary = parts[0].strip()
                        dna_hex = parts[1].rstrip(')')
                        formatted_dna = f"{dna_binary}\n({dna_hex})"
                        self.dna_var.set(formatted_dna)
                        return True
            
            return False
            
        except Exception as e:
            self.log_debug(f"Error: {str(e)}")
            return False
        finally:
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    self.log_debug(f"Warning: Could not clean up temp directory: {str(e)}")

    def read_dna(self):
        self.debug_text.delete(1.0, tk.END)
        self.dna_var.set("")
        self.window.update()
        
        try:
            required_files = [
                "patched_openocd.exe",
                "xilinx-dna.cfg",
                "xilinx-xc7.cfg",
                "jtagspi.cfg"
            ]
            
            self.log_debug("Checking required files...")
            missing_files = []
            for file in required_files:
                file_exists = os.path.exists(self.resource_path(file))
                self.log_debug(f"  {file}: {'Found' if file_exists else 'Not Found'}")
                if not file_exists:
                    missing_files.append(file)
            
            if missing_files:
                raise Exception(f"Required files not found: {', '.join(missing_files)}")
            
            if self._try_read_dna("ch347"):
                return
            
            error_msg = ("Failed to retrieve DNA ID. Please make sure:\n\n"
                        "1. The correct driver is installed on your second PC\n"
                        "2. You are connected to the update/JTAG port on your card\n"
                        "3. Your main PC is powered on")
            self.log_debug("\nError: " + error_msg)
            messagebox.showerror("Error", error_msg)

        except Exception as e:
            self.log_debug(f"\nError: {str(e)}")
            messagebox.showerror("Error", str(e))

    def copy_to_clipboard(self):
        dna_text = self.dna_var.get()
        if dna_text:
            self.window.clipboard_clear()
            self.window.clipboard_append(dna_text)
            self.log_debug("DNA copied to clipboard")
        else:
            self.log_debug("No DNA value to copy")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = LarsonistDNAGrabber()
    app.run()