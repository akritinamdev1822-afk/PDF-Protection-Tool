import os

def get_file_size(file_path):
    """Returns a nicely formatted string representing the file size."""
    try:
        size_bytes = os.path.getsize(file_path)
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
    except FileNotFoundError:
        return "Unknown Size"

def is_valid_pdf(file_path):
    """Checks if the file has a .pdf extension and exists on the filesystem."""
    return file_path.lower().endswith('.pdf') and os.path.isfile(file_path)
