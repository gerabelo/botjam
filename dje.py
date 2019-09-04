import time, sys, os, PyPDF2, textract, re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class downloader:

    def __init__(self,cdCaderno,dtDiario):
        
        # self.file_name      = "Diario_"+tipo+"_"+tribunal+".pdf"
        # self.file_local     = datetime.utcnow().strftime("%Y%m%d-%H%M%S.%f")[:-3]+".pdf"
        self.file_checker   = None
        self.url            = "https://consultasaj.tjam.jus.br/cdje/downloadCaderno.do?"
        self.chrome_driver  = "C:\\chromedriver_win32\\chromedriver.exe"

        self.dtDiario       = dtDiario # datetime.utcnow().strftime("%d/%m/%Y")
        self.tpDownload     = 'D'
        self.cdCaderno      = cdCaderno#'2'

        self.download_dir   = "C:\\Users\\User\\jobs\\courtscraper\\dje\\"+datetime.utcnow().strftime("%d%m%Y")+"\\"+self.cdCaderno # for linux/*nix, download_dir="/usr/Public"
        
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

        self.driver = webdriver.Chrome(self.chrome_driver, chrome_options=self.options)

        self.driver.get(self.url+"dtDiario="+self.dtDiario+"&cdCaderno="+self.cdCaderno+"&tpDownload="+self.tpDownload)

        while (True):    
            try:
                self.file_checker = open(self.download_dir+"\\Caderno2-Judiciario-Capital.pdf", "r+")
                break
            except IOError:
                time.sleep(10)
                
        self.file_checker.close()
        self.driver.close()
        self.driver.stop_client()
        self.driver.quit()

        txtpath = ''

        try:    
            if self.cdCaderno == '2':
                pdf_object = open(self.download_dir+"\\Caderno2-Judiciario-Capital.pdf", 'rb')
                txtpath = self.download_dir+"\\Caderno2-Judiciario-Capital.txt"
            elif self.cdCaderno == '1':
                pdf_object = open(self.download_dir+"\\Caderno1-Administrativo.pdf", 'rb')
                txtpath = self.download_dir+"\\Caderno1-Administrativo.txt"
            elif self.cdCaderno == '3':
                pdf_object = open(self.download_dir+"\\Caderno3-Judiciario-Interior.pdf", 'rb')
                txtpath = self.download_dir+"\\Caderno3-Judiciario-Interior.txt"
            
            txt = open(txtpath,"wb")
            txt.write(self.extractPdfText(pdf_object).encode("utf-8"))
            
            txt.close()
            pdf_object.close()
            self.extractProcAndOAB(txtpath)

        except Exception as e:
            print(e)

if (len(sys.argv) == 3):
    downloader(sys.argv[1], sys.argv[2])
else:
    print("python dje.py <0-2> <date>")