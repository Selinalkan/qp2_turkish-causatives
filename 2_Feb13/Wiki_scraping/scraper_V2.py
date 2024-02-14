import nltk
import urllib
import bs4 as bs
import re

#Getting the data source
source = urllib.request.urlopen("").read()

# Parsing the data/Creating BeautifulSoup object
soup = bs.BeautifulSoup(source, 'lxml')

# Fetching the data
text = ""
for paragraph in soup.find_all("p"):
	text += paragraph.text

# Preprocessing the data
text = re.sub(r"\[[0-9]*\]", " ", text)
text = re.sub(r"\s+", " ", text)
text = re.lower()
text = re.sub(r"\d", " ", text)

# Preparing the dataset

