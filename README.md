# SecurePDF

**Advanced PDF Protection & Security Tool**

SecurePDF is a fully functional, production-ready desktop tool that empowers individuals and enterprises to secure sensitive PDF files. Whether it's college assignments, confidential company records, or personal documents, SecurePDF ensures that unauthorized users cannot open your files.

## Features

- **Encrypt PDFs**: Lock your PDFs with a secure password.
- **Decrypt PDFs**: Unlock previously secured PDFs.
- **Drag & Drop**: Modern drag-and-drop interface.
- **Password Strength Analyzer**: Live evaluation to ensure you use strong passwords.
- **Password Generator**: One-click to generate a strong password algorithmically.
- **Dark & Light Mode**: Modern UI built with CustomTkinter that respects your system theme.

## Tech Stack

- Python 3.8+
- `customtkinter` (Modern UI/UX)
- `pypdf` (Fast and reliable PDF processing)
- `tkinterdnd2` (Native OS file drag & drop)

## Prerequisites & Installation

### 1. Setup Virtual Environment (Recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
*Note: If `tkinterdnd2` fails to install or work on your specific OS, the app will gracefully fall back to a standard "Click to Browse" alternative while still looking great.*

## Usage

Run the program from the terminal:
```bash
python main.py
```

1. Select **Encrypt** or **Decrypt** using the top tab.
2. **Drag & Drop** your PDF directly into the application window.
3. Provide a password (or optionally generate a secure one).
4. Click **Encrypt & Save PDF** or **Decrypt & Save PDF**.
5. You'll be prompted where to save the resulted secure or unlocked file.

## Performance & Security Notes
- The encryption logic uses `pypdf` which supports robust 128-bit/256-bit AES encryption.
- Passwords are only temporarily stored in the memory to perform the operation and are never cached to disk.
- Execution errors and file access bugs are logged gracefully inside the `logs/app.log` file.

## Deployment / Building an `.exe`

You can compile this project into a standalone executable using [PyInstaller](https://pyinstaller.org/).
```bash
pip install pyinstaller
pyinstaller --noconfirm --windowed --name "SecurePDF" main.py
```

## Future Improvements
- Batch file processing in a single drag-and-drop operation.
- Google Drive cloud syncing.
- Support for protecting text extractions while allowing printing.

## Contributions
Pull requests are welcome!
