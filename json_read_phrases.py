#simple json to read phrases
#although it's a lot easier to define a string array

import json
import inspect

# json list -- need to use //n for carriage return (javascript)
a='{"phrase":["1...2...3...4...5\\n6...7...8...9...10", \
"Ducks are great!", \
"Have a nice day", "Hello", "How are you?", \
"My name is ...\\nWhat is your name?"]}'

# string list
b=["1...2...3...4...5\n6...7...8...9...10", \
"Ducks are great!", \
"Have a nice day", \
"Hello", "How are you?", \
"My name is ...\nWhat is your name?"]

def json_list():
    
    y=json.loads(a)
    for i in y ['phrase']:
        print(i)
    print()
    simple_list()

def simple_list():
    global callstack,callee
    for i in range(0,len(b)):
        print(b[i])
    #find who called me
    callee=inspect.stack()
    callstack=callee[1]
    print()
    print("My caller is '",callstack[3],"'")

def foo(j):
    print(j)
    
json_list()
