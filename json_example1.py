#example to read, access, and print a json file

import json

def get_all_values(nested_dictionary):
    for key, value in nested_dictionary.items():
        if type(value) is dict:
            get_all_values(value)
        else:
            print(key, ":", value)

def get_all_keys(d):
    for key, value in d.items():
        yield key
        if isinstance(value, dict):
            yield from get_all_keys(value)

f= open('config.json',encoding='utf8')
#load the json file into data as a dictionary
data = json.load(f)

#this gets all values except for languages.  Not sure why.
get_all_values(data)

#pretty print the json data
print(json.dumps(data, indent=2))

#this actually gets al the keys except thosse below phrases.
#phrases key has multiple keys of the same name (file)
print()
for x in get_all_keys(data):
    print(x)

print()
for i in data:
    for j, k in data[i].items():
        print(j,"->", k)
