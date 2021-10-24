from tClient import *
from nltk.sentiment import SentimentIntensityAnalyzer
import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

twitter = tClient()

sia = SentimentIntensityAnalyzer()


class Globals:
    bottomFrame = None
    rootWindow = None
    searchTermEntry = None
    choiceVar = None
    searchButton = None
    text = None
    used = []
    length = []
    plot = 'z'

def add(x,y):
    Globals.plot = plt.figure()

    plt.scatter(x, y, color='r')

    plt.xlabel('Number of Tweets')
    plt.ylabel('Sentiment of Tweets')
    plt.title('Keyword analysis')

    canvas = FigureCanvasTkAgg(Globals.plot, Globals.bottomFrame)
    canvas.get_tk_widget().grid(row=1, column=0)



def getChoiceVar():
    a = Globals.choiceVar.get()
    print(a)


def gradeTweets(searchTerm, numTweets):
    Globals.used = []
    Globals.length = []
    tweets = twitter.get_tweets(searchTerm, numTweets)
    score = 0
    posTweets = 0
    negTweets = 0
    netTweets = 0
    for tweet in tweets:
        if sia.polarity_scores(tweet)['compound'] < 0:
            Globals.used.append(sia.polarity_scores(tweet)['compound'])
            negTweets += 1
            score += sia.polarity_scores(tweet)['compound']
        elif sia.polarity_scores(tweet)['compound'] > 0:
            Globals.used.append(sia.polarity_scores(tweet)['compound'])
            posTweets += 1
            score += sia.polarity_scores(tweet)['compound']
        else:
            netTweets += 1
    for x in range(1,len(Globals.used)+1):
        Globals.length.append(x)

    avg = round((negTweets/(posTweets+negTweets+netTweets))*100, 2)



    return [avg, posTweets, negTweets, netTweets]


def master(searchTerm,numTweets):
    resultList = gradeTweets(searchTerm, numTweets)
    Globals.text.configure(state=tkinter.NORMAL)
    Globals.text.delete(1.0,tkinter.END)
    Globals.text.insert(tkinter.INSERT,'Percent of Negative Tweets: {}%\nTotal Positive Tweets: {}\nTotal Negative Tweets: {}\nTotal Neutral Tweets: {}'.format(resultList[0],resultList[1],resultList[2],resultList[3]))
    Globals.text.configure(state=tkinter.DISABLED)
    add(Globals.length, Globals.used)


def initializeGUI():
    Globals.rootWindow = tkinter.Tk()
    Globals.rootWindow.title("User Rating Index")

    Globals.rootWindow.geometry("640x640")

    topFrame = tkinter.Frame(Globals.rootWindow)
    topFrame.grid(row=0, column=1)

    middleFrame = tkinter.Frame(Globals.rootWindow)
    middleFrame.grid(row=1, column=1)

    Globals.bottomFrame = tkinter.Frame(Globals.rootWindow)
    Globals.bottomFrame.grid(row=2, column=1)


    Globals.choiceVar = tkinter.IntVar()
    Globals.choiceVar.set(0)

    searchTermLabel = tkinter.Label(topFrame, text='Search Term:')
    searchTermLabel.grid(row=0, column=0)

    Globals.searchTermEntry = tkinter.Entry(topFrame)
    Globals.searchTermEntry.grid(row=0, column=1)

    numTweetsLabel = tkinter.Label(topFrame, text='Number of Tweets:')
    numTweetsLabel.grid(row=1,columnspan=6)

    numTweetRadio1 = tkinter.Radiobutton(middleFrame, text='10', variable=Globals.choiceVar, value=10)
    numTweetRadio1.grid(row=0,column=0)

    numTweetRadio2 = tkinter.Radiobutton(middleFrame, text='25', variable=Globals.choiceVar, value=25)
    numTweetRadio2.grid(row=0, column=1)

    numTweetRadio3 = tkinter.Radiobutton(middleFrame, text='50', variable=Globals.choiceVar, value=50)
    numTweetRadio3.grid(row=0, column=2)

    numTweetRadio4 = tkinter.Radiobutton(middleFrame, text='100', variable=Globals.choiceVar, value=100)
    numTweetRadio4.grid(row=0, column=3)

    Globals.searchButton = tkinter.Button(topFrame, text='Search', command=lambda: master(Globals.searchTermEntry.get(), Globals.choiceVar.get()))
    Globals.searchButton.grid(row=0, column=2)

    Globals.text = tkinter.Text(Globals.bottomFrame, height=4,state=tkinter.DISABLED)
    Globals.text.grid(row=0,column=0)


def start():
    initializeGUI()
    Globals.rootWindow.mainloop()

start()
