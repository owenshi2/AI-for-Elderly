import gradio as gr 
import warnings
import os
from gtts import gTTS
from revChatGPT.V1 import Chatbot
import os
from datetime import datetime
from newsapi.articles import Articles

import speech_recognition as sr
import gradio as gr

warnings.filterwarnings("ignore")

recognizer = sr.Recognizer()

#change this to your own token!
chatbot = Chatbot(config={
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ4dWVzYWxseTNAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsidXNlcl9pZCI6InVzZXItTmVvUUNyWnZhUnJCMEFYSXJaeVpEYnZYIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2RmMmJmMzI5MjM2NzU0MDJjOGNjNGQiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjkxMTY2NzAxLCJleHAiOjE2OTIzNzYzMDEsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb3JnYW5pemF0aW9uLndyaXRlIG9mZmxpbmVfYWNjZXNzIn0.o57gnuBHZUkCo48-_65maeWrHF67N98JbYrsLs1OsERhAJpZg4bJ1sncplkR_xlAOUzywRpcpQXpk9luLXRl75rgQEMvcO2Hr4ODxQH5kMlXkR7dzoP9guYqMk6A9lipEZ7Tz5gla0HXAAeSAPlf5VmsevHSaqywwCiokODAeygtYo7oV4d37zOLLYO2DLfIWqXK7EviUmPLYfu50ouT_TI4hDzxq45713jRMHBGNx0jiImToU_LgaNk0HxuLli6Pu5pufdCoHhSg6bmpr-w7LHvOlCa58xq-LebvGKvdrqKp3DM0bJ1NbVktfj-_iUCMen6DRPMwIhbVGfV5Hm_GQ"
})

audiopath = 'Temp.mp3'


def voiceRec(audio):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio) as source:
        # Adjust for ambient noise for better recognition
        recognizer.adjust_for_ambient_noise(source)
        print("Converting audio to text...")

        try:
            # Listen to the audio and convert it to text
            text = recognizer.recognize_google(audio_data=recognizer.record(source), language="en-US")
            return text

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None

        except sr.RequestError:
            print("Sorry, there was an issue connecting to Google's servers.")
            return None



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
training = ask_chatGPT(p)
print(training)



def transcribe(audio):
    language = 'en'
    result_text = voiceRec(audio)
    
    out_result = ask_chatGPT(result_text)
    
    for line in out_result.split('\n'):
      # print("hi")
      if 'Command: ' in line:
        eid = line.split('#')[1].removesuffix(']')
        commandin = line.removeprefix('[Command: ').removesuffix(']').split('#')[0] + '#' + str(eid)
        parseCommand(commandin)

    
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



