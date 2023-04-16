# downloadGlobalVoices
A script for Downloading Global Voices pieces of news in 2 languages and convert them to text.

#Prerequisites

You need beautifulsoup4 to be installed in ypour computer.

```sudo pip3 install beautifulsoup4```

#Use

To download for example, all the pieces of news in English with translations into Spanish from January to March 2023, you can write:

```python3 downloadGlobalVoices.py 2023 1-3 en es```

To download all 2022 year write:

```python3 downloadGlobalVoices.py 2022 all en es```

The program will create a directory for each year and language and it will save there the pieces of news converted into text. The files will have the same name for each language, using the title of the target language, for example, in the folder for English we will have a file called:

fuerte-nevada-provoca-muerte-de-turistas-en-estacion-de-montana-de-pakistan.txt

containing the piece of news in English, and in the Spanish folder the corresponding piece of news in Spanish will have the same name

fuerte-nevada-provoca-muerte-de-turistas-en-estacion-de-montana-de-pakistan.txt

In this way the automatic alignment will be much easier.

