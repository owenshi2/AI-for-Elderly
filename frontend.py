import gradio as gr 
import warnings
from gtts import gTTS
from revChatGPT.V1 import Chatbot
from datetime import datetime
from newsapi.articles import Articles
import speech_recognition as sr
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
# from fastapi import FastAPI


warnings.filterwarnings("ignore")
app = FastAPI()
recognizer = sr.Recognizer()


#change this to your own token!
# chatbot = Chatbot(config={
#   "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ4dWVzYWxseTNAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsidXNlcl9pZCI6InVzZXItTmVvUUNyWnZhUnJCMEFYSXJaeVpEYnZYIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2RmMmJmMzI5MjM2NzU0MDJjOGNjNGQiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjkxMTY2NzAxLCJleHAiOjE2OTIzNzYzMDEsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb3JnYW5pemF0aW9uLndyaXRlIG9mZmxpbmVfYWNjZXNzIn0.o57gnuBHZUkCo48-_65maeWrHF67N98JbYrsLs1OsERhAJpZg4bJ1sncplkR_xlAOUzywRpcpQXpk9luLXRl75rgQEMvcO2Hr4ODxQH5kMlXkR7dzoP9guYqMk6A9lipEZ7Tz5gla0HXAAeSAPlf5VmsevHSaqywwCiokODAeygtYo7oV4d37zOLLYO2DLfIWqXK7EviUmPLYfu50ouT_TI4hDzxq45713jRMHBGNx0jiImToU_LgaNk0HxuLli6Pu5pufdCoHhSg6bmpr-w7LHvOlCa58xq-LebvGKvdrqKp3DM0bJ1NbVktfj-_iUCMen6DRPMwIhbVGfV5Hm_GQ"
# })
chatbot = Chatbot(config = {
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJvd2Vuc2hpMjAxMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1wbE9GR3RxZkZtSzNaU0VuOFpIMEJVeTEifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6ImF1dGgwfDYzYWIxZTM1ZjE0NGQ2NjU3NWU0NzU3NyIsImF1ZCI6WyJodHRwczovL2FwaS5vcGVuYWkuY29tL3YxIiwiaHR0cHM6Ly9vcGVuYWkub3BlbmFpLmF1dGgwYXBwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTE2Mjc5NDAsImV4cCI6MTY5MjgzNzU0MCwiYXpwIjoiVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG1vZGVsLnJlYWQgbW9kZWwucmVxdWVzdCBvcmdhbml6YXRpb24ucmVhZCBvcmdhbml6YXRpb24ud3JpdGUgb2ZmbGluZV9hY2Nlc3MifQ.1FYNQn5Hz_VGY2oC2CcRf4_BpXEmnFIFFrlLnIHopUpZidt2SYa3C-P0nuYDUQqWTreIDDyEPzNaPTJRky0YGqowSJe8yXRXHKLwZT3j94Gf79jwgl-zLtM5H4VOSbMUnyPI0zg0yTpCj7wdDRcoAZ2RPNj0YJNR6McTMWFVq94Mjm-s2TMf6xRMLT3QdPiYXAqn_SrrhI7blr_V9xUaDzf-D4Sd3TtT3i0lAjiM1AURjFJCW1Mrm2M44-7sCvz_obZm5M3QOAzB7NNoNHR2ML6mpF6fO7B2pz_KR7lMx5rEfAfxbGTHa6KOPoVWpTF6ukFt8_1J0UOaj7T0YsO8wQ"
})
altern = True
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
# print(training)



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
    
    audioobj.save(audiopath)
    storeTrans(result_text, out_result, audiopath)
    retrTrans(altern)
    return [result_text, out_result, audiopath]

def storeTrans(r, o, oA):
  global res_text, out_res, out_aud
  res_text = r
  out_res = o
  out_aud = oA
  print(f'info stored. {res_text}, {out_res}')

def retrTrans(flag):
  print('returning...')
  if(flag):
    flag = not flag
    return [res_text, out_res, out_aud]
  flag = not flag
  return [res_text + '?', out_res, out_aud]

output_1 = gr.Textbox(label="Speech to Text")
output_2 = gr.Textbox(label="ChatGPT Output")
output_3 = gr.Audio(audiopath, autoplay=True)

inp = gr.Interface(
    title = 'AI-For-Elderly Chatbot', 
    fn=transcribe,
    inputs=[
        gr.inputs.Audio(source="microphone", type="filepath")
    ],
    outputs=[]
    )
outp = gr.Interface(
    title = 'AI-For-Elderly Chatbot', 
    fn=retrTrans,
    inputs=[],
    outputs=[
        output_1,  output_2, output_3
    ],
    live = True)

INP_ROUTE = '/input'
OUTP_ROUTE = '/output'
OUT_ROUTE = '/out'

#Design

iframe_dimensions = "height=300px width=100% style=\"max-width=600px; margin=auto;\""
bStyle = "bgcolor= \"black\" style=\"color:white; font-family:Roboto; text-align:center\""
brack = '{'

# resizeJS = f'''
# <script>
#         var frame = document.getElementById("IFResize");
          
#         frame.onload = function()
#         {brack}
#           frame.style.height = frame.contentWindow.document.body.scrollHeight + 'px';
#           frame.style.width  = frame.contentWindow.document.body.scrollWidth+'px';  
#         {brack}
# </script>
# '''

button_style = "height:50px; width:500px; background:#FF8000; font-size:1em; color:#000000; padding:6px"

index_html = f'''
<head>
<link href='https://fonts.googleapis.com/css?family=Roboto' rel='stylesheet'>
</head>
<body {bStyle}>
<h1>Voice Recording</h1>
<h3>
Please record your response below.
</h3>
<h3>
When finished, stop recording and click results.
</h3>
<h3>
Events and medications will be added to the calendar.
</h3>
<div>
<iframe src={INP_ROUTE} {iframe_dimensions}></iframe>
</div>
<button style="{button_style}" onclick="window.location.href='{OUT_ROUTE}';">Results</button>
</body>
'''

result_html = f'''
<head>
<link href='https://fonts.googleapis.com/css?family=Roboto' rel='stylesheet'>
</head>
<body {bStyle}>
<div>
<iframe src={OUTP_ROUTE} height=75% width=100%></iframe>
<button style="{button_style}" onclick="window.location.href='/';">Back to Record</button>
</div>
</body>
'''

@app.get("/", response_class=HTMLResponse)
def index():
  return index_html

@app.get(f"{OUT_ROUTE}", response_class=HTMLResponse)
def result():
  return result_html

app = gr.mount_gradio_app(app, inp, path=INP_ROUTE)
app = gr.mount_gradio_app(app, outp, path=OUTP_ROUTE)

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("frontend:app", host="127.0.0.1", port=7860, reload=True)