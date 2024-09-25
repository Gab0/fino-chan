<img src="./web/static/logo.png" alt="Fino-chan Logo" width="300" height="auto">

## About

A platform where people can talk. The respect and finesse is mandatory, and enforced to everyone by a language model.

Users post messages in the boards, but they are just stored in the database, not immediately shown.
A language model will check the user messages messages in the database, then generate a better version of them.
The model-generated messages will be posted in the forum.

## Tech Stack

- `next.js` frontend (no backend)
- `supabase` for storage. 
- A Python app that runs on the `supabase` database, and handles the moderation and the language model.
- `OpenAI` for the language model, `ChatGPT`.


## Milestones

### Phase 1: MVP

Just a mural where annonymous users can post messages and see what everyone else posted.


### Phase 2: A simple forum

Annonymous forums with threads.


### Phase 3: An imageboard

A fully featured imageboard, with multiple boards. Annonymous users only.

