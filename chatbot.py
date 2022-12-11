"""You are in the main module. This module contains the classes used to handle the conversation between the user and the bot. It also contains the main function that runs the chatbot."""

import textwrap
import re
import os
import audio_commands as ac
import translation as tr

import openai

from api_secrets import API_KEY_OPENAI


openai.api_key = API_KEY_OPENAI


# main chat class
class Conversation:
    """This class handles the conversation between the user and the bot. It handles the formatting of the messages in the Python console, and it also stores the conversation history."""

    def __init__(self):

        self.history = []

        # create "tmp" folder if it doesn't exist
        if not os.path.exists("tmp"):
            os.makedirs("tmp")

    def add_to_history(self, message, is_bot=False):
        """Add a message to the conversation history.

        Args:
            message (str): message to add to the conversation history.
            is_bot (bool, optional): whether the message comes from the bot or the user. Defaults to False.
        """
        self.history.append((message, is_bot))

    def display_conversation(self):
        """Display the conversation history in the Python console."""
        # clear the screen
        print("\033c")
        # loop through the history and format each message
        for message in self.history:
            self.format_message(message)

    def justify(self, txt, width):
        """Justify a text to a certain width. This is used to format the messages in the Python console.

        Args:
            txt (str): text to justify
            width (int): desired width of the text

        Returns:
            str: justified text using carriage returns
        """
        prev_txt = txt
        while (l := width - len(txt)) > 0:
            txt = re.sub(r"(\s+)", r"\1 ", txt, count=l)
            if txt == prev_txt:
                break
        return txt

    def format_message(self, message):
        """Format a message to display it in the Python console. We try to display the conversation like a chat app, with a frame around the message, justified text, left-aligned for the bot and right-aligned for the user.

        Args:
            message (tuple): tuple containing the message and a boolean indicating whether the message is from the bot or the user.
        """
        wrapper = textwrap.TextWrapper(width=30)
        dedented_text = textwrap.dedent(text=message[0])
        txt = wrapper.fill(text=dedented_text)
        txt = txt.splitlines()  # we now have a list of fixed-width lines

        # check if the message is from the bot
        if message[1]:
            # format the message as the bot
            # display a frame around the message
            print("┌" + "─" * 30 + "┐")
            for i, line in enumerate(txt):
                if i == len(txt) - 1:
                    print("│" + line + " " * (30 - len(line)) + "│")
                else:
                    print("│" + self.justify(line, 30) + "│")
            print("└" + "─" * 30 + "┘")

        else:
            # format the message as the user
            # display a frame around the message
            print(" " * 50 + "┌" + "─" * 30 + "┐")
            for i, line in enumerate(txt):
                if i == len(txt) - 1:
                    print(" " * 50 + "│" + line + " " * (30 - len(line)) + "│")
                else:
                    print(" " * 50 + "│" + self.justify(line, 30) + "│")
            print(" " * 50 + "└" + "─" * 30 + "┘")

        print()  # add a blank line


# chatbot class
class DaVinci:
    """This class handles the chatbot. It uses the OpenAI API to generate answers to the user's messages. The model used is the "text-davinci-003" model, with a temperature adjusted according to the character choosen by the user."""

    def __init__(self):
        self.name = None
        self.conditioning = None  # the conditioning is the base description of the character and the context of the conversation, in addition to various behaviors to adopt

    def format_prompt(self, conversation, username):
        """Format the prompt to send to the OpenAI API. The prompt is composed of the conditioning, the conversation history, with the name of the bot and the name of the user in front of each message. The name of the bot is also added at the end of the prompt, to indicate to the API that the bot is now supposed to answer.

        Args:
            conversation (Conversation): conversation object
            username (str): name of the user

        Returns:
            str: formatted prompt
        """
        prompt = ""
        # add the conditioning
        prompt += self.conditioning + "\n"
        # add the history
        for message in conversation.history:
            if message[1]:
                prompt += f"{self.name}: " + message[0] + "\n"
            else:
                prompt += f"{username}: " + message[0] + "\n"

        prompt += f"{self.name}: "

        return prompt

    def get_answer(self, conversation, username, temperature, max_tokens=200):
        """Get an answer from the OpenAI API. The answer is generated using the "text-davinci-003" model, with a temperature adjusted according to the character choosen by the user. The response of the API is parsed to just retrieve the answer.

        Args:
            conversation (Conversation): conversation object
            username (str): name of the user
            temperature (float): temperature of the model
            max_tokens (int, optional): maximum number of tokens in the answer. Defaults to 200.

        Returns:
            str: answer generated by the OpenAI API
        """
        prompt = self.format_prompt(conversation, username)
        answer = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=[f"{username}:"],
        )

        # parse the response of the API
        answer = answer["choices"][0]["text"]

        # delete the spaces at the beginning and the end of the answer
        answer = answer.strip()

        return answer


# user class
class User:
    """This class handles the user. It is used to get an input from the user and to store the user's information."""

    def __init__(self):
        self.name = None
        self.mother_tongue = None

    def get_input(self, message):
        """Get an input from the user.

        Args:
            message (str): message to display to the user

        Returns:
            str: user input
        """
        user_input = input(message)
        return user_input


class Chatbot:
    """This class handles the general functioning of the chatbot. It asks the user to choose a character, then it creates the conversation, the DaVinci and the user objects. It also handles the conversation, by retrieving the DaVinci's messages and the user's inputs, and by displaying them in the console."""

    # Specific behaviors that DaVinci should adopt, no matter the character. They are used to make the conversation more natural and were listed by doing prompt engineering of the OpenAI API. All the behaviors are used in the conditioning.
    CONDITIONING_BEHAVIOR = [
        "Be specific.",
        "Greet your interlocutor by their name.",
        "Ask questions.",
        "Be friendly.",
        "Introduce yourself and ask a question.",
    ]

    # List of characters that the user can choose. Each character is represented by a tuple containing the name of the character, the description of the character, the temperature of the mode associated with the character, and the name of the Uberduck voice identifier associated with the character.
    CONDITIONING_SITUATION = [
        (
            "Mrs. Smith",
            "an English personnal teacher that is here to teach the basics.",
            1,
            "internetgirl_insight_upper",
        ),
        (
            "Arthur",
            "a 8 year old boy that want to make friends to speak about video games, music and movies.",
            0.8,
            "young-simba",
        ),
        (
            "Jack",
            "an old friend that wants to discuss about common memories.",
            1,
            "red-guy",
        ),
    ]

    def __init__(self) -> None:
        # create the conversation
        self.conversation = Conversation()
        # create the DaVinci chatbot
        self.davinci = DaVinci()
        # create the user
        self.user = User()

        self.situation = None

        print("\033c")  # clear the console before starting

        # ask the user to input his information and choose the situation
        self.ask_name()
        self.ask_mother_tongue()
        self.ask_situation()

        # start the conversation by asking DaVinci to provide a greeting
        davinci_answer = self.davinci.get_answer(
            self.conversation, self.user.name, self.situation[2]
        )
        self.conversation.add_to_history(davinci_answer, is_bot=True)
        self.conversation.display_conversation()

    def ask_situation(self):
        """Ask the user to choose a situation. The situation is used to condition DaVinci."""
        print("\033c")
        print("Welcome to the language chatbot.")
        print("Who do you want to talk with?")
        for i, situation in enumerate(self.CONDITIONING_SITUATION):
            print(f"{i+1}. {situation[0]}, {situation[1]}")
        situation = int(self.user.get_input(">>> "))
        self.situation = self.CONDITIONING_SITUATION[situation - 1]
        self.davinci.name = self.situation[0]
        self.davinci.conditioning = f"You are {self.situation[0]}, {self.situation[1]} "
        self.davinci.conditioning += " ".join(self.CONDITIONING_BEHAVIOR)

    def ask_name(self):
        """Ask the user to input his name. The name is used to condition DaVinci."""
        self.user.name = self.user.get_input("What's your name? : ")
        self.CONDITIONING_BEHAVIOR.append(
            f"Your interlocutor name is {self.user.name}."
        )
        print()

    def ask_mother_tongue(self):
        """Ask the user to input his mother tongue"""
        print("What's your mother tongue?")
        for i, language in enumerate(sorted(tr.languages.values())):
            print(f"{i+1}. {language}")
        language = int(self.user.get_input(">>> "))
        self.user.mother_tongue = sorted(tr.languages.keys())[language - 1]
        print()

    def _update_conversation(self, user_input):
        """Update the conversation by adding the user's input to the conversation and by getting the DaVinci's answer, which is then added to the conversation. The conversation is then displayed.

        Args:
            user_input (str): user's input
        """
        self.conversation.add_to_history(user_input, is_bot=False)
        # get the davinci's answer
        davinci_answer = self.davinci.get_answer(self.conversation, self.user.name, self.situation[2])
        # add the davinci's answer to the conversation
        self.conversation.add_to_history(davinci_answer, is_bot=True)
        # display the conversation
        self.conversation.display_conversation()

    def _execute_command(self, command):
        """Execute a command. The commands are used to access to various functionalities of the chatbot.

        Args:
            command (str): code of the command
        """

        if command == "help":
            print("Commands:")
            print(" - /audio (record an audio message)")
            print(" - /translate_last (translate the last message)")
            print(" - /translate_text (translate an user input text)")
            print(
                " - /generate_vocabulary (generate vocabulary list from the conversation)"
            )
            print(" - /play_last (play an audio of the last message)")
            print(" - /help")
            print(" - /exit")
            print()

        elif command == "exit":
            print("Thanks for using My AI Talking Buddy! See you soon!")
            exit()

        elif command == "audio":  # allow the user to record audio to send to DaVinci
            self.record_audio()  # record audio
            text = ac.speech_to_text()  # convert audio to text with AssemeblyAI API
            self._update_conversation(text)  # update the conversation with the text

        elif (
            command == "translate_last"
        ):  # translate the last message to the user's mother tongue
            last_message = self.conversation.history[-1][0]  # get last message
            translated_message = tr.translate(last_message, self.user.mother_tongue)
            translated_message = textwrap.fill(translated_message, width=80)
            print(translated_message + "\n")

        elif (
            command == "translate_text"
        ):  # translate an user input text to the user's mother tongue, for instance if the user doesn't know how to say something in English
            text = self.user.get_input("Text to translate: ")
            translated_message = tr.translate(text, "en")
            translated_message = textwrap.fill(translated_message, width=80)
            print(translated_message + "\n")

        elif (
            command == "generate_vocabulary"
        ):  # generate vocabulary from the conversation
            messages = [message for message, is_bot in self.conversation.history]
            words = [word for message in messages for word in message.split()]
            vocabulary = sorted(set(words))
            # for each word in the vocabulary, check if it is in the list ressources/nounlist.txt
            # the nounlist.txt file contains a list of common nouns in English
            with open("ressources/nounlist.txt", "r") as f:
                nouns = f.read().splitlines()
            vocabulary = [word for word in vocabulary if word in nouns]
            # save the vocabulary in a file with the translation for each word in the user's mother tongue and display the content of the file in the terminal
            with open("ressources/vocabulary.txt", "w") as f:
                for word in vocabulary:
                    f.write(f"{word} - {tr.translate(word, self.user.mother_tongue)}\n")
            with open("ressources/vocabulary.txt", "r") as f:
                print(f.read())

        elif command == "play_last":  # play an audio of the last message
            last_message = self.conversation.history[-1][0]
            ac.text_to_speech(
                text=last_message, voice=self.situation[3]
            )  # generate an audio file with Uberduck AI API
            ac.play_audio(fpath_audio=ac.FPATH_DUCK_AUDIO)  # play the audio file

        else:
            print("> Command not found")

    def record_audio(self):
        """Record an audio message"""
        print("> Recording audio... (press ctrl+c to stop)")
        ac.record_audio()
        print("> Audio recorded successfully\n")

    def continue_chat(self):
        """Continue the chat by getting the user input and updating the conversation"""
        # get the user input
        user_input = self.user.get_input(">>> ")
        # check if the user input is a defined command
        if user_input.startswith("/"):
            # run the command
            self._execute_command(user_input[1:])
        # add the user input to the conversation
        else:
            self._update_conversation(user_input)

    def chat(self):
        """Start the chat"""
        while True:
            self.continue_chat()


if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.chat()
