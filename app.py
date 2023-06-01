# python3 app.py

from datetime import datetime
#stores event data
# timeDat = {id:event}
timeDat = {}
IDs = []
commandValid = True

while commandValid == True:
  commandValid = True
  # add event (time) (date) (description) #id
  # edit event (key) (new value) (#id)
  # print (#id)   e.g: print #e123 #e124
  # remove event (#id)
  inp = input("Type your command: ")
  
  # add event 2:00 04/06/2023 therapy session #e1234
  # edit event time 3:30 #e1234
  # remove event #e1234
  tokens = inp.strip().split()
  id = inp.strip().split('#')[1]
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
    commandValid = False
  

