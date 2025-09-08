import hashlib
import os
from pathlib import Path
from fastapi import UploadFile


def generate_pdf_hash(pdf: UploadFile) -> str:
    """
    Generate a unique SHA-256 hash for a PDF file that can be used as a filename.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: A unique hash string suitable for use as a filename
        
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        IOError: If there's an error reading the file
    """
    
    # Create SHA-256 hash object
    sha256_hash = hashlib.sha256()
    
    # Generate hash
    sha256_hash.update(pdf.file.read())
    
    # Return the hexadecimal representation of the hash
    return sha256_hash.hexdigest()