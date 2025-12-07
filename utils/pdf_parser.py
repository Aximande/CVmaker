"""
Utilitaire pour extraire le texte des fichiers PDF
"""
import io
from typing import Optional


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extrait le texte d'un fichier PDF uploadé via Streamlit.
    
    Args:
        pdf_file: Fichier uploadé via st.file_uploader
        
    Returns:
        Texte extrait du PDF
    """
    text = ""
    
    try:
        # Essayer avec pdfplumber d'abord (meilleur pour les tableaux)
        import pdfplumber
        
        pdf_bytes = io.BytesIO(pdf_file.read())
        pdf_file.seek(0)  # Reset pour utilisation ultérieure
        
        with pdfplumber.open(pdf_bytes) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
                    
    except ImportError:
        # Fallback sur PyPDF2
        try:
            from PyPDF2 import PdfReader
            
            pdf_bytes = io.BytesIO(pdf_file.read())
            pdf_file.seek(0)
            
            reader = PdfReader(pdf_bytes)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
                    
        except Exception as e:
            text = f"Erreur lors de l'extraction du PDF: {str(e)}"
    
    except Exception as e:
        text = f"Erreur lors de l'extraction du PDF: {str(e)}"
    
    return text.strip()


def extract_text_from_pdf_path(pdf_path: str) -> str:
    """
    Extrait le texte d'un fichier PDF à partir de son chemin.
    
    Args:
        pdf_path: Chemin vers le fichier PDF
        
    Returns:
        Texte extrait du PDF
    """
    text = ""
    
    try:
        import pdfplumber
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
                    
    except ImportError:
        try:
            from PyPDF2 import PdfReader
            
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
                    
        except Exception as e:
            text = f"Erreur lors de l'extraction du PDF: {str(e)}"
    
    except Exception as e:
        text = f"Erreur lors de l'extraction du PDF: {str(e)}"
    
    return text.strip()

