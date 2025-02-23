import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


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
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        text_lower = text.lower()

        for char in string.punctuation:
            text_lower = text_lower.replace(char, " ")

        text_words = [word for word in text_lower.split() if word]

        phrase_words = self.phrase.split()

        if not phrase_words:
            return False

        for i in range(len(text_words) - len(phrase_words) + 1):
            if text_words[i : i + len(phrase_words)] == phrase_words:
                return True

        return False


class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())


class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())


class TimeTrigger(Trigger):
    def __init__(self, time_str):
        self.time = datetime.strptime(time_str.strip(), "%d %b %Y %H:%M:%S").replace(
            tzinfo=pytz.timezone("EST")
        )


class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        story_time = story.get_pubdate()

        if story_time.tzinfo is None:
            story_time = story_time.replace(tzinfo=pytz.timezone("EST"))

        return story_time < self.time


class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        story_time = story.get_pubdate()

        if story_time.tzinfo is None:
            story_time = story_time.replace(tzinfo=pytz.timezone("EST"))

        return story_time > self.time


class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)


class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)


class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    filtered = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered.append(story)
                break
    return filtered


def load_config_lines(filename):
    """
    Read the configuration file and return a list of meaningful lines,
    stripping whitespace and ignoring comments and blank lines.
    """

    trigger_file = open(filename, "r")
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith("//")):
            lines.append(line)
    return lines


def create_trigger(trigger_type, args, triggers):
    """
    Factory function to create a trigger object based on the type and arguments.

    Args:
        trigger_type (str): The type of the trigger (e.g., TITLE, DESCRIPTION).
        args (list): List of arguments for the trigger.
        triggers (dict): Dictionary of already created triggers (for composite triggers).

    Returns:
        Trigger: The created trigger object.
    """

    if trigger_type == "TITLE":
        return TitleTrigger(args[0])
    if trigger_type == "DESCRIPTION":
        return DescriptionTrigger(args[0])
    if trigger_type == "AFTER":
        return AfterTrigger(args[0])
    if trigger_type == "BEFORE":
        return BeforeTrigger(args[0])
    if trigger_type == "NOT":
        return NotTrigger(triggers[args[0]])
    if trigger_type == "AND":
        return AndTrigger(triggers[args[0]], triggers[args[1]])
    if trigger_type == "OR":
        return OrTrigger(triggers[args[0]], triggers[args[1]])
    return None


def process_config_line(line, triggers, trigger_list):
    """
    Process a single line from the configuration file. Updates the triggers
    dictionary or appends to the trigger list based on the command.

    Args:
        line (str): A line from the configuration file.
        triggers (dict): Dictionary mapping trigger names to trigger objects.
        trigger_list (list): List to collect the triggers added by the ADD command.
    """

    parts = line.split(",")
    if parts[0] == "ADD":
        for name in parts[1:]:
            if name in triggers:
                trigger_list.append(triggers[name])
        return

    name, trigger_type, *args = parts
    triggers[name] = create_trigger(trigger_type, args, triggers)


def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """

    lines = load_config_lines(filename)
    triggers = {}
    trigger_list = []

    for line in lines:
        process_config_line(line, triggers, trigger_list)

    return trigger_list


SLEEPTIME = 120


def main_thread(master):
    try:
        triggerlist = read_trigger_config("triggers.txt")

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
        cont.tag_config("title", justify="center")
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(
                    END,
                    "\n---------------------------------------------------------------\n",
                    "title",
                )
                cont.insert(END, newstory.get_description())
                cont.insert(
                    END,
                    "\n*********************************************************************\n",
                    "title",
                )
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=" ")
            stories = process("http://news.google.com/news?output=rss")

            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
