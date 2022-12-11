"""This module contains functions for recording audio, converting it to text, and generating audio from text. It uses the following APIs: AssemblyAI, UberDuck."""

import queue
import sys
import sounddevice as sd
import soundfile as sf

import requests
import time
from api_secrets import API_KEY_ASSEMBLYAI, API_KEY_UBERDUCK, API_SECRET_UBERDUCK

import sounddevice as sd
import soundfile as sf
import uberduck


RECORDING_PRM = {
    "samplerate": 16_000,
    "channels": 1,
}
FPATH_RECORD = "tmp/request.mp3"
CHUNK_SIZE = 5_242_880  # 5MB
q = None

# Uberduck
FPATH_DUCK_AUDIO = "tmp/duck_audio.wav"
duck = uberduck.UberDuck(API_KEY_UBERDUCK, API_SECRET_UBERDUCK)

# AssemblyAI
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
headers_auth_only = {"authorization": API_KEY_ASSEMBLYAI}
headers = {"authorization": API_KEY_ASSEMBLYAI, "content-type": "application/json"}


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())


def record_to_file():
    try:
        with sf.SoundFile(
            FPATH_RECORD, mode="w", format="MP3", **RECORDING_PRM
        ) as file:
            with sd.InputStream(**RECORDING_PRM, callback=callback):
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)


def record_audio():
    global q
    q = queue.Queue()
    record_to_file()


def upload(filename):
    def read_file(filename):
        with open(filename, "rb") as f:
            while True:
                data = f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    upload_response = requests.post(
        upload_endpoint, headers=headers_auth_only, data=read_file(filename)
    )
    return upload_response.json()["upload_url"]


def transcribe(audio_url):
    transcript_request = {"audio_url": audio_url}

    transcript_response = requests.post(
        transcript_endpoint, json=transcript_request, headers=headers
    )
    return transcript_response.json()["id"]


def poll(transcript_id):
    polling_endpoint = transcript_endpoint + "/" + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


def get_transcription_result_url(url):
    transcribe_id = transcribe(url)
    while True:
        data = poll(transcribe_id)
        if data["status"] == "completed":
            return data, None
        elif data["status"] == "error":
            return data, data["error"]
        time.sleep(1)


def return_transcript(url):
    data, error = get_transcription_result_url(url)

    if data:
        return data["text"]
    elif error:
        print("Error!!!", error)


def speech_to_text():
    audio_url = upload(FPATH_RECORD)
    return return_transcript(audio_url)


def text_to_speech(text, voice):
    duck.speak(
        speech=text,
        voice=voice,
        return_bytes=False,
        file_path=FPATH_DUCK_AUDIO,
        play_sound=False,
    )


def play_audio(fpath_audio):
    # Extract data and sampling rate from file
    data, fs = sf.read(fpath_audio, dtype="float32")
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing
