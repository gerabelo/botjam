# 
# Geraldo Rabelo [geraldo.rabelo@gmail.com]; Ago 2019
# 
# how to use:
# python tj.py <pesquisa> <UF> <dtInicio> <dtFim>
# 

import requests, codecs, webbrowser, re, math, sys #, time

from datetime import timedelta, datetime
from requests import Session
from pymongo import MongoClient
from bs4 import BeautifulSoup

class consultaAvancada:

    session = Session()
    client = MongoClient("mongodb://localhost:27017")
    
    def __init__(self, pesquisaLivre, UF, dtInicio, dtFim):
        self.ocorrencias = 0
        if dtInicio and dtFim:
            self.dtInicio = dtInicio
            self.dtFim = dtFim
        else:
            self.dtFim = datetime.utcnow().strftime("%d/%m/%Y")
            date = datetime.utcnow()+timedelta(days=-365)
            self.dtInicio = str(date.strftime("%d/%m/%Y"))
        if pesquisaLivre and UF:
            self.UF = UF
            self.URLBASE = "https://consultasaj.tj"+UF+".jus.br"
            self.db = self.client['tj'+UF]
            self.collection = self.db['consultaAvancada']
            self.pesquisaLivre = pesquisaLivre
            self.start(self.getData(1))
        else:
            print("python tj.py <pesquisa> <UF> <dtInicio> <dtFim>")
            sys.exit()

        print('UF: ',self.UF, 'dtInicio: ', self.dtInicio,' dtFim: ',self.dtFim,' pesquisaLivre: ',self.pesquisaLivre,' ocorrencias: ',self.ocorrencias)

    def permanencia(self, data_descriptions):
            i = 0
            self.ocorrencias += len(data_descriptions)
            while (i < self.ocorrencias):
                try:
                    self.collection.insert_one({"description":data_descriptions[i],"url":data_urls[i*3],"dateCreated":datetime.utcnow().strftime("%d/%m/%Y-%H%M%S.%f")[:-3],"keywords":self.pesquisaLivre})
                except:
                    None
                i+=1

    def getData(self, pagina):
        if pagina == 1:
            page = ''
            URL = "https://consultasaj.tj"+self.UF+".jus.br/cdje/consultaAvancada.do"    
            DATA = {
                'dadosConsulta.dtInicio'        : self.dtInicio,
                'dadosConsulta.dtFim'           : self.dtFim,
                'dadosConsulta.cdCaderno'       : '-11',
                'dadosConsulta.pesquisaLivre'   : self.pesquisaLivre,
                'pagina'                        : page
            }
            # HEADERS = {
            #     'Accept'                    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            #     'Accept-Encoding'           : 'gzip, deflate, br',
            #     'Accept-Language'           : 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            #     'Cache-Control'             : 'max-age=0',
            #     'Connection'                : 'keep-alive',
            #     'Content-Length'            : '159',
            #     'Content-Type'              : 'application/x-www-form-urlencoded',
            #     'Cookie'                    : 'JSESSIONID=3A27459F6A5982C8104D0195374401F0.cdje1; _ga=GA1.3.2054290177.1564925011',
            #     'Host'                      : 'consultasaj.tjam.jus.br',
            #     'Origin'                    : 'https://consultasaj.tjam.jus.br',
            #     'Referer'                   : 'https://consultasaj.tjam.jus.br/cdje/consultaAvancada.do',
            #     'Upgrade-Insecure-Requests' : '1',
            #     'User-Agent'                : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
            # }
        else:
            page = str(pagina)
            URL = "https://consultasaj.tj"+self.UF+".jus.br/cdje/trocaDePagina.do"    
            DATA = {
                'pagina'                        : page,
                '_'                             : ''
            }
            # HEADERS = {
            #     'Accept'                    : 'text/javascript, text/html, application/xml, text/xml, */*',
            #     'Accept-Encoding'           : 'gzip, deflate, br',
            #     'Accept-Language'           : 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            #     'Connection'                : 'keep-alive',
            #     'Content-Length'            : '11',
            #     'Content-type'              : 'application/x-www-form-urlencoded; charset=UTF-8',
            #     'Cookie'                    : 'JSESSIONID=3A27459F6A5982C8104D0195374401F0.cdje1; _ga=GA1.3.2054290177.1564925011',
            #     'Host'                      : 'consultasaj.tjam.jus.br',
            #     'Origin'                    : 'https://consultasaj.tjam.jus.br',
            #     'Referer'                   : 'https://consultasaj.tjam.jus.br/cdje/consultaAvancada.do',
            #     'User-Agent'                : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            #     'X-Prototype-Version'       : '1.6.0.3',
            #     'X-Requested-With'          : 'XMLHttpRequest'
            # }
        # result = session.post(url = URL, data = DATA, headers = HEADERS)
        result = self.session.post(url = URL, data = DATA)
        return result.text

    def parsing(self, data):
        data_descriptions = []
        data_urls = []    

        soup = BeautifulSoup(data,'html.parser')

        outfile = "out\\"+datetime.utcnow().strftime("%Y%m%d-%H%M%S.%f")[:-3]+".html"
        file = codecs.open(outfile, "w", "utf-8")
        file.write(data)
        file.close()

        # webbrowser.open_new(outfile)

        for item in soup.findAll("tr", {"class": "ementaClass"}):
            for tds in item.findAll("td",recursive=False):
                for a in tds.findAll("a",recursive=False):
                    data_urls.append(self.URLBASE+a.get('onclick').replace('return popup(\'','').replace('\')',''))

        for item in soup.findAll("tr", {"class": "ementaClass2"}):
            for td in item.findAll("td",recursive=False):
                    data_descriptions.append(td.text)
                    
        self.permanencia(data_descriptions)

    def start(self, data):
        data_descriptions = []
        data_urls = []    

        soup = BeautifulSoup(data,'html.parser')

        divResultadosInferior = soup.find("div",{"id":"divResultadosInferior"})
        outfile = "out\\"+datetime.utcnow().strftime("%Y%m%d-%H%M%S.%f")[:-3]+".html"
        file = codecs.open(outfile, "w", "utf-8")
        file.write(str(divResultadosInferior))
        file.close()

        # webbrowser.open_new(outfile)

        for item in soup.findAll("tr", {"class": "ementaClass"}):
            for tds in item.findAll("td",recursive=False):
                for a in tds.findAll("a",recursive=False):
                    data_urls.append(self.URLBASE+a.get('onclick').replace('return popup(\'','').replace('\')',''))

        for item in soup.findAll("tr", {"class": "ementaClass2"}):
            for td in item.findAll("td",recursive=False):
                    data_descriptions.append(td.text)
                    
        item = soup.find("div", {"id": "divResultadosSuperior"})
        table = item.find("table",recursive=False)
        tr = table.find("tr",recursive=False)
        td = tr.find("td",recursive=False)
        numbers = re.findall(r'\d+',td.text.replace("\t","").replace("\n","").replace(" ",""))
        total_de_paginas = math.ceil(int(numbers[2])/int(numbers[1]))

        self.permanencia(data_descriptions)
        
        while (total_de_paginas > 1):
            self.parsing(self.getData(total_de_paginas))
            total_de_paginas -= 1

if (len(sys.argv) == 5):
    consultaAvancada(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
elif (len(sys.argv) == 4):
        consultaAvancada(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[3])
elif (len(sys.argv) == 3):
        consultaAvancada(sys.argv[1], sys.argv[2], '', '')
else:
    print("python tj.py <pesquisa> <UF> <dtInicio> <dtFim>")