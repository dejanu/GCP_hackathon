#!/usr/bin/env python3

from google.cloud import texttospeech

# import pyaudio
# import wave

def list_languages():
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices().voices
    languages = unique_languages_from_voices(voices)

    print(f" Languages: {len(languages)} ".center(60, "-"))
    for i, language in enumerate(sorted(languages)):
        print(f"{language:>10}", end="" if i % 5 < 4 else "\n")


def unique_languages_from_voices(voices):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set

def list_voices(language_code=None):
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")

def text_to_wav(voice_name, text):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    filename = f"{language_code}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{filename}"')


# def play_wavfile(filepath):
#     """ play wav file from filepath"""
#     #define stream chunk   
#     chunk = 1024  

#     #open a wav format music  
#     f = wave.open(filepath,"rb")  
#     #instantiate PyAudio  
#     p = pyaudio.PyAudio()  
#     #open stream  
#     stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
#                     channels = f.getnchannels(),  
#                     rate = f.getframerate(),  
#                     output = True)  
#     #read data  
#     data = f.readframes(chunk)  

#     #play stream  
#     while data:  
#         stream.write(data)  
#         data = f.readframes(chunk)  

#     #stop stream  
#     stream.stop_stream()  
#     stream.close()  

#     #close PyAudio  
#     p.terminate()  

if __name__ == "__main__":
    txt_input=input("Give text to convert to speech...")
    text_to_wav("en-AU-Wavenet-A",txt_input)
    #play_wavfile(r"en-AU.wav")
    