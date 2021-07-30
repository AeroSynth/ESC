#example to read, access, and print a json file

import json
import os

def language_select(n: int):
    global language_choice
    language_choice = n
    phrase_select(3)#phrase_choice)
        
def phrase_select(n: int):
    global phrase_choice,language_choice
    phrase_choice = n
    print(phrase_choice)
    if n is not None and language_choice is not None:
        ll = data['languages'][get_languages()[language_choice]]
        file_list = [ os.path.join('data', ll['dir'], x['file']) for x in ll['phrases'] ]

        if n < len(file_list):
            print(file_list[n])
        else:
            print("error load_sound {}".format(n))

def get_languages():
    return list(data['languages'].keys())

#def main():
f= open('config.json',encoding='utf8')
#load the json file into data as a dictionary
data = json.load(f)
language_choice=0

#if __name__ == '__main__':
#    main()

