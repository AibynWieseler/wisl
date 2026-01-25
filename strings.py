print("Hello")
print('Hello')
#strings are summoned by double or single quotes

a = "Hello"
print(a)
#assigning a string to a variable

a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)
#assigning a multiline string to a variable by using three quotes

#we can use slicing to get specific chars from string
b = "Hello, World!"
print(b[2:5]) #from position from 2 to 5, excluded

b = "Hello, World!"
print(b[:5])
#slice From the Start

b = "Hello, World!"
print(b[2:])
#slice To the End

#using negative indexes, we can slice from the end of a string
b = "Hello, World!"
print(b[-5:-2])

#lower, upper, replacing and splitting the string
a = "Hello, World!"
print(a.lower())

a = "Hello, World!"
print(a.upper())

a = "Hello, World!"
print(a.replace("H", "J"))

a = "Hello, World!"
print(a.split(","))

