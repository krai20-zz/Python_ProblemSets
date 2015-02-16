# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

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
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

class NewsStory():
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

class WordTrigger(Trigger):
    def __init__ (self, word):
        self.word = word.lower()

    def is_word_in(self,text):
        for element in text.split():
            if self.word == element.lower():
                return True
        return False

class TitleTrigger(WordTrigger):
    def evaluate(self, story):
        title = story.get_title()
        for character in string.punctuation:
            title = title.replace(character,' ')
        return self.is_word_in(title)

class SubjectTrigger(WordTrigger):
    def evaluate(self, story):
        subject = story.get_subject()
        for character in string.punctuation:
            subject = subject.replace(character,' ')
        return self.is_word_in(subject)

class SummaryTrigger(WordTrigger):
    def evaluate(self, story):
        summary = story.get_summary()
        for character in string.punctuation:
            summary = summary.replace(character,' ')
        return self.is_word_in(summary)

# Composite Triggers
# Problems 6-8

class NotTrigger(Trigger):
    def __init__(self, trig):
        self.trig = trig

    def evaluate(self, story):
        return not self.trig.evaluate(story)


class AndTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2

    def evaluate(self, story):
        return self.trig1.evaluate(story) and self.trig2.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2

    def evaluate(self, story):
        return self.trig1.evaluate(story) or self.trig2.evaluate(story)

# Phrase Trigger
# Question 9

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        title = story.get_title()
        summary = story.get_summary()
        subject = story.get_subject()
        if self.phrase in title or self.phrase in subject or self.phrase in summary:
            return True
        return False

#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """

    triggered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                triggered_stories.append(story)
    return triggered_stories


#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    Triggerlist = []
    for line in lines:
        line = line.split()
        if line[0] != 'ADD':
            trigger_def = line[0]
        keyword = line[1]
        arg = line[1:]

        trigger_def = keyword + 'Trigger'(arg)

    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Obama")
    t2 = SummaryTrigger("MIT")
    t3 = PhraseTrigger("Supreme Court")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    #triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

