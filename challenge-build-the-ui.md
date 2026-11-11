# Challenge: build the interface yourself

You have a working API. Firms, people, reports, knowledge search, an agent that decides for
itself when to search, all of it tested and running. Nobody outside a terminal can use any
of it yet. That is your job for the next stretch.

Build a Streamlit app, in your own new UI project, with three features. No starter code is
given here on purpose. You know how to call an HTTP endpoint and display a result. Everything
below is a requirement, not a hint.

---

## Feature 1: Ask

A text box where someone can type a question in plain English, and a button to send it.

When clicked, it must call `POST /agent/ask` with the question, and:

- Show the answer text if the request completed successfully
- Show something sensible if it did not complete (the agent hit its iteration limit)
- Show the number of tool calls made and the token counts somewhere on screen
- Show a clear error message if the request fails, do not let it crash silently

## Feature 2: Search only

A separate text box and button for retrieval without generation.

When clicked, it must call `POST /knowledge/search`, and:

- List every result returned, with its title and its score
- Handle the case where the index has not been built yet, this returns a specific status
  code, not a generic failure
- Handle a normal failure differently from the "index not built" case

## Feature 3: Streaming summary

A way to pick a firm, by id, and a button to request its summary.

When clicked, it must call the streaming summary endpoint from Friday, and:

- Display the text as it arrives, not all at once after a wait
- Work for every firm id currently in the data

---

## What you are being judged on

Not whether it looks polished. Whether:

1. Every feature genuinely calls your real, running API, nothing is faked or hardcoded
2. Failures are handled, not ignored
3. You can explain, out loud, what each button press actually does end to end

## Before you start

Your API needs to already be running, in its own terminal, on its usual port. This app is a
separate project with its own environment. If you have not set that up yet, do that first,
it is not part of this challenge, it is the thirty minutes before it.
