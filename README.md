# ChatGPT as a Voice Assistant for Scheduling

## What are we trying to improve?

In this project we experimented with AIs, APIs, and prompt engineering to find a way and address issues affecting time management and the elderly. By attaching a conversational input to ChatGPT, we aimed to make using the engine feel more natural to the user. This was a Summer Project using AI, voice recognition, TtS, and other features to help aid accessibility for scheduling in elderly care.

## What we did

We considered potential issues that those with disabilities and elderly may face when using a text-based system like ChatGPT, and discussed some features that may help to make the system easier to use.

Some features include:

- Direct voice recognition
- Simple UI
- Text-to-speech output

These features are then directly linked to ChatGPT.

## How to run

Needs python3 installed for primary libraries.

The libraries for python are included in requirements.txt; just run "pip install -r requirements.txt" in terminal.

Use your personal key instead when using: [https://chat.openai.com/api/auth/session](https://chat.openai.com/api/auth/session) (need to sign in to chatgpt account first.) and copy to line 45 of assist-time.py

Then run "python assist-time.py".

### From Sally:

Demo: [https://github.com/owenshi2/AI-for-Elderly/assets/92959551/beb2f60f-bd4b-40e1-8445-8ed899f51d5e](https://github.com/owenshi2/AI-for-Elderly/assets/92959551/beb2f60f-bd4b-40e1-8445-8ed899f51d5e)

To run the code, download frontend.py (or copy it to a new python file), run 'gradio frontend.py', and open in the url it provided. When you ask, you can add something like 'please answer the question in 3 sentence', otherwise it would take very long for it to answer

To use automation you need to download chromedriver: https://chromedriver.chromium.org/downloads