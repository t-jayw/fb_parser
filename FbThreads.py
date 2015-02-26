import nltk
from bs4 import BeautifulSoup as bs

stubfile = "/Users/tylerw/msgsample.htm"
fullfile = "/Users/tylerw/Downloads/facebook-tylerjaywoodd/html/messages.htm"



def tokenizeString(string):
    tokenized = nltk.word_tokenize(string)
    return tokenized

def removeStopWords(wordlist):
    goWords = [word.lower() for word in wordlist if word.lower()
                not in nltk.corpus.stopwords.words('english')]
    return goWords

def prepString4Nltk(string):
    tokenized = tokenizeString(string)
    words = removeStopWords(tokenized)
    return words


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



class PeopleArchive(Archive):
    def __init__(self, filepath, *members):
        super(PeopleArchive, self).__init__(filepath)
        self.members = [name for name in members]

    def pullPersonMessages(self):
        """
        Finds threads with all of members
        returns a dict of {member: "all their text"}
        """
        personMessageDict = {name: "" for name in self.members}
        test = []
        for thread in self.threadObjects:
            if len(set(self.members) & set(thread.participants)) > 1:
                test.append(thread.participants)
                thread.aggregateMessages()
                for message in thread.Messages:
                    if message.sender in self.members:
                        name = message.sender
                        personMessageDict[name] += ("\n" + message.content)
            else:
                pass
        self.personMessageDict = personMessageDict

    def prepPersonMessageDict(self, *people):
        for person in people:
            if person in self.personMessageDict.keys():
                self.personMessageDict[person] = \
                        prepString4Nltk(self.personMessageDict[person])


    def findTopWords(self, *person):
        pass


if __name__ == "__main__":
    foo = PeopleArchive(fullfile, "Tyler Wood", "Edmarc Hedrick")
    foo.makeArchiveSoup()
    foo.pullThreads()
    foo.pullPersonMessages()

    for k, v in foo.personMessageDict.items():
        print k, len(v)

    foo.prepPersonMessageDict("Tyler Wood", "Edmarc Hedrick")

    print(len(foo.personMessageDict))

    for k, v in foo.personMessageDict.items():
        print k, len(v)

