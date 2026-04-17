import customtkinter as ctk

class StyledButton(ctk.CTkButton):
    def __init__(self, master, text, command=None, button_type="primary", **kwargs):
        # Determine colors based on button type
        if button_type == "primary":
            fg_color = "#4CAF50"
            hover_color = "#45a049"
            text_color = "white"
        elif button_type == "secondary":
            fg_color = "#1E1E2E"
            hover_color = "#2c2c40"
            text_color = "white"
        elif button_type == "accent":
            fg_color = "#00ADB5"
            hover_color = "#008f96"
            text_color = "white"
        else:
            fg_color = "#4CAF50"
            hover_color = "#45a049"
            text_color = "white"

        super().__init__(
            master, 
            text=text,
            command=command,
            corner_radius=6, 
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color,
            font=("Segoe UI", 14, "bold"),
            **kwargs
        )

class DragDropFrame(ctk.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, fg_color="transparent", border_width=2, border_color="#4CAF50", corner_radius=10, **kwargs)
        
        self.command = command
        
        self.label = ctk.CTkLabel(
            self, 
            text="Drag and Drop your PDF here\nor Click to Browse", 
            font=("Segoe UI", 16),
            text_color="gray"
        )
        self.label.pack(expand=True, padx=20, pady=20)
        
        # We will bind standard click to open a file dialog,
        # but drag and drop events will be attached in app_ui.py
        self.bind("<Button-1>", self._on_click)
        self.label.bind("<Button-1>", self._on_click)
        
    def _on_click(self, event):
        if self.command:
            self.command()
