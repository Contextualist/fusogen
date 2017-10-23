# Fusogen

**Fusogen** is a multi-way sync chatbot for WeChat. It helps users from different groups interact as if they are in the same group, by

1. Propagate messages to other groups, with tagged username.
2. (WIP) Handle inter-group `@` mention.

Fusogen uses [itchat](littlecodersh/ItChat) for WeChat web api.

## Quick start

1. **!!!Important!!!** Purge the bot user's group contact, and save *only* the groups you what to sync.
2. Install dependencies and run
```
pip install -r requirements.txt
python fusogen.py
```
3. Scan QR code to log in the bot user
4. Now greet everyone across the border with your own account (not the bot user)

**!!!Important!!!** Do not try to run more than one fusogen bot within the sync groups, or they will trigger message flood.

## Message types synced

Supported 

* Plain text
* Image, video, file
* Shared link
* Custom stickers

Not implemented

* Shared location

Not supported

* Voice
* Shop stickers
* Red package
* Bundled chat history
