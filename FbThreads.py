
from bs4 import BeautifulSoup as bs

stubfile = "/Users/tylerw/msgsample.htm"


class Thread(object):
    def __init__(self, threadSoup):
        self.soup = threadSoup
        self.participants = threadSoup.contents[0].split(',')
        self.messagesSoup = self.soup.findAll('div', {"class":"message"})
        self.Messages = [Message(msg) for msg in self.messagesSoup]

class Message(object):
    def __init__(self, msgSoup):
        self.sender = msgSoup.find('span').contents
        self.content = msgSoup.findNext('p').contents
        self.meta = msgSoup.find('span', {"class":"meta"})

    def printMessage(self):
        print(self.content)

def msgSoup(msgfile):
    with file(msgfile) as f:
        htmString = f.read()
    return bs(htmString)

def pullThreads(soup):
    thread_divs = (soup.findAll("div", {"class" : "thread"}))
    return thread_divs



if __name__ == "__main__":
    stubsoup = msgSoup(stubfile)

    foo = pullThreads(stubsoup)

    bar = [Thread(x) for x in foo]

    print(bar[3].Messages[0].content)
