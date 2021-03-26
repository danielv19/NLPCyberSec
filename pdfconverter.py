import os
#might have to “pip install [import]” if wordninja, PyPDF2, and other below aren’t downloaded
import os
import wordninja
import PyPDF2
from pathlib import Path
import textract
from pikepdf import Pdf
import slate3k as slate

#input_folder has all the original oig pdfs
input_folder = "C:/Users/daniel/Documents/oig_reports/"
#decrypt_folder has all the decrypted copies of encrypted oig reports
decrypt_folder = "C:/Users/daniel/jupyter/decrypted_files/"
#text_folder has all the txt versions of oig pdf
text_folder = "C:/Users/daniel/jupyter/text/"

#for every file in the folder of oig pdfs
for filename in os.listdir(input_folder):
    pdf = open(input_folder+filename,'rb')
    #outputing a txt file with the same filename as the pdf
    output = text_folder + filename[0:len(filename)-4] + ".txt"
        
     file = input_folder + filename

    pdfReader = PyPDF2.PdfFileReader(pdf)
    #if the pdf is encrypted, use Pdf from pikepdf to make a
    #decrypted version and output it into decrypt_folder
    if pdfReader.isEncrypted:
        pdf2 = Pdf.open(pdf)
        pdf2.save(decrypt_folder + filename)
        pdf.close()
        #stop reading the encrypted pdf and start reading the new decrypted pdf
        pdf = open(decrypt_folder+filename,'rb')
        pdfReader = PyPDF2.PdfFileReader(pdf)
        file = decrypt_folder + filename

#open output text file to write
text = open(output, "a", encoding='utf-8')
    #open and read file with slate, more accurate
    try:
        with open(file,'rb') as f:
            extracted_text = slate.PDF(f)
            for word in extracted_text:
                text.write(word)
       #however if slate fails, throw exception to go to original method
        if (Path(output).stat().st_size < 1000):
            raise Exception("no text")
    except:
        #access every page to copy text
        for i in range(pdfReader.getNumPages()):
            page = pdfReader.getPage(i)
	#first we try to extract text from the page
            try:
                textPage = page.extractText()
    #wordninja used to infer spaces in word block text
                words = wordninja.split(textPage)
                for word in words:
                    text.write(f"{word} ")
	#extractText() returns blank / gives an error when a blank page is returned\
            #thus, we increment to skip the bank page
            except:
                i += 1
    text.close()
