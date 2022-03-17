from tkinter import N
from tkinter.messagebox import NO
import tabula
import pandas as pd
import PyPDF2
import csv
import uuid


def file_extracted_data(file):
    create_tsv_files(file)
    return None,None

def create_tsv_files(file):
    custom_path = 'media/' + file.filename
    file2 = open(custom_path, 'rb')
    readpdf = PyPDF2.PdfFileReader(file2)
    total_pages = readpdf.numPages + 1
    for i in range(1,total_pages):
        filename = 'media/' + str(uuid.uuid4()) + ".tsv"
        tabula.convert_into(file2,filename,output_format="tsv", lattice=True,stream=True,pages=str(i))
    return True