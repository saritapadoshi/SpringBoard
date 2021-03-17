#!/usr/bin/env python
# coding: utf-8

# In[81]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np


# In[82]:


# Function to call the HTTP GET Request for the constructed URL

def getHTMLResponse(url):
    #print("URL in the function getHTMLResponse is " + url)
    response = requests.get(url)
    response.text # Access the HTML with the text property
    return(response)


# In[83]:


# Function to get the chapter names of the subject from the <Heading> in the HTML response

def getChapterName(heading):
    string = str(heading)
    name = string.split("Chapter")
    x = re.sub(" \d+", "", name[1])
    x2 = re.sub(" ","",x,1)
    x1 = x2.split("<")
    chapter_name = x1[0]
    return(chapter_name)
   


# In[84]:


# Function to get the question and answer pair of each chapter

def getQuestionsForChapter(response, class_num, chapter_num):
    chapterDict = {}
    qAList = []
        
    soup = BeautifulSoup(response.text, "html.parser")
   
    chapter_name = getChapterName(soup.h2)
    
    chapterDict['chapter_name']=chapter_name
    chapterDict['chapter_num']=chapter_num
   
    articlelist = soup.find("article").find_all("p")  # Answers are in article 
    dlist = [article.text for article in articlelist]
    
    for txt in dlist:
        ansDict = {} 
        if (class_num == 5):               # Hardcoding as the website is not uniform 
            newlist = txt.split("Ans.")    # in the website some answers start with "Ans:" For class 5
        else:
            newlist = txt.split("Answer.") # in the website some answers start with "Ans:" For Class 1
        if(len(newlist) == 2):
            ansDict['question'] = newlist[0]
            ansDict['answer'] = newlist[1]
            qAList.append(ansDict)
    chapterDict['qAList']=qAList
    
    return chapterDict


# In[85]:


### This function is used to get the Question / answer list for all the Chapters of Class

def getClassResponse(class_url, class_num):

    url_list=[]
    total_chapters = 10
    
    for chap_no in range(1,total_chapters):
        newurl = class_url+str(chap_no)+"/"
        url_list.append(newurl)
        response = getHTMLResponse(newurl)
        # Invoke function to get the list of questions of eahc chapter
        qnAnsList.append(getQuestionsForChapter(response, class_num, chap_no))


# In[86]:


# Main -- Program to scrape additional questions defined by CBSE for classes on the
# website LearnCBSE.com..

# Setting the base url to learn-cbse. website
class_base_url ="https://www.learncbse.in/ncert-solutions-for-class-"

# Currently fetching for Class 5
class_num = 5

# Currently fetching for EVS subject
subject = "evs"

# Create a dictionary object to hold the Chapter Num, chapter Name, 
# list of question, answer pair
qnAnsList = []
data = []
    
# Names of the columns in the DataFrame to be written to the CSV file    
columnsList = ["ChapterNum","ChapterName","Question","Answer"]

#DataFrame to hold all the Question Answer fetched
questionbank = pd.DataFrame(data = None, columns=columnsList)

newclass_url = class_base_url+str(class_num)+"-"+subject+"-chapter-"

getClassResponse(newclass_url,class_num)
    
for newdict in qnAnsList:
    newList = newdict['qAList']    
    for qDict in newList:
        mydict = {}
        mydict = {'ChapterNum':newdict['chapter_num'], 
                  'ChapterName':newdict['chapter_name'],
                  'Question':qDict['question'],
                 'Answer':qDict['answer']}
        data.append(mydict)
        
    
questionbank = pd.DataFrame(data)
filename = "CBSE-Class-"+str(class_num)+"-EVS.csv"
questionbank.to_csv(filename)
    



