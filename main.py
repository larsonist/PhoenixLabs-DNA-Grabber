#!/usr/bin/env python3
"""
Larsonist's DNA Grabber 
A tool for reading FPGA device DNA identifiers
"""

from core import DNAGrabber
from gui import LarsonistDNAGrabberGUI

def main():
    dna_grabber = DNAGrabber()
    
    app = LarsonistDNAGrabberGUI(dna_grabber)
    
    app.run()

if __name__ == "__main__":
    main()