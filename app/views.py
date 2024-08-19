from django.shortcuts import render, redirect, HttpResponse
from .forms import DocumentForm
from .models import Document
from .utils import convert_pdf_to_word, convert_pdf_to_pptx, convert_pdf_to_image, create_zip_file
import os

def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)  # Don't save to database yet
            document.save()  # Save to database to get PK
            try:
                converted_file_path = convert_pdf_to_word(document.pdf_file.path, document.pk)
                document.word_file = converted_file_path
                document.save()  # Save again with word_file updated

                pptx_file_path = convert_pdf_to_pptx(document.pdf_file.path, document.pk)
                document.pptx_file = pptx_file_path
                document.save()

                image_file_paths = convert_pdf_to_image(document.pdf_file.path, document.pk)
                filename = os.path.splitext(os.path.basename(document.pdf_file.name))[0]
                zip_file_path =  f'images/{filename}.zip'
                create_zip_file(image_file_paths, zip_file_path)
                document.image_file = zip_file_path
                document.save()

                return redirect('converted_document', pk=document.pk)
            except ValueError as e:
                # Handle the case where the converted file path is too long
                return HttpResponse(str(e), status=500)
    else:
        form = DocumentForm()
    return render(request, 'index.html', {'form': form})

def converted_document(request, pk):
    document = Document.objects.get(pk=pk)
    return render(request, 'converted_document.html', {'document': document})