# level25 - 1 point
[Link to the challenge](http://websec.fr/level25)

## Description
```
Nobody listen to techno, nor to wrap music.
```
You can include any page so long as it is black not the flag.txt one. As usual, the source code is free.

## Write-up
They provided us the PHP file with the page's source code:

``` PHP
// I only kept the parts that looked important...

<?php
if (!isset($_GET['page'])) {
  header('Location: http://websec.fr/level25/index.php?page=main');
  die();
}
?>

// Random commentary
<!--
    Yeah, the webserver is configured so that you can't directly access .txt files :)
    And no, PHP wrappers aren't the only way to have fun!
-->

// Form to include the page we wanted (as a .txt)
<label for='user_id'>Enter the page you want to include:</label>
<form name='username' method='get'>
    <div class='form-group col-md-2'>
        <input type='text' class='form-control' id='page' name='page' value='main' required>
    </div>
    <div class='col-md-2'>
        <input type='submit' class='form-control btn btn-default' name='send'>
    </div>
</form>

// Most important part!! 
<?php
parse_str(parse_url($_SERVER['REQUEST_URI'])['query'], $query);
foreach ($query as $k => $v) {
    if (stripos($v, 'flag') !== false) # I need to bypass this...
        die('You are not allowed to get the flag, sorry :/');
}

include $_GET['page'] . '.txt'; # ...and include flag.txt!
?>
```

From the parse_url() [documentation](https://www.php.net/manual/en/function.parse-url.php) we see that `On seriously malformed URLs, parse_url() may return FALSE.`. If we pass a malformed URL to this function, `$query` will become `FALSE` and the `foreach` won't kill the script with the `die()` command. Thus, the `include $_GET['page'] . '.txt';` will be executed, including whatever page we want.

URLs need to conform to the spec which is, more or less, scheme: `[//[user:password@]host[:port]][/]path[?query][#fragment]`. From a [StackOverflow question](https://stackoverflow.com/questions/47807529/how-to-avoid-php-parse-url-return-false-when-parse-sa-12b-12-3-3-41233-whi), I got an example of a malformed URL with the query as `a=12&b=12.3.3.4:123`. The problem is the `:` symbol there.

With this in mind, we make a request to the server with this URL: `http://websec.fr/level25/index.php?page=flag&a=12&b=12.3.3.4:1233`
And... It works!! We were able to get the flag!

**FLAG: `WEBSEC{How_am_I_supposed_to_parse_uri_when_everything_is_so_broooken}`**

---
#### Links that really helped me understand better what was going on:
https://www.php.net/manual/en/function.parse-url.php
https://www.php.net/manual/en/function.parse-str.php
https://www.php.net/manual/en/control-structures.foreach.php
https://www.php.net/manual/en/function.stripos.php
https://stackoverflow.com/questions/47807529/how-to-avoid-php-parse-url-return-false-when-parse-sa-12b-12-3-3-41233-whi