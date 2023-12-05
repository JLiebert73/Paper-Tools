import fitz  # PyMuPDF
import os
import shutil
import re

def extract_first_two_lines(pdf_path):
    with fitz.open(pdf_path) as doc:
        first_line = doc[0].get_text("text").split('\n')[0]
        second_line = doc[0].get_text("text").split('\n')[1]
    return first_line, second_line

def clean_filename(filename):
    # Replace or remove characters that are not allowed in Windows filenames
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    
    # Remove dashes and other special characters
    filename = re.sub(r'[^\w\s]', '', filename)
    
    # Ignore continuous strings starting with "arXiv"
    filename = re.sub(r'\barXiv[^\w\s]*', '', filename, flags=re.IGNORECASE)
    
    # Ignore continuous strings that match a date pattern (YYYY-MM-DD)
    filename = re.sub(r'\b\d{4}-\d{2}-\d{2}\b', '', filename)
    
    # Ignore numbers beyond 8 digits
    filename = re.sub(r'\b\d{9,}\b', '', filename)
    
    # Convert everything from all uppercase to only first word uppercase
    filename = filename.title()
    
    return filename

def rename_and_move_pdf(pdf_path, new_name, output_folder):
    directory, filename = os.path.split(pdf_path)
    clean_new_name = clean_filename(new_name)
    new_path = os.path.join(output_folder, clean_new_name + '.pdf')
    os.rename(pdf_path, new_path)
    return new_path

def get_paper_name(pdf_path):
    with fitz.open(pdf_path) as doc:
        first_line = doc[0].get_text("text").split('\n')[0]
        second_line = doc[0].get_text("text").split('\n')[1]
        return f"{first_line}_{second_line}"

if __name__ == "__main__":
    folder_path = 'd:\Tools\Paper_rename\data'  # Replace with the actual path to your folder
    output_folder = 'd:\Tools\Paper_rename\output'  # Replace with the desired output folder path

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)

            paper_name = get_paper_name(pdf_path)

            # Check if the paper name has less than 2 words
            if len(paper_name.split()) < 2:
                # Use the next 2 lines as names
                third_line, fourth_line = extract_first_two_lines(pdf_path)
                paper_name = f"{third_line}_{fourth_line}"

            new_pdf_path = rename_and_move_pdf(pdf_path, paper_name, output_folder)

            try:
                print(f"PDF renamed and moved to: {new_pdf_path}")
            except UnicodeEncodeError:
                # Handle encoding errors by ignoring problematic characters
                print("PDF renamed and moved. (Note: Some characters could not be displayed in the console.)")
            
            # Print the new file name
            print(f"New File Name: {os.path.basename(new_pdf_path)}")
