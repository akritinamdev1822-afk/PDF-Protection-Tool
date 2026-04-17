import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading

from utils.pdf_handler import encrypt_pdf, decrypt_pdf
from utils.password_utils import check_password_strength, generate_strong_password
from utils.file_utils import get_file_size, is_valid_pdf
from utils.logger import logger
from ui.components import StyledButton, DragDropFrame

try:
    from tkinterdnd2 import DND_FILES
    HAS_DND = True
except ImportError:
    HAS_DND = False
    logger.warning("tkinterdnd2 is not installed or configured correctly. Drag and drop will be disabled.")


class AppUI(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.selected_file_path = None
        
        self.setup_layout()

    def setup_layout(self):
        # Grid layout configuration
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header_label = ctk.CTkLabel(self, text="SecurePDF – Advanced PDF Security", font=("Segoe UI", 24, "bold"))
        self.header_label.grid(row=0, column=0, pady=(20, 10), padx=20)

        # Main Tabview using CustomTkinter
        self.tabview = ctk.CTkTabview(self, width=600, height=400)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.tabview.add("Encrypt")
        self.tabview.add("Decrypt")
        
        self.setup_encrypt_tab(self.tabview.tab("Encrypt"))
        self.setup_decrypt_tab(self.tabview.tab("Decrypt"))

        # Progress / Status area
        self.status_label = ctk.CTkLabel(self, text="Status: Ready", font=("Segoe UI", 12), text_color="gray")
        self.status_label.grid(row=2, column=0, pady=(10, 5))
        
        self.progressbar = ctk.CTkProgressBar(self, width=400, fg_color="#1E1E2E", progress_color="#4CAF50")
        self.progressbar.grid(row=3, column=0, pady=(0, 20))
        self.progressbar.set(0)

    def setup_encrypt_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        
        # Drag & Drop Zone
        self.enc_drag_frame = DragDropFrame(tab, command=lambda: self.browse_file("encrypt"))
        self.enc_drag_frame.grid(row=0, column=0, padx=20, pady=15, sticky="ew")
        
        # File info
        self.enc_file_info = ctk.CTkLabel(tab, text="No file selected", font=("Segoe UI", 12))
        self.enc_file_info.grid(row=1, column=0, pady=(0, 15))
        
        # Attach TkinterDnD event if available
        if HAS_DND:
            self.enc_drag_frame.drop_target_register(DND_FILES)
            self.enc_drag_frame.dnd_bind('<<Drop>>', lambda e: self.on_drop(e, "encrypt"))

        # Password Input Frame
        pwd_frame = ctk.CTkFrame(tab, fg_color="transparent")
        pwd_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        pwd_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(pwd_frame, text="Password:", font=("Segoe UI", 14)).grid(row=0, column=0, padx=(0, 10))
        self.enc_pwd_var = ctk.StringVar()
        self.enc_pwd_var.trace_add("write", self.update_pwd_strength)
        
        self.enc_pwd_entry = ctk.CTkEntry(pwd_frame, textvariable=self.enc_pwd_var, show="*", width=200)
        self.enc_pwd_entry.grid(row=0, column=1, sticky="w")
        
        self.pwd_strength_label = ctk.CTkLabel(pwd_frame, text="", font=("Segoe UI", 12))
        self.pwd_strength_label.grid(row=0, column=2, padx=10)

        gen_btn = StyledButton(pwd_frame, text="Generate", width=80, button_type="accent", command=self.auto_generate_password)
        gen_btn.grid(row=0, column=3, padx=10)

        # Action Button
        action_btn = StyledButton(tab, text="Encrypt & Save PDF", button_type="primary", command=self.process_encryption)
        action_btn.grid(row=3, column=0, pady=20)

    def setup_decrypt_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        
        # Drag & Drop Zone
        self.dec_drag_frame = DragDropFrame(tab, command=lambda: self.browse_file("decrypt"))
        self.dec_drag_frame.grid(row=0, column=0, padx=20, pady=15, sticky="ew")
        
        # File info
        self.dec_file_info = ctk.CTkLabel(tab, text="No file selected", font=("Segoe UI", 12))
        self.dec_file_info.grid(row=1, column=0, pady=(0, 15))

        if HAS_DND:
            self.dec_drag_frame.drop_target_register(DND_FILES)
            self.dec_drag_frame.dnd_bind('<<Drop>>', lambda e: self.on_drop(e, "decrypt"))

        # Password Input Frame
        pwd_frame = ctk.CTkFrame(tab, fg_color="transparent")
        pwd_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        pwd_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(pwd_frame, text="Password:", font=("Segoe UI", 14)).grid(row=0, column=0, padx=(0, 10))
        self.dec_pwd_var = ctk.StringVar()
        self.dec_pwd_entry = ctk.CTkEntry(pwd_frame, textvariable=self.dec_pwd_var, show="*", width=200)
        self.dec_pwd_entry.grid(row=0, column=1, sticky="w")

        # Action Button
        action_btn = StyledButton(tab, text="Decrypt & Save PDF", button_type="secondary", command=self.process_decryption)
        action_btn.grid(row=3, column=0, pady=20)

    def browse_file(self, mode):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.set_file(file_path, mode)

    def on_drop(self, event, mode):
        # TkinterDnD returns paths inside curly braces if they contain spaces
        file_path = event.data.strip('{}')
        self.set_file(file_path, mode)

    def set_file(self, file_path, mode):
        if not is_valid_pdf(file_path):
            messagebox.showerror("Invalid File", "Please select a valid PDF file.")
            return

        self.selected_file_path = file_path
        size_str = get_file_size(file_path)
        basename = os.path.basename(file_path)
        info_text = f"File: {basename} ({size_str})"
        
        if mode == "encrypt":
            self.enc_file_info.configure(text=info_text)
            self.status_label.configure(text=f"Status: Ready to encrypt {basename}")
        else:
            self.dec_file_info.configure(text=info_text)
            self.status_label.configure(text=f"Status: Ready to decrypt {basename}")

    def update_pwd_strength(self, *args):
        pwd = self.enc_pwd_var.get()
        strength, color = check_password_strength(pwd)
        if strength == "Empty":
            self.pwd_strength_label.configure(text="", text_color="gray")
        else:
            self.pwd_strength_label.configure(text=strength, text_color=color)

    def auto_generate_password(self):
        pwd = generate_strong_password()
        self.enc_pwd_var.set(pwd)
        self.enc_pwd_entry.configure(show="") # Briefly show the generated password
        self.master.after(3000, lambda: self.enc_pwd_entry.configure(show="*"))
        
    def process_encryption(self):
        if not self.selected_file_path:
            messagebox.showwarning("Missing File", "Please select a PDF file first.")
            return
            
        password = self.enc_pwd_var.get()
        if not password:
            messagebox.showwarning("Missing Password", "Please enter a password.")
            return
            
        strength, _ = check_password_strength(password)
        if strength == "Weak":
            if not messagebox.askyesno("Weak Password", "Password is weak. Do you want to continue anyway?"):
                return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", 
            initialfile=f"secured_{os.path.basename(self.selected_file_path)}",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not output_path:
            return

        self.run_task(encrypt_pdf, self.selected_file_path, output_path, password, "Encryption")

    def process_decryption(self):
        if not self.selected_file_path:
            messagebox.showwarning("Missing File", "Please select a PDF file first.")
            return
            
        password = self.dec_pwd_var.get()
        if not password:
            messagebox.showwarning("Missing Password", "Please enter the password to decrypt.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", 
            initialfile=f"unlocked_{os.path.basename(self.selected_file_path)}",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not output_path:
            return

        self.run_task(decrypt_pdf, self.selected_file_path, output_path, password, "Decryption")

    def run_task(self, func, input_path, output_path, password, action_name):
        self.progressbar.start()
        self.status_label.configure(text=f"Status: Processing {action_name}...")
        
        def task():
            success, message = func(input_path, output_path, password)
            self.progressbar.stop()
            self.progressbar.set(0)
            
            if success:
                self.status_label.configure(text=f"Status: {action_name} Successful!")
                messagebox.showinfo("Success", message)
            else:
                self.status_label.configure(text=f"Status: {action_name} Failed!")
                messagebox.showerror("Error", message)

        threading.Thread(target=task, daemon=True).start()
