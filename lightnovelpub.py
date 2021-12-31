from bs4 import BeautifulSoup
import requests
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from progress.bar import Bar 
import textwrap

w = textwrap.TextWrapper(width=85)

baseUrl = 'https://www.lightnovelpub.com'




def getBaseUrl(link):
    try:
        browser = webdriver.Firefox()
        browser.implicitly_wait(1) # seconds
        browser.get(link + '/chapters')
        
        html = browser.page_source
        
        html = BeautifulSoup(html,'html.parser')

        lst = html.select('.chapter-list > li')

        lstRes = []
        for index in lst:
            endpoint = index.findChild('a')['href']
            lstRes.append(baseUrl + endpoint)

        return lstRes

    except TimeoutException:
        print("Loading took too much time!")
    finally:
        browser.quit()


def getChapter(link,ind):
    try:
        pdf = FPDF(format='A4')
        pdf.set_font("Times", size = 15)
        
        browser = webdriver.Firefox()
        browser.implicitly_wait(1) # seconds
        browser.get(link)
    
        html = browser.page_source
    
        html = BeautifulSoup(html,'html.parser')

        html = html.find('div', {'id':'chapter-container'})

        lstStr = []

        pdf.add_page(orientation='P')

        for i in html.findChildren('p'):
            if i.string is None:
                continue
            
            sentence = i.string

            sentence = '\n'.join(w.wrap(sentence))

            lstStr += sentence.split('\n')
    

        for index in lstStr:
            index = index.encode('latin-1', 'replace').decode('latin-1')
            if(index == 0):   
                pdf.cell(210, 10, txt = index ,ln = 0, align = 'C')
                pdf.ln()
            else:
                pdf.cell(210, 10, txt = index,ln = 0, align = 'L')
                pdf.ln()
            
        pdf.output("Chapter" + str(ind) + ".pdf")

    except TimeoutException:
        print("Loading took too much time to getChapters!")
    finally:
        browser.quit()


link = input("Qual o link da novel(lightnovelpub): ")
# link = 'https://www.lightnovelpub.com/novel/i-hate-systems'

res = getBaseUrl(link)

print(type(res))
bar = Bar('Extracting data...', max=len(res))
for i in range(len(res)+1):
    getChapter(res[i],i+1)
    bar.next()

bar.finish()



    





