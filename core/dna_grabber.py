"""
the actual grabber
"""

import os
import sys
import subprocess
import tempfile
import shutil
from typing import Optional, Tuple, List, Callable

class DNAGrabber:
    def __init__(self):
        self.debug_callback = None
    
    def set_debug_callback(self, callback: Callable[[str], None]):
        self.debug_callback = callback

    def log_debug(self, message: str):
        if self.debug_callback:
            self.debug_callback(message)
    
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def extract_dna_from_output(self, output: str) -> Optional[str]:
        """extract the DNA value from openocd"""
        for line in output.split('\n'):
            if line.strip().startswith("DNA ="):
                self.log_debug(f"Found DNA line: {line}")
                dna_text = line.split("DNA =")[1].strip()
                parts = dna_text.split('(')
                if len(parts) >= 2:
                    dna_binary = parts[0].strip()
                    dna_hex = parts[1].rstrip(')')
                    formatted_dna = f"{dna_binary}\n({dna_hex})"
                    return formatted_dna
        return None

    def create_direct_bat_method(self, temp_dir):
        # Create Windows batch files that directly call the executables if needed
        ftdi_bat_path = os.path.join(temp_dir, "run_ftdi.bat")
        ch347_bat_path = os.path.join(temp_dir, "run_ch347.bat")
        
        # Copy all required files to temp directory
        for file in os.listdir(self.resource_path(".")):
            src_path = self.resource_path(file)
            if os.path.isfile(src_path):
                dst_path = os.path.join(temp_dir, file)
                try:
                    shutil.copy2(src_path, dst_path)
                    self.log_debug(f"Copied {file} to temp directory")
                except Exception as e:
                    self.log_debug(f"Failed to copy {file}: {str(e)}")
        
        # Create FTDI batch file
        with open(ftdi_bat_path, "w") as f:
            f.write(f'cd /d "{temp_dir}"\r\n')
            f.write('openocd.exe -f init_232_35t.cfg\r\n')
            f.write('exit\r\n')
        
        # Create CH347 batch file
        with open(ch347_bat_path, "w") as f:
            f.write(f'cd /d "{temp_dir}"\r\n')
            f.write('openocd-347.exe -f init_347_35t.cfg\r\n')
            f.write('exit\r\n')
            
        return ftdi_bat_path, ch347_bat_path
    
    def read_dna(self, mode="auto") -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Main function to read DNA from the device
        
        Args:
            mode: The adapter mode to use ("auto", "ftdi", or "ch347")
            
        Returns:
            Tuple containing:
                - Success status (bool)
                - DNA string if successful, None otherwise
                - Error message if failed, None otherwise
        """
        temp_dir = None
        
        try:
            # create temp dir
            temp_dir = tempfile.mkdtemp()
            self.log_debug(f"Created temporary directory: {temp_dir}")
            
            # create bat
            ftdi_bat, ch347_bat = self.create_direct_bat_method(temp_dir)
            
            # check availability
            ch347_available = os.path.exists(os.path.join(temp_dir, "openocd-347.exe"))
            ftdi_available = os.path.exists(os.path.join(temp_dir, "openocd.exe"))
            
            self.log_debug("\nChecking available adapters:")
            self.log_debug(f"  CH347: {'Available' if ch347_available else 'Not Available'}")
            self.log_debug(f"  FTDI: {'Available' if ftdi_available else 'Not Available'}")
            
            if not ch347_available and not ftdi_available:
                error = "No OpenOCD executables found. Either openocd.exe or openocd-347.exe is required."
                return False, None, error
            
            self.log_debug(f"Selected mode: {mode}")
            
            # try ftdi with batch
            if mode == "ftdi" or mode == "auto":
                if ftdi_available:
                    self.log_debug("\nTrying FTDI adapter with batch file approach...")
                    
                    cmd = [ftdi_bat]
                    self.log_debug(f"Running batch file: {ftdi_bat}")
                    
                    CREATE_NO_WINDOW = 0x08000000
                    result = subprocess.run(
                        cmd, 
                        capture_output=True,
                        text=True,
                        creationflags=CREATE_NO_WINDOW,
                        timeout=30
                    )
                    
                    full_output = result.stdout + result.stderr
                    self.log_debug("\nFTDI Batch Output:")
                    self.log_debug(full_output)
                    
                    dna_text = self.extract_dna_from_output(full_output)
                    if dna_text:
                        self.log_debug("Successfully read DNA using FTDI adapter!")
                        return True, dna_text, None
                else:
                    self.log_debug("Skipping FTDI mode (openocd.exe not found)")
            
            # try ftdi with batch
            if (mode == "auto" and not (ftdi_available and dna_text)) or mode == "ch347":
                if ch347_available:
                    self.log_debug("\nTrying CH347 adapter with batch file approach...")
                    
                    cmd = [ch347_bat]
                    self.log_debug(f"Running batch file: {ch347_bat}")
                    
                    CREATE_NO_WINDOW = 0x08000000
                    result = subprocess.run(
                        cmd, 
                        capture_output=True,
                        text=True,
                        creationflags=CREATE_NO_WINDOW,
                        timeout=30
                    )
                    
                    full_output = result.stdout + result.stderr
                    self.log_debug("\nCH347 Batch Output:")
                    self.log_debug(full_output)
                    
                    dna_text = self.extract_dna_from_output(full_output)
                    if dna_text:
                        self.log_debug("Successfully read DNA using CH347 adapter!")
                        return True, dna_text, None
                else:
                    self.log_debug("Skipping CH347 mode (openocd-347.exe not found)")
            
            # failure sad
            error_msg = ("Failed to retrieve DNA ID. Please make sure:\n\n"
                        "1. The correct driver is installed\n"
                        "2. You are connected to the update/JTAG port on your card\n"
                        "3. Your main PC is powered on\n"
                        "4. Your USB cable is properly connected")
            self.log_debug("\nError: " + error_msg)
            return False, None, error_msg

        except Exception as e:
            error_msg = str(e)
            self.log_debug(f"\nError: {error_msg}")
            return False, None, error_msg
        
        finally:
            # cleanup temp
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                    self.log_debug(f"Removed temporary directory: {temp_dir}")
                except Exception as e:
                    self.log_debug(f"Warning: Could not clean up temp directory: {str(e)}")