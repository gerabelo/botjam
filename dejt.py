import time, sys, os, PyPDF2, textract
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class downloader:

    def __init__(self,tipo,tribunal):
        self.download_dir = "C:\\Users\\User\\jobs\\courtscraper\\pdf\\"+tribunal+"\\"+tipo # for linux/*nix, download_dir="/usr/Public"
        self.file_name = "Diario_"+tipo+"_"+tribunal+".pdf"
        self.file_local = datetime.utcnow().strftime("%Y%m%d-%H%M%S.%f")[:-3]+".pdf"
        self.file_checker = None
        self.url = "https://dejt.jt.jus.br/cadernos/"
        self.chrome_driver = "C:\\chromedriver_win32\\chromedriver.exe"
        
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        self.run()

    def extractProcAndOAB(self,filepath):
        with open(filepath, encoding='utf-8') as txt:
            output = open(filepath[:-4]+'-proc-oab.txt','w+')
            lines = txt.readlines()
            i = 0
            for line in lines:
                proc = re.search("(\d{7}[-]\d{2}[.]\d{4}[.]\d{1}[.]\d{2}[.]\d{4})",line)
                if proc:
                    i += 1
                    print(proc.group(0))
                    output.write(proc.group(0)+'\n')
            j = 0
            for line in lines:
                # oab = re.search("[(]\w{3}\s(\d+)\w{0,1}[/]\w{2}[)]",line)
                oab = re.search("[O][A][B]\s(\d+)\w{0,1}[/]\w{2}",line)
                
                if oab:
                    j += 1
                    print(oab.group(0))
                    output.write(oab.group(0)[4:]+'\n')
            print(i,' ',j)
            output.close()

    def extractPdfText(self,pdf_object):
        print("pdf_object: ",pdf_object)
        pdfFileReader = PyPDF2.PdfFileReader(pdf_object)
        totalPageNumber = pdfFileReader.numPages
        print('This pdf file contains totally ' + str(totalPageNumber) + ' pages.')
        currentPageNumber = 1
        text = ''
        while(currentPageNumber < totalPageNumber ):
            pdfPage = pdfFileReader.getPage(currentPageNumber)
            text = text + pdfPage.extractText()
            currentPageNumber += 1

        if text == '':
            # If can not extract text then use ocr lib to extract the scanned pdf file.
            text = textract.process(pdf_object, method='tesseract', encoding='utf-8')
        # print('text: ',text)
        return text

    def run(self):
        self.options = webdriver.ChromeOptions()

        self.profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
               "download.default_directory": self.download_dir , "download.extensions_to_open": "applications/pdf"}

        self.options.add_experimental_option("prefs", self.profile)

        self.driver = webdriver.Chrome(self.chrome_driver, chrome_options=self.options)  # Optional argument, if not specified will search path.

        self.driver.get(self.url+self.file_name)

        while (True):    
            try:
                self.file_checker = open(self.download_dir+"\\"+self.file_name, "r+") # or "a+", whatever you need
                break
            except IOError:
                time.sleep(10)
                
        self.file_checker.close()
        self.driver.close()
        self.driver.stop_client()
        self.driver.quit()

        try:
        # pdf_object = open(self.download_dir+"\\"+self.file_name, 'rb') # fileObject = open("C:\\Users\\User\\jobs\\courtscraper\\pdf\\24\A\\test.pdf", 'rb')        
        # txt = open(self.download_dir+"\\"+self.file_name+".txt","w+")
        # txt.write(self.extractPdfText(pdf_object)) #print(self.extractPdfText(self.download_dir+"\\"+self.file_name))
        # pdf_object.close()
        # txt.close()
            
            pdf_object = open(self.download_dir+"\\"+self.file_name, 'rb') # fileObject = open("C:\\Users\\User\\jobs\\courtscraper\\pdf\\24\A\\test.pdf", 'rb')        
            txt = open(self.download_dir+"\\"+self.file_name+".txt","wb")
            txt.write(self.extractPdfText(pdf_object).encode("utf-8")) #print(self.extractPdfText(self.download_dir+"\\"+self.file_name))
            
            txt.close()
            pdf_object.close()
            self.extractProcAndOAB(txtpath)

            os.rename(self.download_dir+"\\"+self.file_name,self.download_dir+"\\"+self.file_local)
            os.rename(self.download_dir+"\\"+self.file_name+".txt",self.download_dir+"\\"+self.file_local+".txt")

        # raw = parser.from_file(self.download_dir+"\\"+self.file_local)
        except Exception as e:
            print(e)

if (len(sys.argv) == 3):
    downloader(sys.argv[1], sys.argv[2])
else:
    print("python dejt.py <A/J> <0..42>")