import sys
import customtkinter as ctk

# Attempt to load TkinterDnD wrapper for drag-and-drop support
try:
    from tkinterdnd2 import TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False

from ui.app_ui import AppUI
from utils.logger import logger

# Set the appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class SecurePDFApplication(ctk.CTk if not HAS_DND else TkinterDnD.Tk):
    """
    Main application root. 
    It conditionally inherits from TkinterDnD.Tk to allow native drag and drop if installed.
    """
    def __init__(self):
        super().__init__()
        
        if HAS_DND:
            # Re-initialize basic aspects of custom tkinter since TkinterDnD replaces standard Tk
            self.config(background=ctk.ThemeManager.theme["CTk"]["fg_color"][0])
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            
        self.title("SecurePDF – Advanced PDF Protection Tool")
        self.geometry("700x550")
        self.minsize(600, 500)
        
        logger.info("Starting SecurePDF application")

        # Top Navigation / Utility frame (Dark mode toggle)
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self.nav_frame.pack(side="top", fill="x", padx=10, pady=5)
        
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.nav_frame, 
            values=["System", "Dark", "Light"],
            command=self.change_appearance_mode_event,
            width=100
        )
        self.appearance_mode_menu.pack(side="right", padx=10)
        
        # Main App UI frame
        self.main_app = AppUI(self)
        self.main_app.pack(fill="both", expand=True, padx=10, pady=10)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        logger.info(f"Appearance mode changed to: {new_appearance_mode}")

if __name__ == "__main__":
    app = SecurePDFApplication()
    app.mainloop()
