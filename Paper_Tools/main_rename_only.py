import os
import spacy
import fitz  # PyMuPDF
from summarizer import Summarizer

# Load the English language model from spaCy
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    return text

def extract_information_from_text(text):
    # Use spaCy for NLP tasks, extract relevant information from the text
    # You can customize this part based on what information you want to extract
    doc = nlp(text)

    # Extract the first few words as the filename
    filename_info = " ".join([token.text for token in doc[:5]]) if len(doc) >= 5 else "untitled_document"

    return filename_info

def clean_filename(filename):
    # Remove or replace invalid characters for filenames
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def save_renamed_pdf(pdf_path, new_text, output_folder):
    # Clean the filename to make it Windows-compatible
    cleaned_filename = clean_filename(new_text)

    # Create a new PDF with the updated text
    new_pdf_path = os.path.join(output_folder, f"{cleaned_filename}.pdf")

    # Write the updated text to the new PDF
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((10, 10), new_text)
    doc.save(new_pdf_path)

    return new_pdf_path

def generate_summary(text):
    # Use BERT extractive summarizer
    summarizer = Summarizer()
    summary = summarizer(text)
    return summary

def save_summary_to_file(summary, output_folder, filename):
    # Save the summary to a text file
    summary_file_path = os.path.join(output_folder, f"{filename}_summary.txt")
    with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
        summary_file.write(summary)
    return summary_file_path

def process_pdf_folder(folder_path, output_folder):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)

            # Extract text from PDF
            text = extract_text_from_pdf(pdf_path)

            # Extract relevant information from the text
            extracted_info = extract_information_from_text(text)

            # Save the renamed PDF to a new file
            new_pdf_path = save_renamed_pdf(pdf_path, extracted_info, output_folder)
            print(f"Created new file: {new_pdf_path}")

            # Generate a summary of the document text
            summary = generate_summary(text)

            # Save the summary to a file
            summary_file_path = save_summary_to_file(summary, output_folder, extracted_info)
            print(f"Created summary file: {summary_file_path}")

# Replace 'd:\Tools\Paper_rename\data' with the actual path to your PDF folder
pdf_folder_path = 'd:\Tools\Paper_rename\data'
# Replace 'output_folder' with the folder where you want to save the new PDFs and summaries
output_folder_path = 'd:\Tools\Paper_rename\output_summary'
process_pdf_folder(pdf_folder_path, output_folder_path)
