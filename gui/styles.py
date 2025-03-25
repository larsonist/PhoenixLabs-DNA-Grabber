"""
styles
"""

from tkinter import ttk

class GUIStyles:
    def __init__(self, ui_font, mono_font):
        self.ui_font = ui_font
        self.mono_font = mono_font
        
        self.colors = {
            'bg_dark': '#1E1E1E',
            'bg_darker': '#141414',
            'bg_lighter': '#2C2C2E',
            'bg_card': '#2C2C2E',
            'accent_blue': '#0A84FF',
            'accent_light': '#4CA2FF',
            'accent_dark': '#0066CC',
            'text_primary': '#FFFFFF',
            'text_secondary': '#EBEBF5',
            'text_muted': '#8E8E93',
            'success_green': '#30D158',
            'error_red': '#FF453A',
            'warning_amber': '#FFD60A',
            'border': '#3A3A3C'
        }
    
    def apply_styles(self):
        style = ttk.Style()
        
        style.configure('Main.TFrame', 
                       background=self.colors['bg_dark'])
        
        style.configure('Title.TLabel',
                       font=(self.ui_font, 20, 'bold'),
                       background=self.colors['bg_dark'],
                       foreground=self.colors['text_primary'])
        
        style.configure('Subtitle.TLabel',
                       font=(self.ui_font, 12),
                       background=self.colors['bg_dark'],
                       foreground=self.colors['text_secondary'])
        
        style.configure('Card.TFrame', 
                       background=self.colors['bg_card'])
        
        style.configure('CardInner.TFrame', 
                       background=self.colors['bg_card'])
        
        style.configure('CardTitle.TLabel',
                       font=(self.ui_font, 13, 'bold'),
                       background=self.colors['bg_card'],
                       foreground=self.colors['accent_blue'])
        
        style.configure('DNAContent.TFrame',
                       background=self.colors['bg_card'])
        
        style.configure('DNA.TLabel',
                       font=(self.mono_font, 14),
                       background=self.colors['bg_card'],
                       foreground=self.colors['text_primary'])
        
        style.configure('Status.TFrame',
                       background=self.colors['bg_card'])
        
        style.configure('Status.TLabel',
                       font=(self.ui_font, 11),
                       background=self.colors['bg_card'],
                       foreground=self.colors['text_muted'])
        
        style.configure('SectionTitle.TLabel',
                       font=(self.ui_font, 12, 'bold'),
                       background=self.colors['bg_dark'],
                       foreground=self.colors['text_secondary'])
        
        style.configure('RadioFrame.TFrame',
                       background=self.colors['bg_dark'])
        
        style.configure('Mode.TRadiobutton',
                       font=(self.ui_font, 11),
                       background=self.colors['bg_dark'],
                       foreground=self.colors['text_primary'])
        
        style.map('Mode.TRadiobutton',
                 background=[('selected', self.colors['bg_dark'])],
                 foreground=[('selected', self.colors['text_primary'])])
        
        style.configure('Custom.Vertical.TScrollbar',
                       background=self.colors['bg_card'],
                       troughcolor=self.colors['bg_darker'],
                       borderwidth=0,
                       arrowsize=12)
        
        style.configure('Footer.TLabel',
                       font=(self.ui_font, 9),
                       background=self.colors['bg_dark'],
                       foreground=self.colors['text_muted'])