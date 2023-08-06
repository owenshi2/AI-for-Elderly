import whisper
import gradio as gr 
import time
import warnings
import json
import os
import ffmpeg
from gtts import gTTS
from revChatGPT.V1 import Chatbot
from TTS.api import TTS
# from playsound import playsound
import os
import requests
# from dotenv import load_dotenv
import simpleaudio as sa
# import revChatGPT
from datetime import datetime
from newsapi.articles import Articles

import speech_recognition
import pyttsx3
import gradio as gr
from transformers import pipeline

warnings.filterwarnings("ignore")

recognizer = speech_recognition.Recognizer()
modelname = TTS.list_models()[0]
tts = TTS(modelname)

#change this to your own token!
chatbot = Chatbot(config={
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ4dWVzYWxseTNAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsidXNlcl9pZCI6InVzZXItTmVvUUNyWnZhUnJCMEFYSXJaeVpEYnZYIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2RmMmJmMzI5MjM2NzU0MDJjOGNjNGQiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjkxMTY2NzAxLCJleHAiOjE2OTIzNzYzMDEsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb3JnYW5pemF0aW9uLndyaXRlIG9mZmxpbmVfYWNjZXNzIn0.o57gnuBHZUkCo48-_65maeWrHF67N98JbYrsLs1OsERhAJpZg4bJ1sncplkR_xlAOUzywRpcpQXpk9luLXRl75rgQEMvcO2Hr4ODxQH5kMlXkR7dzoP9guYqMk6A9lipEZ7Tz5gla0HXAAeSAPlf5VmsevHSaqywwCiokODAeygtYo7oV4d37zOLLYO2DLfIWqXK7EviUmPLYfu50ouT_TI4hDzxq45713jRMHBGNx0jiImToU_LgaNk0HxuLli6Pu5pufdCoHhSg6bmpr-w7LHvOlCa58xq-LebvGKvdrqKp3DM0bJ1NbVktfj-_iUCMen6DRPMwIhbVGfV5Hm_GQ"
})

p = pipeline("automatic-speech-recognition")
audiopath = 'Temp.mp3'

def voiceRec(audio):
    text = p(audio)["text"]
    return text


def ask_chatGPT(p):
  fullmsg = ''
  # print("Chatbot: ")
  prev_text = ""
  for data in chatbot.ask(p,):
    message = data["message"][len(prev_text) :]
    # print(message, end='', flush=True)
    prev_text = data["message"]
    fullmsg += message

  return fullmsg

#train gpt to understand some prompt!
# with open('GPT-prompt-ex.txt', 'r') as file:
#   txtData = file.read()
# # print(txtData)
# # ask_chatGPT("Hello")

# p = txtData
# # ask_chatGPT(p)
# print("prompt: ", ask_chatGPT(p))


def transcribe(audio):
    language = 'en'
    result_text = voiceRec(audio)
    
    out_result = ask_chatGPT(result_text)
    
    audioobj = gTTS(text = out_result, 
                    lang = language, 
                    slow = False)
    
    audioobj.save("Temp.mp3")

    return [result_text, out_result, "Temp.mp3"]

output_1 = gr.Textbox(label="Speech to Text")
output_2 = gr.Textbox(label="ChatGPT Output")
output_3 = gr.Audio("Temp.mp3")

gr.Interface(
    title = 'AI-For-Elderly Chatbot', 
    fn=transcribe, 
    inputs=[
        gr.inputs.Audio(source="microphone", type="filepath")
    ],

    outputs=[
        output_1,  output_2, output_3
    ],
    share=True).launch()

os.remove(audiopath)



