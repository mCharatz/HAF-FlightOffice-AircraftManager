from tkinter import N
import tabula
import pandas as pd
import PyPDF2
import csv
 
#reads table from pdf file
#df = tabula.read_pdf("fly.pdf",java_options="-Dfile.encoding=UTF8")[0]

#do that for every page and delet 4 first lines
#tabula.convert_into("fly.pdf","out.tsv",output_format="tsv", lattice=False,stream=True,pages="1")
def pilot_data_from_tsv(data):
    if ['ΕΤΟΣ'] in data:
        year = data[data.index(['ΕΤΟΣ']) + 1][0]
        unit = data[data.index(['ΜΟΝAΔΑ / ΜΟΙΡΑ']) + 1][0]
    elif ['ΜΟΝAΔΑ / ΜΟΙΡΑ', 'ΕΤΟΣ'] in data:
        year = data[data.index(['ΜΟΝAΔΑ / ΜΟΙΡΑ', 'ΕΤΟΣ']) + 1][1]
        unit = data[data.index(['ΜΟΝAΔΑ / ΜΟΙΡΑ', 'ΕΤΟΣ']) + 1][0]
    else:
        return None

    try:
        month = data[data.index(['ΜΗΝΑΣ'])+1][0]
    except:
        return None

    pilot_list = []
    for pilot in data:
        if len(pilot) != 14:
            continue
        if pilot == ['A/A', 'AMA', 'ΕΠΩΝΥΜΟ', 'ΟΝΟΜΑ', 'ΒΑΘΜΟΣ', 'ΕΙΔΙΚ', 'ΑΦΟΣ', 'ΚΥΒ/ΤΗΣ', 'ΣΥΓΚ/ΤΗΣ', 'IFR', 'ΝΥΧΤΑ', 'ΝΑΥΤΙΛΙΑ', 'ΠΛΗΡΩΜΑ', 'ΚΑΤΗΓΟΡΙΑ']:
            continue
        if pilot == ['', '', '', '', '', '', '', '', '', '', '', '', '6ΜΗΝΟ/\n18ΜΗΝΟ', '']:
            continue
        if pilot == ['', '', '', '', '', '', 'ΩΡΕΣ', 'ΩΡΕΣ', 'ΩΡΕΣ', 'ΩΡΕΣ', 'ΩΡΕΣ', 'ΩΡΕΣ', '', '']:
            continue
        if pilot == ['ΘΕΩΡΗΘΗΚΕ', '', '', '', '', '', '', '', '', '', '', '', '', '']:
            continue

        pilot_list.append(pilot)
    
    return_data = {
        'year':year,
        'month':month,
        'military_unit': unit,
        'pilots': pilot_list
    }

    return return_data
        

def trainer_data_from_tsv(data):
    trainter_list = []
    for pilot in data:
        if len(pilot) != 6:
            continue
        if pilot == ['', 'ΒΑΘΜΟΣ', 'ΕΠΩΝΥΜΟ', 'ΑΜΑ', 'Α/Φ', 'ΩΡΕΣ']:
            continue

        trainter_list.append(pilot)
    
    return_data = {
        'pilots': trainter_list
    }

    return return_data

#every page of the pdf
file = open('train.pdf', 'rb')
readpdf = PyPDF2.PdfFileReader(file)
total_pages = readpdf.numPages + 1
'''for i in range(1,total_pages):
    filename = str(i)+"_train.tsv"
    print(filename)
    print(str(i))
    tabula.convert_into("train.pdf",filename,output_format="tsv", lattice=True,stream=True,pages=str(i))'''

for i in range(1,total_pages):
    filename = str(i)+".tsv"
    tsv_file = open(filename)
    read_tsv = csv.reader(tsv_file,delimiter='\t')
    print("============================\n")
    pilot_data = pilot_data_from_tsv(list(read_tsv))
    print(pilot_data)

file2 = open('train.pdf', 'rb')
readpdf2 = PyPDF2.PdfFileReader(file2)
total_pages = readpdf2.numPages + 1


for i in range(1,total_pages):
    filename = str(i)+"_train.tsv"
    tsv_file = open(filename)
    read_tsv2 = csv.reader(tsv_file,delimiter='\t')
    print("============================\n")
    trainer_data = trainer_data_from_tsv(list(read_tsv2))
    print(trainer_data)
#then call read_tsv

#convert it to csv or take data instant



#print(df)