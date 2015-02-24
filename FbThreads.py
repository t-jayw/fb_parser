import nltk
from bs4 import BeautifulSoup as bs

stubfile = "/Users/tylerw/msgsample.htm"


class Thread(object):
    def __init__(self, threadSoup):
        self.soup = threadSoup
        self.participants = [name.strip() for name in
                        threadSoup.contents[0].split(',')]
        self.messagesSoup = self.soup.findAll('div', {"class":"message"})
        self.Messages = []

    def aggregateMessages(self):
        self.Messages = [Message(msg) for msg in self.messagesSoup
                                if len(msg.findNext('p').contents) > 0]

class Message(object):
    def __init__(self, msgSoup):
        self.sender = msgSoup.find('span').contents
        self.content = msgSoup.findNext('p').contents
        self.meta = msgSoup.find('span', {"class":"meta"})

    def printMessage(self):
        print(self.content)

class Archive(object):
    def __init__(self, filepath):
        self.archivePath = filepath
        self.archiveSoup = ""
        self.threadObjects = True

    def makeArchiveSoup(self):
        with file(self.archivePath) as f:
            raw = f.read()
            self.archiveSoup = bs(raw)

    def pullThreads(self):
        threadTags = (self.archiveSoup.findAll("div", {"class" : "thread"}))
        self.threadObjects = [Thread(x) for x in threadTags]

    def pullMessages(self):
            [thread.aggregateMessages() for thread in self.threadObjects]

if __name__ == "__main__":
    foo = Archive(stubfile)
    foo.makeArchiveSoup()
    foo.pullThreads()
    foo.pullMessages()

    for x in foo.threadObjects:
        if 'Edmarc Hedrick' in x.participants:
            print [msg.content for msg in x.Messages]

#    for k in bar:
#    for f in k.Messages:
#            if (f.sender[0] == 'Brent Klauck'):
#                if len(f.content) > 0:
#                    print(f.sender, f.content[0])
#                    print ((f.sender[0] == 'Brent Klauck'))
#            else:
#                pass


