import sys
import os
import shutil
import urllib.request
from bs4 import BeautifulSoup
import codecs
import tkinter as tk

# Helper functions
def monthToStr(month):
    month = int(month)
    return f"{month:02}"

def getAllLinks(year, month, lang):
    if lang != "en":
        url = f"https://{lang}.globalvoices.org/{year}/{monthToStr(month)}"
    else:
        url = f"https://globalvoices.org/{year}/{monthToStr(month)}"
    all_links = []

    try:
        f = urllib.request.urlopen(url)
        web = f.read().decode('utf-8')
        soup = BeautifulSoup(web, 'lxml')

        links = soup.find_all('a')
        for link in links:
            link = link['href']
            if link.startswith(url):
                camps = link.split("/")
                if len(camps) > 3:
                    all_links.append(link)

        cont = 1
        while True:
            cont += 1
            url2 = f"{url}/page/{cont}/"
            f = urllib.request.urlopen(url2)
            web = f.read().decode('utf-8')
            soup = BeautifulSoup(web, 'lxml')
            links = soup.find_all('a')
            good_links = []
            for link in links:
                link = link['href']
                if link.startswith(url):
                    camps = link.split("/")
                    if len(camps) > 3 and link != url2:
                        good_links.append(link)
            if not good_links:
                break
            all_links.extend(good_links)
    except Exception as e:
        print(f"Error fetching links: {e}")

    return list(set(all_links))

def getPageText(link):
    text = []
    try:
        f = urllib.request.urlopen(link)
        web = f.read()
        soup = BeautifulSoup(web, 'lxml')

        title = soup.find('title')
        if title:
            text.append(title.getText())

        divs = soup.find_all("div", {"class": "postmeta post-tagline"})
        for div in divs:
            subtitle = div.getText()
            text.append(subtitle)

        entries = soup.find_all("div", {"class": "entry"})
        for entry in entries:
            paras = BeautifulSoup(str(entry), 'lxml').find_all("p")
            for para in paras:
                text.append(para.getText())
    except Exception as e:
        print(f"Error fetching page text: {e}")
    return text

def run_program():
    year = year_entry.get()
    months = months_entry.get()
    lang1 = lang1_entry.get()
    lang2 = lang2_entry.get()

    if lang1 == "en":
        lang1, lang2 = lang2, "en"

    directory1 = f"{year}-{lang1}"
    directory2 = f"{year}-{lang2}"

    if os.path.exists(directory1) and os.path.isdir(directory1):
        shutil.rmtree(directory1)
    os.mkdir(directory1)

    if os.path.exists(directory2) and os.path.isdir(directory2):
        shutil.rmtree(directory2)
    os.mkdir(directory2)

    monthlist = []
    if months.lower() == "all":
        monthlist = list(range(1, 13))
    elif "-" in months:
        start, end = map(int, months.split("-"))
        monthlist = list(range(start, end + 1))
    elif ":" in months:
        monthlist = list(map(int, months.split(":")))
    else:
        monthlist = [int(months)]

    allLinksL1 = []
    for month in monthlist:
        try:
            links = getAllLinks(year, month, lang1)
            allLinksL1.extend(links)
        except Exception as e:
            print(f"Error processing month {month}: {e}")

    for link in allLinksL1:
        print(f"Processing link: {link}")
        camps = link.split("/")
        if not camps[-1].strip():
            prefixname = camps[-2] if camps[-2].strip() else camps[-3]
        else:
            prefixname = camps[-1]
        filenameL1 = f"{prefixname}.txt"
        filenameL2 = f"{prefixname}.txt"
        filename = os.path.join(directory1, filenameL1)

        try:
            text = getPageText(link)
            with codecs.open(filename, "w", encoding="utf-8") as output:
                for s in text:
                    output.write(s + "\n")

            f = urllib.request.urlopen(link)
            soup = BeautifulSoup(f.read(), 'lxml')
            spanL2 = soup.find_all("span", {"class": f"translation-language post-translation-{lang2}"})
            if spanL2:
                linkL2 = BeautifulSoup(str(spanL2), 'lxml').find("a")["href"]
                text = getPageText(linkL2)
                filename = os.path.join(directory2, filenameL2)
                with codecs.open(filename, "w", encoding="utf-8") as output:
                    for s in text:
                        output.write(s + "\n")
        except Exception as e:
            print(f"Error processing link {link}: {e}")

    print("Process completed.")

# GUI Setup
root = tk.Tk()
root.title("")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Year:").grid(row=0, column=0, sticky="e")
year_entry = tk.Entry(frame, width=20)
year_entry.grid(row=0, column=1)

tk.Label(frame, text="Months:").grid(row=1, column=0, sticky="e")
months_entry = tk.Entry(frame, width=20)
months_entry.grid(row=1, column=1)

tk.Label(frame, text="Language 1:").grid(row=2, column=0, sticky="e")
lang1_entry = tk.Entry(frame, width=20)
lang1_entry.grid(row=2, column=1)

tk.Label(frame, text="Language 2:").grid(row=3, column=0, sticky="e")
lang2_entry = tk.Entry(frame, width=20)
lang2_entry.grid(row=3, column=1)

run_button = tk.Button(root, text="Run", command=run_program)
run_button.pack(pady=5)

root.mainloop()
