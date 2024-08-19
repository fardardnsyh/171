from pdf2docx import Converter
import os
import uuid
from pdf2pptx import convert_pdf2pptx
from pdf2image import convert_from_path
import zipfile

def convert_pdf_to_word(pdf_file_path, document_pk):
    unique_id = uuid.uuid4()

    docx_filename = f"{unique_id}{document_pk}.docx"
    
    directory = 'words'
    if not os.path.exists(directory):
        os.makedirs(directory)
    docx_file_path = os.path.join(directory, docx_filename)
    cv = Converter(pdf_file_path)
    cv.convert(docx_file_path, start=0, end=None)
    cv.close()
    
    return docx_file_path

def convert_pdf_to_pptx(pdf_file_path, document_pk):
    unique_id = uuid.uuid4()
    directory = 'pptx'
    pptx_filename = f"{unique_id}{document_pk}.pptx"
    pptx_file_path = os.path.join(directory, pptx_filename)  
    os.makedirs(os.path.dirname(pptx_file_path), exist_ok=True)
    convert_pdf2pptx(pdf_file_path, pptx_file_path, resolution=300, start_page=0,page_count=None)
    return pptx_file_path 

def convert_pdf_to_image(pdf_file_path, document_pk):
    image_paths = []
    output_directory = 'images'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    images = convert_from_path(pdf_file_path, output_folder=output_directory)
    for i, image in enumerate(images):
        image_path = os.path.join(output_directory, f'page_{i+1}.jpg')
        image.save(image_path, 'JPEG')
        image_paths.append(image_path)
    return image_paths

def create_zip_file(image_paths, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for image_path in image_paths:
            zipf.write(image_path, os.path.basename(image_path))