import fitz  # PyMuPDF
from docx import Document
from bs4 import BeautifulSoup


def getText(file_path):
    file_extension = file_path.split('.')[-1].lower()

    # Extract text based on file extension
    if file_extension == 'pdf':
        text = extract_text_from_pdf(file_path)
    elif file_extension == 'docx':
        text = extract_text_from_docx(file_path)
    elif file_extension == 'html':
        text = extract_text_from_html(file_path)
    else:
        text = "Unsupported file format"

    return text


def extract_text_from_pdf(file_path):
    text = ''
    try:
        pdf_document = fitz.open(file_path)
        for page in pdf_document:
            text += page.get_text()
    except Exception as e:
        text = f"Error reading PDF: {str(e)}"
    return text


def extract_text_from_docx(file_path):
    text = ''
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text
    except Exception as e:
        text = f"Error reading DOCX: {str(e)}"
    return text


def extract_text_from_html(file_path):
    text = ''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            # Get text from the HTML content (excluding tags)
            text = soup.get_text(separator=' ', strip=True)
    except Exception as e:
        text = f"Error reading HTML: {str(e)}"
    return text





