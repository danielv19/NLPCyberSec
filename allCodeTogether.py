##PUT EACH SECTION IN A DIFFERENT BLOCK IN JUPYTER NOTEBOOK!!!!
##===================================================================================
#SECTION 1: PDF Converter
##===================================================================================
import os
import wordninja
import PyPDF2
from pathlib import Path
import textract
from pikepdf import Pdf
import slate3k as slate
from pathlib import Path
for folder in os.listdir("C:/Users/danil/jupy/oig/pdf"):
    input_folder = "C:/Users/danil/jupy/oig/pdf/" + folder + "/"
    decrypt_folder = "C:/Users/danil/jupy/oig/decrpyted/"
    text_folder = "C:/Users/danil/jupy/oig/text/" + folder + "/"
    for filename in os.listdir(input_folder):
        pdf = open(input_folder+filename,'rb')
        output = text_folder + filename[0:len(filename)-4] + ".txt"

        file = input_folder + filename

        pdfReader = PyPDF2.PdfFileReader(pdf)    
        if pdfReader.isEncrypted:
            pdf2 = Pdf.open(pdf)
            pdf2.save(decrypt_folder + filename)
            pdf.close()
            pdf = open(decrypt_folder+filename,'rb')
            pdfReader = PyPDF2.PdfFileReader(pdf)
            file = decrypt_folder + filename
        
        text = open(output, "a", encoding='utf-8')
        try:
            with open(file,'rb') as f:
                extracted_text = slate.PDF(f)
                for word in extracted_text:
                    text.write(word)
            if (Path(output).stat().st_size < 1000):
                raise Exception("no text")
        except:
            for i in range(pdfReader.getNumPages()):
                page = pdfReader.getPage(i)
                try:
                    textPage = page.extractText()
                    words = wordninja.split(textPage)
                    for word in words:
                        text.write(f"{word} ")
                except:
                    i += 1
        text.close()
##===================================================================================
##SECTION 2: PROCESSING (LOOK AT GOOGLE DOC FOR MORE INFO ON HOW TO GET GOOD DATA
##===================================================================================  
import re
import os
import array
from nltk.tokenize import RegexpTokenizer
import nltk
nltk.download('stopwords')

for folder in os.listdir("C:/Users/danil/jupy/oig/text/"):
  text_folder = "C:/Users/danil/jupy/oig/text/" + folder + "/"
  for filename in os.listdir(text_folder):
      file = open(text_folder+filename,'r+',encoding='utf-8')

      oneLine = ""
      for line in file:
          stripped = line.rstrip()
          oneLine += " " + stripped
      oneLine = re.sub('\s+',' ',oneLine)
      oneLine = re.sub("[^a-zA-Z0-9]+", " ",oneLine)

      file.truncate(0)
      file.close()

      file = open(text_folder+filename,'w+')

      tokenizer = RegexpTokenizer(r'\w+')
      raw = oneLine.lower()
      tokens = tokenizer.tokenize(raw)
      en_stop = list(nltk.corpus.stopwords.words('english'))
      stopped_tokens = [token for token in tokens if token not in en_stop]

      for word in stopped_tokens:
          file.write(" " + word)
      file.close()
##===================================================================================
##SECTION 3: RENAMING AND DATA FRAME COLLECTION (put parts into differnt blocks in jupyter nootebok)
##===================================================================================  
#PART 1
import os
import re
import pathlib 
import pandas as pd

##text_folder = "C:/Users/danil/jupy/text/"
agency_folder= "United States Postal Service (USPS)"
input_folder = "C:/Users/danil/jupy/oig/text/"

def string(array):
    string = ""
    return(string.join(array))

def fy_year(str1):
    name = re.sub("[^fy0-9]+", " ",str1)
    #print(name)
    check = ""
    year = 0
    for word in string(name):
        if word != " ":
            check += check.join(word)
        elif check[:2] == "fy":
            break
        else:
            check = ""
    try:
        if int(check[2:]) > 0:
            year = int(check[2:])
            if year < 22:
                year = 2000 + year
            elif year > 22 and year < 100:
                year = 1900 + year
            elif year < 1990:
                year = 0
        return year
    except:
        return 0
#PART 2
report_year = []
report_agency = []
report_number = []
report_text = []
#for agency_folder in os.listdir(input_folder):
#dictionary to keep track of how many documents are counted by year
year_dict = {'0000':1}
for i in range(22):
    year_dict[2000+i] = 1
folder_name = re.sub("[^A-Z]+", " ",agency_folder)
acronym = []
skip = False
for i in range(len(folder_name)-1):
    if folder_name[i] != ' ' and folder_name[i+1] != ' ':
        if skip:
            skip = False
        else:
            acronym.append(folder_name[i])
        acronym.append(folder_name[i+1])
        skip = True
folder_name = string(acronym)
for text in os.listdir(input_folder+agency_folder):
    title = re.sub("[^0-9]+", " ",text)
    numbers = [int(s) for s in title.split() if s.isdigit()]
    year = 0
    for number in numbers:
        if int(str(number)[0:4]) > 1990 and int(str(number)[0:4]) < 2022:
            year = int(str(number)[0:4])
            break
        elif number > 10 and number < 22:
            year = 2000 + number
            break
    if year == 0:
        year = fy_year(text)
        if year == 0: 
            with open(input_folder+agency_folder+"/"+text, 'rb') as file:
                for word in file:
                    numbers = [int(s) for s in word.split() if s.isdigit()]
                    for number in numbers:
                        if number > 1990 and number < 2022:
                            year = number
        if year == 0:
            year = '0000'
    full_name = str(input_folder + agency_folder + "/" + text)
    new_name = str(input_folder + agency_folder + "/" + folder_name + "_" + str(year) + "_" + str(year_dict[year]) + ".txt")
    textfull = ""
    report_year.append(year)
    report_agency.append(folder_name)
    report_number.append(year_dict[year])
    year_dict[year] += 1
    with open(input_folder+agency_folder + "/" + text, 'r', encoding="utf8") as file:
        full_text = file.read().replace('\n', '')
    report_text.append(full_text)
    os.rename(full_name, new_name)
#Part 3
dataframe = {}
dataframe['Agency'] = report_agency
dataframe['Year'] = report_year
dataframe['Number'] = report_number
dataframe['Text'] = report_text
dataframe = pd.DataFrame(data=dataframe)
##===================================================================================
##SECTION 4: LDA AND DATA OUTPUT
##===================================================================================  
import numpy as np
import pandas as pd
import re

# Plotly imports
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls

# Other imports
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from matplotlib import pyplot as plt
## %matplotlib inline
import nltk
from nltk.stem import WordNetLemmatizer
lemm = WordNetLemmatizer()

class LemmaCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(LemmaCountVectorizer, self).build_analyzer()
        return lambda doc: (lemm.lemmatize(w) for w in analyzer(doc))
    
    
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    return text

def print_top_words(model, feature_names, n_top_words):
    for index, topic in enumerate(model.components_):
        message = "\nTopic #{}:".format(index + 1)
        message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1 :-1]])
        print(message)
        print("="*90)
train = dataframe

#stopwords = nltk.corpus.stopwords.words('english')
#for headline in train["headline"]:
#    headline_list = nltk.word_tokenize(headline)
#    headline_list_clean = [word for word in headline_list if word.lower() not in stopwords]

#analyzing the text values
text = list(train["Text"].values)
# Calling our overwritten Count vectorizer
tf_vectorizer = LemmaCountVectorizer(max_df=0.95, min_df=2, preprocessor=preprocess_text, stop_words='english', decode_error='ignore')
tf = tf_vectorizer.fit_transform(text)

#feel free to edit the number of components (topic) and other parameters
lda = LatentDirichletAllocation(n_components=3, max_iter=100, learning_method = 'online', learning_offset = 40., random_state = 0)
lda.fit(tf)
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, 8)
