import re
import os
from nltk.tokenize import RegexpTokenizer
import nltk

#folder with all unprocessed text files
text_folder = "C:/Users/danil/jupy/text/"
#download the nltk stopwords
nltk.download('stopwords')

for filename in os.listdir(text_folder):
    #open unprocessed text file
    file = open(text_folder+filename,'r+',encoding='utf-8')
    #put all words in one line (remove all enter keys ‘\n’) 
    oneLine = ""
    for line in file:
        stripped = line.rstrip()
        oneLine += " " + stripped
    #remove all unnecessary whitespace
    oneLine = re.sub('\s+',' ',oneLine)
    #remove all characters that are not letters or numbers
    oneLine = re.sub("[^a-zA-Z0-9]+", " ",oneLine)

    #clear the unprocessed text file
    file.truncate(0)
    file.close()

   #open the empty text file in write mode
    file = open(text_folder+filename,'w+')

    #setting up tokenizer to remove common english stopwords
    tokenizer = RegexpTokenizer(r'\w+')
    raw = oneLine.lower()
    tokens = tokenizer.tokenize(raw)
    en_stop = set(nltk.corpus.stopwords.words('english'))
    
    #final_tokens contains all the cleaned text in lowercase
    final_tokens= [token for token in tokens if token not in en_stop]
    #write the cleaned text in the previously empty text file
    for word in final_tokens:
        file.write(" " + word)
    file.close()
