# my-ai-talking-buddy

## Wish to chat freely in a foreign language? 👫💬

This is a **CLI chatbot for learning and practicing the English language**.

## Installation and launch

Clone the repo.

`cd` to the directory containing `chatbot.py`.

Modify `api_secrets_example.py` content with your API keys and then rename the file to `api_secrets.py`

`pip install requirements.txt` into your environment.

Run `python chatbot.py` to dive into the CLI and start chatting! 😊

## How to use

### Personalize your session 🎯

To get started, you will be asked to indicate your name. 
Then, select your mother tongue and choose a buddy by entering the number associated to it. 

Once you're all set up, there are 2 ways at your disposal to interact with Jack, Mrs. Smith or Arthur: _free chatting_ and _commands_.

### Free chatting 📧

Simply type **anything** you want! 

Answer your buddy's enquiries, ask them more about themselves or specific events they lived - they'll be happy to give you all the details you'd like.

Make up stories, ask about all the adventures you (virtually) lived together.

Don't hesitate to change topic whenever you wish to. 

### Commands 🤖

To list all commands, enter `/help`.

Here is a reminder of all possible commands:

- `/audio`: Record your voice instead of typing. Stop recording with `ctrl+c`.
- `/translate_last`: Translate the last message to your mother tongue.
- `/translate_text`: You will be asked to enter a text which you wish to translate. 
- `/generate_vocabulary`: Generate a list of the most common words in English which you used in your discussion.
- `/play_last`: Allow your buddy to talk through your speakers! Listen to their last message.
- `/help`: List all commands.
- `/exit`: Once you're done talking to your buddy.

## Inspiration

What is the best way to learn a new language? For sure by **talking**, especially by having a discussion with lifelike characters who never run out of creativity or new stories to tell you about.

## What it does

We introduce a talking AI-powered bot that helps users learn and practice English.

The bot uses advanced natural language processing technology to understand user input and provide **detailed, contextualized answers**, as well as **speech transcriptions** for more **intuitive interaction**.

Several characters are available to speak with, so that the user never gets bored - they all have their specific voice and relation to the language learner. With their friendly and approachable personality, they make learning **fun, engaging and accessible to everyone**.

Additionally, our AI talking bot allows users to spontaneously interact with it in a variety of ways, including typing responses or speaking directly to the bot, so as to ensure that users can use the bot in the way that is most convenient and comfortable for them.

## How we built it

We combined many of the basic building blocks available from the organizers of this hackathon. These blocks being very powerful taken separately, our goal was to combine them in a clever way. 

The speech-to-text part leverages AssemblyAI to transcribe the sentences uttered by the user for a more natural interaction.

Generating the answers of the Buddy is done by GPT3-DaVinci. 

The text-to-speech part is done using Uberduck. We picked high-quality, expressive voices to teach the user the correct pronunciation of words.

We rely on Google Translate for text-to-text translation. 


## Challenges we ran into

We had never used any of the APIs before, nor had we really played with GPT3. There was therefore some work involved in learning how to use the APIs and practicing prompt engineering to obtain precisely what we wanted.

## Accomplishments that we're proud of

Being able to make a simple yet comprehensive app out of diverse building blocks using the latest advances in the domain - in such a short amount of time - is very rewarding and promising for the future of language learning apps in general.

## What we learned

We developed our collaborative skills to go straight to the point of building a clean repo and a functional project as quickly as possible.

## What's next for _My AI Talking Buddy_ ➡📱

The biggest improvement we can think of is to turn it into a **mobile app**, to keep your Buddy in your pocket at all times. This would also allow for a responsive interface, keeping a permanent record of all your conversations, exporting your vocabulary lists to your phone’s notes app - and much more.

We have some additional ideas which we would love to build into our Buddy:

- Detecting the language spoken: if the user is more comfortable talking in their mother tongue, allow them to!
- Selecting a level: from beginner to advanced!
- Additional languages!

In the meantime, we encourage you to **try it yourself**: it's as simple as talking to one of your relatives. 
