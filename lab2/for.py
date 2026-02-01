#for loop is used for iterating over a sequence - set, tuple, etc
fruits = ["apple", "banana", "cherry", "pear"]
for x in fruits:
  print(x)

#loop through the letters in the word "banana":
for x in "banana":
  print(x)

#break statement is used almost the same way as in while loop
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
  
#same for continue statement
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

#range function returns a sequence of numbers
for x in range(6):
  print(x)

#nested loop - one loop inside another loop
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:
  for y in fruits:
    print(x, y)