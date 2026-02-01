#Lists are used to store multiple items in a single variable.
thislist = ["apple", "banana", "cherry"]
print(thislist)

#they are ordered, changeable, and allow duplicate values.
thislist = ["apple", "banana", "cherry", "apple", "cherry"]
print(thislist)

#list length
thislist = ["apple", "banana", "cherry"]
print(len(thislist))

#list() constructor
thislist = list(("apple", "banana", "cherry")) # note the double round-brackets
print(thislist)

#changing the value of a specific item
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]
thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist)

#inserting at specific position
thislist = ["apple", "banana", "cherry"]
thislist.insert(2, "watermelon")
print(thislist)