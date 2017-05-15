"""Author: Avinash Reddy Penugonda
   Project: Word Finder in an Image
   Spell Check Algorithm: Peter Norvig's Algorithm used
"""

import os
import sys

#imports the spell check algorithm in the same folder
import spell

#imports the package if present, or throws error
try:
    import cv2
except ImportError:
    print("please add opencv library")
    sys.exit();

#imports the package if present, or throws error
try:
    from PIL import Image
except ImportError:
    print("please install PIL library")
    sys.exit();
    
#imports the package if present, or throws error
try:
    import numpy as np
except ImportError:
    print("please install numpy  library")
    sys.exit();

#imports the package if present, or throws error
try:
    import pytesseract
except ImportError:
    print("please install teserract library")
    sys.exit(); 

#function that reads the image for the text
def imageRead(IMG_PATH):
    #read the image
    img=cv2.imread(IMG_PATH)

    #gets the resolution of the image
    IMG_SIZE=img.shape

    #print(IMG_SIZE[0])
   # print(img.dtype)

    #convert image to gray sclae
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation to remove noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)

    #apply erosion to remove noise
    img = cv2.erode(img, kernel, iterations=1)

    #write the image
    cv2.imwrite("output_noiseless.png", img)

    #apply threshold gaussian filter to to filter other than black and white
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    #write the image to the disk
    cv2.imwrite("output_adaptive_thres.png", img)

    #convert the image to text
    result = pytesseract.image_to_string(Image.open('output_adaptive_thres.png'))
    return result

#post process the data detected by removing empty spaces
def refine_str(string):
    line=string.split("\n")
    d=[]
    for i in range(0,len(line)):
        if (line[i]!=''):   
            d.append(line[i])
    return d

#post process the data by removing empty lines
def refine_line(string):
    line=string.split(" ")
    words=[]
    for i in range(0,len(line)):
        if (line[i]!=''):
            words.append(line[i])
    return words

#to find all the occurances of the words in the image
def find_word(array,string):
    occur=[]
    length=len(string)
    dicti=dict()
    #loop all the elements in the array to find the match
    for i in range(0, len(array)):
        for j in range (0, len(array[i])):
            #to check if the word in the list is equal to the searched word
            if(string[0].upper()==(array[i][j].upper())):
                occur.append(j+1)
        #only add the occurance to the dict if it's not empty
        if(len(occur)>0):
            dicti[i+1]=occur[:]     #add all the occurances to the dictionary
        #clear the list for the next iteration
        occur.clear()
    return dicti

#to do the spell check on the list of words
def spel_check(array):
    occur=[]
    final_occur=[]
    total_count=0
    count=0
    #loop all the elements in the array to find the match
    for i in range(0, len(array)):
        for j in range (0, len(array[i])):
            #to count the total number of workds
            total_count=total_count+1
            #lower case conversion
            a=spell.words(array[i][j])
            #to check the number of spell correction done and append if corrected
            if(array[i][j]==spell.correction(a[0])):
                occur.append(array[i][j])
            else:
                occur.append(spell.correction(a[0]))
                count=count+1
        #adds all the corrected/same words to the list
        final_occur.append(occur[:])
        #clear the list for the next list in the lists of lists
        occur.clear()
    print("\nPercentage of spell corrections made =",(count/total_count)*100)
    return final_occur

#gets the absolute directory of this script
print("\nPath where files are read=")
PATH=os.path.dirname(os.path.abspath(__file__))
print(PATH)

#add the image name to the abs path to later read it
IMG_PATH=PATH+"/4.png"
print(IMG_PATH)

#to read the image
raw_data=imageRead(IMG_PATH)

#to post process the data by removing empty lines
refined_data=refine_str(raw_data)
print("\n--------The raw data is:----")
print("'",raw_data,"'")

#to post process the data to remove empty words ie.blank spaces
final_words=[]
for i in refined_data:
    #remove the blank lines
    refined_words=refine_line(i)
    #remove the blank spaces
    final_words.append(refined_words)
    
print("\n-------Refined data is ---")

#print the detected words list
print("Final detected words in the image are =\n",final_words)

#call the spell correct function to do spelling correction
spel_correct=spel_check(final_words)
print("\n  \nThe text after Spell check and Correction= \n",spel_correct);

#take user input to search the word
letter="y"

#iterate for ever
while(True):
    #checks if y/n
    if(letter=="y" or letter=="Y"):
        print("\n")
        #search input
        search_word=input("Enter the word to search=")
        print("\n")
        search_list=search_word.split(" ");

        #call the search function
        output=find_word(spel_correct, search_list)

        #to check if the searched word is present or not
        if(len(output)>0):
            print("a:[b]--->a specifies line number and [b] specifies the word position in the line")
            print("Word found at:", output)
            print("\n")
        else:
            print("Not found!\n")
        letter="n"
        #input to continue or not
        letter=input("Enter 'y' or 'Y' to continue or 'n' to exit: ")
    else:
        sys.exit()




