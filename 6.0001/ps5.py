# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
        #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


# ======================
# Data structure design
# ======================

class NewsStory:
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower().strip()

    def is_phrase_in(self, text):
        text = text.lower().strip()
        for ch in string.punctuation:
            text = text.split(ch)
            text = ' '.join(text)
        text = ' '.join(text.split())

        if not (self.phrase in text or self.phrase == text):
            return False

        if not text.startswith(self.phrase):
            if text[text.index(self.phrase) - 1] != ' ':
                return False

        if not text.endswith(self.phrase):
            if text[text.index(self.phrase) + len(self.phrase)] != ' ':
                return False

        return True


# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.title)


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.description)


# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    # Constructor:
    #        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
    #        Convert time from string to a datetime before saving it as an attribute.
    def __init__(self, time):
        self.time_naive = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        self.time = self.time_naive.replace(tzinfo=pytz.timezone("EST"))


# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        if story.pubdate.tzinfo is None or story.pubdate.tzinfo.utcoffset(story.pubdate) is None:
            return self.time_naive > story.pubdate
        else:
            return self.time > story.pubdate


class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        if story.pubdate.tzinfo is None or story.pubdate.tzinfo.utcoffset(story.pubdate) is None:
            return self.time_naive < story.pubdate
        else:
            return self.time < story.pubdate


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)


# Problem 8
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)


# Problem 9
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)

# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)

    stories = [s for s in stories if all([t.evaluate(s) for t in triggerlist])]

    return stories


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    triggers = {}
    final_trigger_list = []

    for line in lines:
        words = line.split(',')
        if words[0].lower().strip() == 'add':
            [final_trigger_list.append(triggers.get(t)) for t in words[1:]]
            # for t in words[1:]:
            #     final_trigger_list.append(triggers.get(t))
        elif words[1].lower().strip() == 'title':
            triggers[words[0]] = TitleTrigger(words[2])
        elif words[1].lower().strip() == 'description':
            triggers[words[0]] = DescriptionTrigger(words[2])
        elif words[1].lower().strip() == 'before':
            triggers[words[0]] = BeforeTrigger(words[2])
        elif words[1].lower().strip() == 'after':
            triggers[words[0]] = AfterTrigger(words[2])
        elif words[1].lower().strip() == 'not':
            triggers[words[0]] = NotTrigger(triggers[words[2]])
        elif words[1].lower().strip() == 'and':
            triggers[words[0]] = AndTrigger(triggers[words[2]], triggers[words[3]])
        elif words[1].lower().strip() == 'or':
            triggers[words[0]] = OrTrigger(triggers[words[2]], triggers[words[3]])

    print(lines)  # for now, print it so you see what it contains!

    return final_trigger_list


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("POSITIVE")
        # t2 = DescriptionTrigger("POSITIVE")
        # t3 = DescriptionTrigger("CRISIS")
        # t4 = AndTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.guid not in guidShown:
                cont.insert(END, newstory.title + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.description)
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.guid)

        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
