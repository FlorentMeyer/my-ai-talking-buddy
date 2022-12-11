"""This module contains the functions to translate text from one language to another"""

from deep_translator import GoogleTranslator

# dictionary of languages
languages = {"fr": "français", "es": "español", "de": "deutsch", "it": "italiano"}


def print_languages():
    """enumerate the possible languages in alphabetical order"""
    for i, language in enumerate(sorted(languages.values())):
        print(f"{i+1}. {language}")


def translate(text, target_language):
    return GoogleTranslator(source="auto", target=target_language).translate(text)
