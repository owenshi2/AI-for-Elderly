from revChatGPT.V1 import Chatbot
from TTS.api import TTS
# from playsound import playsound
import os
import requests
from dotenv import load_dotenv
import simpleaudio as sa
# import revChatGPT
from datetime import datetime
from newsapi.articles import Articles

import speech_recognition
import pyttsx3

recognizer = speech_recognition.Recognizer()
# print('trying now...')
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
  except Exception as e:
    return e
  return text


modelname = TTS.list_models()[0]
tts = TTS(modelname)

chatbot = Chatbot(config={
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJvd2Vuc2hpMjAxMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1wbE9GR3RxZkZtSzNaU0VuOFpIMEJVeTEifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6ImF1dGgwfDYzYWIxZTM1ZjE0NGQ2NjU3NWU0NzU3NyIsImF1ZCI6WyJodHRwczovL2FwaS5vcGVuYWkuY29tL3YxIiwiaHR0cHM6Ly9vcGVuYWkub3BlbmFpLmF1dGgwYXBwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2ODY4OTA5NzIsImV4cCI6MTY4ODEwMDU3MiwiYXpwIjoiVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG1vZGVsLnJlYWQgbW9kZWwucmVxdWVzdCBvcmdhbml6YXRpb24ucmVhZCBvcmdhbml6YXRpb24ud3JpdGUifQ.mgCDn7iumMuQ-cD8ksEwZXCAJad7QAp0iqHOIqfxgd9dewJP5D6fOY64y8gt_foIWtoffoRJYxhHZ39c8Ky71DhU9tdVzr5bdpN0W9EsDP9po5JSiw8PFBf_pYtuxMmvLVSNwHwlbUtQBeqpA0LMhKWvQbizATzJhkqS725-lRudu3E_eyU0DO66Z4jO2_zyi_Kd0ktzh0usm_H8Vd3auYsB2K6sx6BAmrNA-V1HF1iyuYtCJwxd_TmjLR5BfIGXk57M29EfgiGFuHUImEFFQmVoQjKlGPcHyXODQXKfi89bRFPVNxjBwsW1ZGK4rG7NIyffgv-kLCsOgFd1T8Hqjw"
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
# p = input("Me: ")
# print("\n")

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