print("hello?")
from revChatGPT.V1 import Chatbot
from TTS.api import TTS
import numpy as np
import os
import requests
import simpleaudio as sa
from datetime import datetime
from newsapi.articles import Articles

import speech_recognition
import pyttsx3


recognizer = speech_recognition.Recognizer()
print('trying now...')
# try:
#   with speech_recognition.Microphone() as mic:
#     recognizer.adjust_for_ambient_noise(mic, duration=0.2)
#     print('listening in...')
#     audio = recognizer.listen(mic)
#     text = recognizer.recognize_google(audio)
#     print(f'Out: {text}.')
# except speech_recognition.UnknownValueError():
#   pass
# print('done.')
def voiceRec():
  try:
    with speech_recognition.Microphone() as mic:
      recognizer.adjust_for_ambient_noise(mic, duration=0.2)
      print('listening in...')
      audio = recognizer.listen(mic, 10, 5)

      print('translating...')
      text = recognizer.recognize_google(audio)

      print(f'Out: {text}.')
  except OSError as e:
    error_message = str(e)
    # Handle the OSError here or convert it to a JSON-serializable format
    error_data = {"error_message": error_message}
    print(error_data)
  return text


modelname = TTS.list_models()[0]
tts = TTS(modelname)

chatbot = Chatbot(config={
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ4dWVzYWxseTNAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsidXNlcl9pZCI6InVzZXItTmVvUUNyWnZhUnJCMEFYSXJaeVpEYnZYIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2RmMmJmMzI5MjM2NzU0MDJjOGNjNGQiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjg3OTczMjI1LCJleHAiOjE2ODkxODI4MjUsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb3JnYW5pemF0aW9uLndyaXRlIn0.x8neYVzdIHbt99X-X3KgVo6XTHWd1FE3K0Alcv4QPivgfhVj9c_B6AzmBDNJSoB6BVjfKZfJxfPUH-70LAsTpe6gxVsMXO8sI92cGCcGDG18tSkgASY8AtFZoqug-88ZwkYx97AEosAPIshXpdOq4bSYOwMBBG2z6MUZ4bPtFaD-MPz-WtOjf2XB9vTNSqb5CVluENUBhircCO5a8l7mJ1oY7c77D0Q8Iy7E2I7yerwtk4JYlv04aI4d36tfP808_rX-7766HST-J2_0vPJcXfJuobQ507QQrYybL46tu8SL4MA3qIvsy6QGoRfWRE4F4sMQlXMFwsXO2iRrrV98xA"
})

# newsAPI_key = '6fc8ca08f8b54f8fa87ccbd0643f1117'
# # # newsapi requests
# load_dotenv()
# api = os.environ.get('api')
# url = f'https://newsapi.org/v2/everything?q=keyword&apiKey=6fc8ca08f8b54f8fa87ccbd0643f1117'
# resp = requests.get(url)
# data = resp.json()
# articles = data.get('articles')
# # title = articles[2]['title']
# for title in articles:
#   print(title['title'])

fullmsg = ''
def ask_chatGPT(p):
  print("inside ask?")
  global fullmsg
  print("Chatbot: ")
  prev_text = ""
  for data in chatbot.ask(p,):
    message = data["message"][len(prev_text) :]
    print(message, end='', flush=True)
    prev_text = data["message"]
    fullmsg += message

  tts.tts_to_file(text= fullmsg, speaker=tts.speakers[1], language=tts.languages[0], speed=1.25, file_path='output.wav')
  print()

timeDat = {}
def parseCommand(comm):
  tokens = comm.strip().split()
  id = comm.strip().split('#')[1]
  type = tokens[0]
  length = len(tokens)
  if type == "add":
    desc = ""
    for i in range(4, length):
      if tokens[i].startswith('#'):
        break
      desc += tokens[i] + ' '
      #store description in dict
    if id not in timeDat: #time is free
      t = datetime.strptime(tokens[2], '%H:%M')
      str_t = t.strftime('%H:%M')
      d = datetime.strptime(tokens[3], '%m/%d/%Y')
      str_d = d.strftime('%m/%d/%Y')
      event = {
        'time' : str_t,
        #datetime.datetime.strptime(tokens[2], '%H:%M'),#2:00
        # 'date' : datetime.datetime.strptime(tokens[3], '%m/%d/%Y'),#04/06/23
        # 'time' : tokens[2], #just show the time the person what to set
        'date' :str_d, #show the date also
        'descript' : desc
      } # time : 2:00, date : 04/06/23, desc : (description)
      timeDat[id] = event
  elif type == "edit":
    if id in timeDat:
      if tokens[2] == 'time':
        t = datetime.strptime(tokens[3], '%H:%M')
        str_t = t.strftime('%H:%M')
        timeDat[id]['time'] = str_t
        # datetime.strptime(tokens[4], '%H:%M')
      elif tokens[2] == 'date':
        d = datetime.strptime(tokens[3], '%m/%d/%Y')
        str_d = d.strftime('%m/%d/%Y')
        timeDat[id]['date'] = str_d
        #datetime.strptime(tokens[3], '%m/%d/%Y')
      else:
        timeDat[id][tokens[2]] = desc
      # timeDat[id][] = #do whatever edits
  elif type == "remove":
    if id in timeDat:
      # timeDat[id].pop(tokens[2], None)
      del timeDat[id]
      #remove id and associated description
  elif type == "print":
    for x in timeDat:
      print("id : ",x)
      for key, value in timeDat[x].items():
        print(key, ':', value)
  else:
    print("Invalid Command")

with open('GPT-prompt-ex.txt', 'r') as file:
  txtData = file.read()
# print(txtData)
# ask_chatGPT("Hello")

p = txtData
ask_chatGPT(p)
# audiopath = os.path.dirname(__file__) + '\output.wav'
audiopath = 'output.wav'
wave_obj = sa.WaveObject.from_wave_file(audiopath)
play_obj = wave_obj.play()
play_obj.wait_done()
os.remove(audiopath)
fullmsg = ''
p = input("Me: ")
print("\n")

while p != "exit":
  p = input("Enter to Record.")
  ask_chatGPT(voiceRec())
  wave_obj = sa.WaveObject.from_wave_file(audiopath)
  play_obj = wave_obj.play()
  play_obj.wait_done()
  os.remove(audiopath)
  for line in fullmsg.split('\n'):
    if 'Command: ' in line:
      eid = line.split('#')[1].removesuffix(']')
      commandin = line.removeprefix('[Command: ').removesuffix(']').split('#')[0] + '#' + str(eid)
      parseCommand(commandin)
  fullmsg = ''
  print(timeDat)
  print('\n')