import time, sys, os
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
        os.rename(self.download_dir+"\\"+self.file_name,self.download_dir+"\\"+self.file_local)

        exit()

if (len(sys.argv) == 3):
    downloader(sys.argv[1], sys.argv[2])
else:
    print("python dejt.py <A/J> <0..42>")