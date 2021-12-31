import requests 
import os
from fpdf import FPDF
from bs4 import BeautifulSoup
from progress.bar import Bar
import textwrap

w = textwrap.TextWrapper(width=85)

"""Take the given [url] and search for the chapter"""
def get_base_url(url):
  chapters = []

  r = requests.get(URL, proxies={'http':'187.95.112.36'}).text
  res = BeautifulSoup(r,'html.parser')

  cap = res.find_all('li', attrs = {'class': 'chapter-item'})
  title = res.select(".novel-body > h2:nth-child(1)")

  create_folder(title[0].string)

  for i in cap :
    episode = {
              'name': i.a.string,
              'link': URL + '/' + i.a['href'].split('/')[3],
              }
    chapters.append(episode)
  
  return chapters

"""Show the download progress"""
def bar_loading(episodes):

  bar = Bar('Extracting data...', max=len(episodes))

  for index in episodes:

    get_chapters(index['link'])
    
    bar.next()

  bar.finish()
 
  
"""Take each chapter and scrap the data from the [link] """
def get_chapters(link):

  r = requests.get(link, proxies={'http':'187.95.112.36'}).text
  res = BeautifulSoup(r,'html.parser')
  cap = res.find('div', attrs = {'id': 'chapter-content'})
  
  #Doesn't work for novel in the format "-1-1"
  chapter = link.split("-")[-1]


  pdf = FPDF(format='A4')
  pdf.set_font("Times", size = 15)
  

  result = cap.findChildren("p") 

  listStr = []

  for index in result:
    if index.string is None:
      continue

    # "encode" because the data have non-latin-1 character
    # Can improve searching for a new pdf package!
    sentence = index.string.encode('latin-1', 'replace').decode('latin-1')

    sentence = '\n'.join(w.wrap(sentence))

    listStr += sentence.split('\n')
  

  pdf.add_page(orientation='P')


  for index in listStr:
    if(index == 0):
      pdf.cell(210, 10, txt = index ,ln = 0, align = 'C')
      pdf.ln()
    else:
      pdf.cell(210, 10, txt = index,ln = 0, align = 'L')
      pdf.ln()
    

  pdf.output("Chapter" + chapter +".pdf")


def create_folder(novel_name):
  path = os.getcwd()
  novel_name = novel_name.replace(" ","_")
  new_path = path + "\\" + novel_name
  try:
    os.mkdir(new_path)
    os.chdir(new_path)

    path = os.getcwd()
    print(path)
  except OSError:
    print ("Creation of the directory %s failed" % path)
    print ("OSError [%d]: %s at %s" % (OSError.errno, OSError.strerror, OSError.filename))
  else:
    print ("Successfully created the directory %s " % path)

# Main

URL = input("Digite a novel (wuxiaworld): ")

episodes = get_base_url(URL)

bar_loading(episodes)






