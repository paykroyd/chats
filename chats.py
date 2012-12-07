# Read chats from gmail's imap interface then put together some stats

import os
import sys
import imaplib
from xml.dom import minidom
from xml.parsers.expat import ExpatError
from datetime import datetime
from dateutil import parser as date_parser

class GChatLogs(object):
  """
  Auths with gmail and loads gchat logs.
  """

  def __init__(self, user, passwd):
    self.gmail = imaplib.IMAP4_SSL('imap.gmail.com')
    self.gmail.login(user, passwd)
    self.gmail.select('[Gmail]/Chats', True)
    self.ids = None

  @property
  def chat_ids(self):
    """
    Returns a list of all the chat ids.
    """
    if self.ids == None:
      result, data = self.gmail.search(None, "ALL")
      self.ids = data[0].split() # the ids are space separated
    return self.ids

  def get_chat(self, id):
    """
    Returns the chat with the log.
    """
    result, data = self.gmail.fetch(id, "(RFC822)")
    return ChatLog(id, data[0][1])

  def import_chats(self, directory):
    """
    Imports all of the chats into the directory given.
    """
    count = 0
    for id in self.chat_ids:
      if not os.path.exists('%s/%s.chat' % (directory, id)):
        try:
          chat = self.get_chat(id)
          chat.write(directory)
          count += 1
        except:
          print 'failed to get chat id: %s - %s' % (id, sys.exc_info()[0])
    print 'finished saving %d chat logs' % count


class ChatLog(object):
  """
  Returns data about the chat log.
  """
  def __init__(self, id, data):
    """
    Params:
      id: string 
      data: imap data returned by gmail
    """
    self.id = id
    self.raw = data.replace("=\r\n", "").replace("=3D\"", "=\"")
    self.sender = self.header('From')
    self.to = self.header('To')
    self.date = date_parser.parse(self.header('Date'))
    self.subject = self.header('Subject')

    try:
      self.conversation = minidom.parseString(self.body())
      self.messages = []
      for message in self.conversation.getElementsByTagName('cli:message'):
        self.messages.append(ChatMessage(message))
    except ExpatError as e:
      print 'error parsing data for chat id %s: %s' % (id, e)

  def print_conversation(self):
    for message in self.messages:
      print message

  def header(self, name):
    """
    Returns the value of the specified header.
    """
    header = self.raw[:self.raw.index(';')]
    start = header.index(name + ":")
    end = header.index('\r\n', start)
    assert end > start
    value = header[start + len(name) + 1:end]
    return value.rstrip().lstrip()

  def body(self):
    start = self.raw.index("<con:")
    end = self.raw.rindex("</con:conversation>") + len("</con:conversation>")
    return self.raw[start:end]

  def write(self, directory='.'):
    """
    Writes the chat to a file in the directory.
    """
    f = open('%s/%s.chat' % (directory, self.id), 'w')
    f.write(self.raw)
    f.close()

  @classmethod
  def read(cls, filename, directory='.'):
    """
    Read the file from the current directory and returns a ChatLog object.
    
    Params:
      filename: name of a file in the current directory
    """
    f = open(directory + '/' + filename, 'r')
    try:
      id = filename[:-5]
      raw = f.read()
      return ChatLog(id, raw)
    finally:
      f.close()

class ChatMessage(object):
  """
  An individual message in a chat
  """
  def __init__(self, message):
    """
    Params:
      message: dom representation of the xml message
    """
    self.sender = message.attributes['to'].value
    body = message.getElementsByTagName('cli:body')
    self.timestamp = datetime.fromtimestamp(float(message.attributes['int:time-stamp'].value) / 1000)
    assert(len(body) == 1)
    self.body = body[0].childNodes[0].nodeValue

  def __str__(self):
    return "(%s) %s: %s" % (self.timestamp, self.sender, self.body)
    
