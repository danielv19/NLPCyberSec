import os
import re
import pathlib 
import pandas as pd
#folder with all processed text files and folders by department/agency
input_folder = "C:/Users/danil/jupy/oig/"

#a method to make a string out of an array -> ex. string([‘h’, ‘e’, ‘l’, ‘l’, ‘o’]) -> “hello”
def string(array):
    string = ""
    return(string.join(array))

#a method that finds a year number in the context of fy## in the txt title/name
#ex. str1 = “fy12fisma_0” -> fy_year(str1) -> 2012
def fy_year(str1):
    #remove all characters that are not fy or numbers
    name = re.sub("[^fy0-9]+", " ",str1)
    check = ""
    year = 0
    #looks at every character in the refined title name
    for word in string(name):
        #if a character is not a space, then join it with variable check
        if word != " ":
            check += check.join(word)
        #this means that the next character is a space and the string of consecutive characters is 
        done forming a word, now we check if that word starts with “fy” if it is we’ ll determine year
        elif check[:2] == "fy":
            break
        else:
            #if character is a space and the check does not start with fy then start over to look for a      
            new string of characters 
            check = ""
    try:
        #convert the “##” in “fy##” into a number, if it is not able to then an exception will be thrown 
        and 0 will we returned, returning 0 = no year found
        if int(check[2:]) > 0:
            #year will focus on the last two digits of a year (2012)
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

#arrays to keep track of data to use in the dataframe
report_year = []
report_agency = []
report_number = []
report_text = []

#naming text for every agency folder within the input folder
for agency_folder in os.listdir(input_folder):
    #dictionary to keep track of how many documents are counted by year
    year_dict = {'0000':1}
    for i in range(22):
        year_dict[2000+i] = 1

    #folder_name is the name of the folder, but only with uppercase letters
    #ex. Smithsonian Institution (SI) -> “[‘S’, ‘’, ‘’, ‘’, ‘’, ‘’,.....’I’, ‘’, ‘’, ‘’,......‘’, ’S’, ‘I’,  ‘’]
    folder_name = re.sub("[^A-Z]+", " ",agency_folder)
    #array to store acronym name
    acronym = []
    skip = False
    #looping through the folder_name text with only uppercase letters
    for i in range(len(folder_name)-1):
       #if a consecutive characters are not spaces (they are uppercase) -> this is an acronym
        if folder_name[i] != ' ' and folder_name[i+1] != ' ':
            if skip:
                skip = False
            else:
	     #put the acronym letter in the array (ex. ABC → A has just been appended)
                acronym.append(folder_name[i])
#put the next acronym letter in the array (ex.B has been appended, and soon C will)
            acronym.append(folder_name[i+1])
#and skip the next letter so there is no repeat acronym letter
            skip = True

    #rename folder_name to be the acronym
    folder_name = string(acronym)

    #looping through  the texts in the agency folder
    for text in os.listdir(input_folder+agency_folder):
        #trying to find year, will utilize fy_year(string)
        #removes all non-number characters in the txt name
        title = re.sub("[^0-9]+", " ",text)
        #puts all numeric characters into the numbers array
        numbers = [int(s) for s in title.split() if s.isdigit()]
        year = 0
        #looping through all numbers in the numbers array
        for number in numbers:
#if beginning of the number is between 1991-2021, this year will be assigned
#we are looking at int(str(number)[0:4]) since numbers like 201601 exist
            if int(str(number)[0:4]) > 1990 and int(str(number)[0:4]) < 2022:
                year = int(str(number)[0:4])
                break
#else if the number is between 11-21, the one of the years 2011-21 will be assigned
#we are looking at this as some txt names include “OIG_16_1‘ → [16, 1]
            elif number > 10 and number < 22:
                year = 2000 + number
                Break
        # year == 0 will happen when no year is found
        if year == 0:
	#now pass the txt name into fy_year(string) to try to find a year with txt named “fy12...”
            year = fy_year(text)
	#if year is still not found move on to open the txt file
            if year == 0: 
                with open(input_folder+agency_folder+"/"+text, 'rb') as file:
                    for word in file:
		#put all numbers in txt file in an array of numbers
                        numbers = [int(s) for s in word.split() if s.isdigit()]
		#usually the first year in the txt file is the year, so return the first year (1991-2021)
                        for number in numbers:
                            if number > 1990 and number < 2022:
                                year = number
	#if still no year is found, then put ‘0000’ as the year
            if year == 0:
                year = '0000'
        #full_name is the original PATH of the txt file
        full_name = str(input_folder + agency_folder + "/" + text)
        #new_name has a similar PATH as full_name except for the txt file name where it will 
        #follow agency_folder_str(year)_str(year_dict[year]) -> ex.DOE_2016_1
        new_name = str(input_folder + agency_folder + "/" + folder_name + "_" + str(year) + "_" + str(year_dict[year]) + ".txt")
        #adding information into the arrays to use in the data frame (year, agency, and increment)
        report_year.append(year)
        report_agency.append(folder_name)
        report_number.append(year_dict[year])
        #this will increment year_dict[year] by one so that the next time the same year is accessed 
        #within the same agency folder, the year_dict[year] will be increased by 1
        year_dict[year] += 1
        #opening the file to get the text and put it into report_text to use in the data frame
        with open(input_folder+agency_folder + "/" + text, 'r', encoding="utf8") as file:
            full_text = file.read().replace('\n', '')
        report_text.append(full_text)
        #renaming the txt file with the new name
        os.rename(full_name, new_name)

#create an empty dataframe object
dataframe = {}
#adding a column for the agency corresponding to the array with all the text’s agency name
dataframe['Agency'] = report_agency
#adding a column for the year….
dataframe['Year'] = report_year
#adding a column for the number associated with the text file
dataframe['Number'] = report_number
#adding a column for the text associated with the txt file
dataframe['Text'] = report_text
#combining the dataframe arrays to convert into a DataFrame object
dataframe = pd.DataFrame(data=dataframe)
