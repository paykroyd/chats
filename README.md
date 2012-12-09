chats
=====

Python program to archive and analyze google chat logs.

This is a work in progress. I'm interested in taking a look at how IMs affect my work day since our company uses it a lot for communication. There's not much there yet in terms of actual analysis, but the code to pull down your chat, archive them, and make them available to things with is there.

Archiving your chats
====================

```python
import chats
logger = chats.GChatLog(user='username', passwd='1234')
logger.import_chats('/path/to/archive/dir') # this will save all of the chats on the server into individual files in that directory
```



