input = input()
info = input.split()
dict = {}

for i in range(len(info)):
  if(info[i].lower() == 'add'):
    try:
      description = ''
      for j in range(2, len(info)-i):
        if(info[i+j] != 'add' and info[i+j] != 'edit' and info[i+j] != 'remove'):
          description += info[i+j] + ' '
        else:
          break
      description = description[:-1]
      dict[info[i+1]] = description
    except IndexError:
      print(f"You only enter {len(info)} element, need 3")

  elif(info[i].lower() == 'edit'):
      time = info[i+1]
      if time not in dict:
        print(f"{time} not added yet")
      else:
        try:
            description = ''
            for j in range(2, len(info)-i):
                if(info[i+j] != 'add' and info[i+j] != 'edit' and info[i+j] != 'remove'):
                    description += info[i+j] + ' '
                else:
                    break
            description = description[:-1]
            dict[info[i+1]] = description
        except IndexError:
            print(f"You only enter {len(info)} element, need 3")

  elif(info[i].lower() == 'remove'):
    try:
      dict.pop(info[i+1])
    except KeyError:
      print(f"element {info[i+1]} not in the dictionary!")

print("dictionary: ", dict)