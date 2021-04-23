#Spam Scan by Jonathan Gill, Erick Aranda, and Lorne Beerman

# Usage:
# spamscan.py -OPTION <TwitterApiCsvFile> <keyword>
# -b --> Specific Keyword and Sentiment Analysis
#-m --> Bot repost analysis on tweets with specified keywords
#-t ---> Tweet Trend Analysis with graphical output (Leave keyword field blank)

#2016 Election Twitter API Source: Kaggle

#w3schools.com/python
#https://docs.python.org/3/library/csv.html
#geeksfirgeeks.org/fuzzywuzzy-python-library/
#pypi.org/project/vaderSentiment/

#Sentiment text files source:
#Bing Liu, Minqing Hu and Jsheng Cheng. "Opinion Observer: Analyzing and comparing opinions on the Web." Proceedings of the 14th International World Wide Web Conference (WWW-2005), May 10-14, 2005, Chiba, Japan.


import csv
import sys
import time
import datetime
from datetime import date
from datetime import timedelta
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# This function treats the csv file like a dictionary to collect called user data. This also uses the sadwords function implementation to determine the sentiment of tweet content.

def basic(database,tweet,pos,neg):
    list2 = []
    for row in database:
        if row['tweet'] == None:
            return list2
        if tweet in row['tweet']:
            list2.append(row['tweet'])
            print(row['tweet'])
            print(" "*2)
            sadwords(row['tweet'],neg,pos)
            print(" This statement based on our database may contain biased or misinformation.")
            print(" ")
            print(" The user's name is:",row['user_name'])
            print(" ")
            print(" The user's info is:")
            print(" ")
            print( row['user_description'])
            print(" ")
            print(" The city of origin:", row['city'])
            print(" The country of origin:",row['country'])
            print(" The number of retweets is:",row['retweet_count']) 
            print(" The application source is of this tweet is:", row['source'])
            print("------------------------------------------------------------------------------")
            print(" "*2)
        
    else:
        print(" This statement based on our database does not contain any bias or misinformation")

    
def read_the_csv(input_file):
    input_file = open(input_file, newline='')
    csv_reader = csv.DictReader(input_file)
    for row in csv_reader:
        for key, value in row.items():
            try:
                row[key] = value.strip()
            except:
                pass
            yield row

#step one, read in database
#step two, assign each line a compound score
#step three, continue onward.
#for analysis, we just summarize every line's compound score, that way
#it's easy to grab the time. 


########################################################################################################

def botmatch(database,tweet):
    counter = 0
    for row in database:
        if fuzz.ratio(tweet,row['tweet']) >=90:
            counter +=1
    print('The tweet', tweet)
    print('is similar to', counter)
    print('tweets posted by other accounts')
    print(' ')

########################################################################################################



def trendanalysis(database2, analyzer):

    for line in database2:
        try:
            line['sentiment'] = analyzer.polarity_scores(line['tweet'])
        except:
            pass


    sentimentTracker=[]
    sentimentTrackerCleaned=[]


#the format for sentiment goes ['neg':, 'neu':, 'pos':, 'compound':]
# the format for datetime.datetime is datetime.datetime(year, month, day, hour, minute, second)
f

    for line in database2:
        try:
            sentimentTracker.append(((line['sentiment']['compound']), (line['created_at'])))
        except:
            pass
    for item in range(len(sentimentTracker)):
        
        try:  
            date = datetime.datetime(int(str(sentimentTracker[item][1][0:4])), int(str(sentimentTracker[item][1][5:7])), int(str(sentimentTracker[item][1][8:10])), int(str(sentimentTracker[item][1][11:13])), int(str(sentimentTracker[item][1][14:16])), int(str(sentimentTracker[item][1][17:19])))
            sentimentTrackerCleaned.append((sentimentTracker[item][0], date))
        except:
            pass


    sentimentByMinute={}
    startingDateTime = sentimentTrackerCleaned[0][1]

    print("The Time Period for this collection is:\n")
    print(sentimentTrackerCleaned[-1][1] - sentimentTrackerCleaned[1][1])
    worstTweet = 0
    bestTweet = 0
    for item in range(len(sentimentTrackerCleaned)):
        if(item == 0):
            print("successfully reached the first step")
            timeComparison = startingDateTime
            sentimentByMinute[0] = sentimentTrackerCleaned[0][0]
            currentMinute = 0
            counterForAverage = 1
        if (sentimentTrackerCleaned[item][0] != 0):
            if (sentimentTrackerCleaned[item][1] - timeComparison < datetime.timedelta(minutes=1)):
                sentimentByMinute[currentMinute] = sentimentByMinute[currentMinute] + sentimentTrackerCleaned[item][0]
                counterForAverage = counterForAverage +1

            if (sentimentTrackerCleaned[item][1] -timeComparison > datetime.timedelta(minutes=1)):
                try:
                    sentimentByMinute[currentMinute] = sentimentByMinute[currentMinute]/counterForAverage
                    currentMinute = currentMinute + 1
                    sentimentByMinute[currentMinute] = 0
                    counterForAverage = 0
                except:
                    pass
            if (sentimentTrackerCleaned[item][0] < sentimentTrackerCleaned[worstTweet][0]):
                worstTweet = item
            if (sentimentTrackerCleaned[item][0] > sentimentTrackerCleaned[bestTweet][0]):
                bestTweet = item
    print(sentimentByMinute)
    print("\nThe most favored tweet is:\n")
    print(sentimentTrackerCleaned[bestTweet])
    print("\n")
    print(database2[bestTweet]['tweet'])
    print("\nThe least favored tweet is:\n")
    print(sentimentTrackerCleaned[worstTweet])
    print(database2[worstTweet]['tweet'])
    print("\n")
    f_write = open('graph.txt', 'w+')
    for item in range(len(sentimentByMinute)):
        string = str(item) + ' ' + str(sentimentByMinute[item]) + '\n'
        f_write.write(string)
    f_write.close()


    xplot=[]
    yplot=[]
    yaxis=[-1, -.9, -.8, -.7, -.6, -.5, -.4, -.3, -.2, -.1, 0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
    for item in range(len(sentimentByMinute)):
        xplot.append((item))
        yplot.append((sentimentByMinute[item]))
        plt.title("trend")
        plt.xlabel("minute")
        plt.ylabel("sentiment")
        plt.yticks(yaxis)
        plt.plot(xplot, yplot, marker = 'o', c='g')
        plt.show()


########################################################################################################

# makes a basic sentiment determination based on the number of positive words to negative words.

def sadwords(tweet,neg,pos):
    counterA = 0
    counterB = 0

    for line in neg:
        if line.rstrip() in tweet:
            counterA += 1
            
    if counterA!= 0:
        print("This tweet has" + " " + str(counterA) + " " + "negative sentiment words")

    for line in pos:
        if line.rstrip() in tweet:
            counterB +=1
        
    if counterB != 0:
        print("This tweet has" + " " + str(counterB) + " " + "positive sentiment words")
    
    if counterA > counterB:
        print("This tweet maybe negatively biased.")
        print(" ")

    if counterB > counterA:
        print("This tweet maybe be positively biased.")
        print(" ")
    else:
        print("This tweet may have bias.")
        

    
########################################################################################################

#opens list of positive and negative words.
pos = open('positive.txt', 'r').readlines()

neg = open('negative.txt', 'r').readlines()

#opens csv twitter api database file.

with open(sys.argv[2], newline='') as database:
    DB = csv.DictReader(database)

    if sys.argv[1] ==None:
        print("Please enter a valid option")

#option b returns a list of tweets based on a inputted keyword along with specific user and sentiment details.
    if sys.argv[1] == '-b':

        string = sys.argv[3]

        basic(DB,string,pos,neg)

#option m tests a range of tweets based in a specified keyword to test for bot reposting.
    
    if sys.argv[1] == '-m':

        list2 = []
        string = sys.argv[3]

        for row in DB:
            if row['tweet']==None:
                break
            if string in row['tweet']:
                list2.append(row['tweet'])

        for i in list2:
            botmatch(DB,i)

#option t finds the most popular tweet along with sentiment trends in a guioutput.

    if sys.argv[1] == '-t':

        analyzer = SentimentIntensityAnalyzer()

        analyzer.polarity_scores("here is the string to analyse")

        database2 = read_the_csv(sys.argv[2])

        database2 = list(database2)

        trendanalysis(database2,analyzer)

#that outputs a dictionary of 'neg', 'neu', 'pos', 'compound'
#the compound score is basically a summary score between -1 and +1

#the idea is to graph the compound scores over time. 
#average out the compound scores per hour? and then plot it. 

# create dictionary for plotting only
# we modify database, give it an overall sentiment, attach it to the database. 
# so just add a compound score 







