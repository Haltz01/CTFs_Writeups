#!/usr/bin/python3

wantedChars = ['$', '_', 'G', 'E', 'T', '[', ']', '1', '2', '(', ')']

availableChars = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '(',
    ')',
    '.',
    '~',
    '^',
    '|',
    '&',
    '+',
    '-',
    '*',
    '/'
]

for char1 in availableChars:
    for char2 in availableChars:
        for char3 in availableChars:
            if (chr(ord(char1) ^ ord(char2) ^ ord(char3)) in wantedChars):
                print(char1 + " ^ " + char2 + " ^ " + char3 + " = " + chr(ord(char1) ^ ord(char2) ^ ord(char3))) 
                wantedChars.remove(chr(ord(char1) ^ ord(char2) ^ ord(char3))) 