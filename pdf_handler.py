from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError
import os
from .logger import logger

def encrypt_pdf(input_path, output_path, password):
    """
    Encrypts a PDF file using pypdf.
    Returns: (success_boolean, status_message)
    """
    try:
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            logger.warning(f"File {input_path} is already encrypted.")
            return False, "File is already encrypted."
            
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
            
        writer.encrypt(password)
        
        with open(output_path, "wb") as f:
            writer.write(f)
            
        logger.info(f"Successfully encrypted {input_path} -> {output_path}")
        return True, "Encryption successful!"
    except PdfReadError:
        logger.error(f"Cannot read PDF {input_path}. File might be corrupted.")
        return False, "Corrupted or invalid PDF file."
    except Exception as e:
        logger.error(f"Failed to encrypt {input_path}: {str(e)}")
        return False, f"Encryption failed: {str(e)}"

def decrypt_pdf(input_path, output_path, password):
    """
    Decrypts an encrypted PDF file using pypdf.
    Returns: (success_boolean, status_message)
    """
    try:
        reader = PdfReader(input_path)
        if not reader.is_encrypted:
            logger.warning(f"File {input_path} is not encrypted.")
            return False, "File is not encrypted."
            
        decrypt_result = reader.decrypt(password)
        
        # pypdf decrypt() behavior evaluation depending on version
        # It returns an enumeration PasswordType if successful (usually > 0)
        if hasattr(decrypt_result, "value"):
            is_valid = decrypt_result.value != 0
        else:
            is_valid = decrypt_result != 0
            
        if not is_valid:
            logger.warning("Incorrect password provided for decryption.")
            return False, "Incorrect password."
            
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
            
        with open(output_path, "wb") as f:
            writer.write(f)
            
        logger.info(f"Successfully decrypted {input_path} -> {output_path}")
        return True, "Decryption successful!"
    except Exception as e:
        logger.error(f"Failed to decrypt {input_path}: {str(e)}")
        return False, f"Decryption failed: {str(e)}"
