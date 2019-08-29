import time, sys, os, PyPDF2, textract
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def extractPdfText(pdf_object):
    pdfFileReader = PyPDF2.PdfFileReader(pdf_object)
    totalPageNumber = pdfFileReader.numPages
    currentPageNumber = 1
    text = ''
    while(currentPageNumber < totalPageNumber ):
        pdfPage = pdfFileReader.getPage(currentPageNumber)
        text = text + pdfPage.extractText()
        currentPageNumber += 1

    if text == '':
        # If can not extract text then use ocr lib to extract the scanned pdf file.
        text = textract.process(pdf_object, method='tesseract', encoding='utf-8')

    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Facebook Auto Publisher')
    parser.add_argument('pdf', help='PDF File')
    parser.add_argument('txt', help='TXT File')

    args = parser.parse_args()    
    try:
        pdf_object = open(args.pdf, 'rb')
        txt = open(args.txt,"wb")
        txt.write(extractPdfText(pdf_object).encode("utf-8"))
        
        txt.close()
        pdf_object.close()

    except Exception as e:
        print(e)

