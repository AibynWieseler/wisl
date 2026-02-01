i = 1
while i < 6:
  print(i)
  i += 1 #print i as long as i is less than 6:

#break statement - to exit the loop when conidition is met
i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1

#continue statement - to skip the current iteration when condition is met
i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)

#else statement - to execute a block of code once when the condition is no longer true
i = 1
while i < 6:
  print(i)
  i += 1
else:
  print("i is no longer less than 6")
