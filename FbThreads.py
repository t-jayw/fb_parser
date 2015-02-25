import nltk
from bs4 import BeautifulSoup as bs

stubfile = "/Users/tylerw/msgsample.htm"
fullfile = "/Users/tylerw/Downloads/facebook-tylerjaywood/html/messages.htm"


class Thread(object):
    def __init__(self, threadSoup):
        self.soup = threadSoup
        self.participants = [name.strip() for name in
                        threadSoup.contents[0].split(',')]
        self.messagesSoup = self.soup.findAll('div', {"class":"message"})
        self.Messages = True

    def aggregateMessages(self):
        self.Messages = [Message(msg) for msg in self.messagesSoup
                                if len(msg.findNext('p').contents) > 0]

class Message(object):
    def __init__(self, msgSoup):
        self.sender = msgSoup.find('span').contents[0]
        self.content = msgSoup.findNext('p').contents[0]
        self.meta = msgSoup.find('span', {"class":"meta"})

    def printMessage(self):
        print(self.content)

class Archive(object):
    def __init__(self, filepath):
        self.archivePath = filepath

    def makeArchiveSoup(self):
        with file(self.archivePath) as f:
            raw = f.read()
            self.archiveSoup = bs(raw)

    def pullThreads(self):
        self.threadObjects = [Thread(x) for x in
                self.archiveSoup.findAll("div", {"class" : "thread"})]

    def pullMessages(self):
            [thread.aggregateMessages() for thread in self.threadObjects]


    def pullPersonMessages(self, *members):
        """
        Finds threads with all of members
        returns a dict of {member: "all their text"}
        """
        members = [name for name in members]
        personMessageDict = {name: "" for name in members}
        for thread in self.threadObjects:
            if len(set(members) & set(thread.participants)) > 1:
                thread.aggregateMessages()
                for message in thread.Messages:
                    if message.sender in members:
                        name = message.sender
                        personMessageDict[name] += ("\n" + message.content)
            else:
                pass
        return personMessageDict




if __name__ == "__main__":
    foo = Archive(stubfile)
    foo.makeArchiveSoup()
    foo.pullThreads()
    boo = foo.pullPersonMessages("Tyler Wood", "Edmarc Hedrick")

    for x in boo:
        print x

#    for k in bar:
#    for f in k.Messages:
#            if (f.sender[0] == 'Brent Klauck'):
#                if len(f.content) > 0:
#                    print(f.sender, f.content[0])
#                    print ((f.sender[0] == 'Brent Klauck'))
#            else:
#                pass


