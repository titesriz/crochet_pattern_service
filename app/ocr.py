from io import BytesIO

import pytesseract
from PIL import Image
from fastapi import UploadFile


def image_file_to_text(file: UploadFile, lang: str = "fra+eng") -> str:
    """
    Lit un UploadFile (image) et retourne le texte OCR.
    """
    # On lit le contenu du fichier en mémoire
    content = file.file.read()
    image = Image.open(BytesIO(content))

    # Tesseract fait l'OCR sur l'image
    text = pytesseract.image_to_string(image, lang=lang)

    # Debug : afficher le texte OCR brut dans le terminal
    print("=== OCR RAW TEXT START ===")
    print(text)
    print("=== OCR RAW TEXT END ===")

    # On renvoie une version un peu nettoyée
    return text.strip()