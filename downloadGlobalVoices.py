import sys
import os
import shutil
import urllib.request
from bs4 import BeautifulSoup
import codecs

def monthToStr(month):
    month=int(month)
    if month<10:
        strMonth="0"+str(month)
    else:
        strMonth=str(month)
    return(strMonth)

def getAllLinks(year,month,lang):
    if not lang=="en":
        url="https://"+lang+".globalvoices.org/"+str(year)+"/"+monthToStr(month)
    else:
        url="https://globalvoices.org/"+str(year)+"/"+monthToStr(month)
    all_links=[]
    print("URL",url)

    f = urllib.request.urlopen(url)
    web=f.read().decode('utf-8')

    soup = BeautifulSoup(web, 'lxml')

    links = soup.find_all('a')
    for link in links:
        link=link['href'] 
        if link.startswith(url):
            text=[]
            camps=link.split("/")
            if len(camps)>5:
                all_links.append(link)
    cont=1            
    while 1:
        cont+=1
        url2=url+"/page/"+str(cont)+"/"
        try:
            f = urllib.request.urlopen(url2)
            web=f.read().decode('utf-8')
            soup = BeautifulSoup(web, 'lxml')
            links = soup.find_all('a')
            good_links=[]
            for link in links:
                link=link['href'] 
                if link.startswith(url):
                    camps=link.split("/")
                    if len(camps)>6 and not link==url2:
                        good_links.append(link)
            if len(good_links)==0:
                break
            all_links.extend(good_links)
        except:
            break
    all_links = list(set(all_links))
    
    return(all_links)
    
def getPageText(link):
    text=[]
    
    f = urllib.request.urlopen(link)
    web=f.read()
    soup = BeautifulSoup(web, 'lxml')        
    title = soup.find_all('title')[0]
    if not title==None:
        title=title.getText()
        text.append(title)
        
    divs=soup.findAll("div", {"class" : "postmeta post-tagline"})
    for div in divs:
        subtitle=div.getText()
        text.append(subtitle)
        
    entries=soup.findAll("div", {"class" : "entry"})
    for entry in entries:
        soup3 = BeautifulSoup(str(entry), 'lxml')
        paras=soup3.find_all("p")
        for para in paras:
            try:
                para=para.getText()
                text.append(para)
            except:
                print("ERROR",sys.exc_info())
    return(text)

year=sys.argv[1]
months=sys.argv[2]
#all, 1:2:3, 1-3
lang1=sys.argv[3]
lang2=sys.argv[4]

#if one of the languages is English, it should be lang2
if lang1=="en":
    lang1=lang2
    lang2="en"

#creating the directories for each language
directory1=str(year)+"-"+lang1
directory2=str(year)+"-"+lang2

if os.path.exists(directory1) and os.path.isdir(directory1):
    shutil.rmtree(directory1)
os.mkdir(directory1)

if os.path.exists(directory2) and os.path.isdir(directory2):
    shutil.rmtree(directory2)
os.mkdir(directory2)

#creating the list of months
monthlist=[]
if months.lower()=="all":
    monthlist=[1,2,3,4,5,6,7,8,9,10,11,12]
elif months.find("-")>-1:
    monthlist=list(range(int(months.split("-")[0]),int(months.split("-")[1])+1))
elif months.find(":")>-1:
    monthlist=months.split(":")
else:
    monthlist=[int(months)]
allLinksL1=[]

for month in monthlist:
    year=int(year)
    mont=int(month)
    try:
        links=getAllLinks(year,month,lang1)
    
        allLinksL1.extend(links)
    except:
        pass

for link in allLinksL1:
    print(link)
    camps=link.split("/")
    filenameL1=camps[-2]+".txt"
    filenameL2=camps[-2]+".txt"

    filename=os.path.join(".", directory1, filenameL1)
    output=codecs.open(filename,"w",encoding="utf-8")

    f = urllib.request.urlopen(link)
    web=f.read()
    soup = BeautifulSoup(web, 'lxml')

    text=getPageText(link)
    for s in text:
        output.write(s+"\n")
    output.close()
    try:
        spanL2=soup.findAll("span", {"class" : "translation-language post-translation-"+lang2})
        soup2 = BeautifulSoup(str(spanL2),'lxml')
        linkL2=soup2.find_all("a")[0]['href'] 
        
        filename=os.path.join(".", directory2, filenameL2)
        output=codecs.open(filename,"w",encoding="utf-8")
        
        text=getPageText(linkL2)
        for s in text:
            output.write(s+"\n")
        output.close()
    except:
        pass
    

    
