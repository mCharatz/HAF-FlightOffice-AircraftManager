from tkinter import N
from tkinter.messagebox import NO
import tabula
import pandas as pd
import PyPDF2
import csv
import uuid
import logging

def create_tsv_files(file):
    logger = logging.getLogger("mylogger")
    filename = 'media/' + str(uuid.uuid4()) + ".tsv"
    tabula.convert_into(file.file,filename,output_format="tsv", lattice=True,stream=True,pages="all")
    tsv_file = open(filename)
    read_tsv = csv.reader(tsv_file,delimiter='\t')
    multi_list = proccess_tsv_file(list(read_tsv))
    r = extract_data_from_multi_list(multi_list)
    logger.info(r)
    return r

def proccess_tsv_file(data):
    logger = logging.getLogger("mylogger")
    start_tables_indexes = []
    for index, elem in enumerate(data):
        if ['ΜΟΝAΔΑ / ΜΟΙΡΑ', 'ΕΤΟΣ'] == elem:
            start_tables_indexes.append(index)
        elif ['ΜΟΝAΔΑ / ΜΟΙΡΑ'] == elem:
            start_tables_indexes.append(index)
    start_tables_indexes.append(len(data))
    multi_list = [data[start_tables_indexes[i]:start_tables_indexes[i+1]] for i in range(len(start_tables_indexes)-1)]
    return multi_list

def extract_data_from_multi_list(multi_list):
    multi_return_data = []
    for table in multi_list:
        if ['ΕΤΟΣ'] in table:
            year = table[table.index(['ΕΤΟΣ']) + 1][0]
            unit = table[table.index(['ΜΟΝAΔΑ / ΜΟΙΡΑ']) + 1][0]
        elif ['ΜΟΝAΔΑ / ΜΟΙΡΑ', 'ΕΤΟΣ'] in table:
            year = table[table.index(['ΜΟΝAΔΑ / ΜΟΙΡΑ', 'ΕΤΟΣ']) + 1][1]
            unit = table[table.index(['ΜΟΝAΔΑ / ΜΟΙΡΑ', 'ΕΤΟΣ']) + 1][0]
        else:
            return None

        try:
            month = table[table.index(['ΜΗΝΑΣ'])+1][0]
        except:
            return None

        pilot_list = []
        for pilot in table:
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

        multi_return_data.append(return_data)

    return multi_return_data