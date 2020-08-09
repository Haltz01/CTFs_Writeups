<?php
ini_set('display_errors', 'on');
ini_set('error_reporting', E_ALL);

function sanitize($id, $table) {
    /* Rock-solid: https://secure.php.net/manual/en/function.is-numeric.php */
    if (! is_numeric ($id) or $id < 2) {
        exit("The id must be numeric, and superior to one.");
    }

    /* Rock-solid too! */
    $special1 = ["!", "\"", "#", "$", "%", "&", "'", "*", "+", "-"];
    $special2 = [".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]"];
    $special3 = ["^", "_", "`", "{", "|", "}"];
    $sql = ["union", "0", "join", "as"];
    $blacklist = array_merge ($special1, $special2, $special3, $sql);
    foreach ($blacklist as $value) {
        if (stripos($table, $value) !== false)
            exit("Presence of '" . $value . "' detected: abort, abort, abort!\n");
    }
}

if (isset ($_POST['submit']) && isset ($_POST['user_id']) && isset ($_POST['table'])) {
    $id = $_POST['user_id'];
    $table = $_POST['table'];

    sanitize($id, $table);

    $pdo = new SQLite3('database.db', SQLITE3_OPEN_READONLY);
    $query = 'SELECT id,username FROM ' . $table . ' WHERE id = ' . $id;
    //$query = 'SELECT id,username,enemy FROM ' . $table . ' WHERE id = ' . $id;

    $getUsers = $pdo->query($query);
    $users = $getUsers->fetchArray(SQLITE3_ASSOC);

    $userDetails = false;
    if ($users) {
        $userDetails = $users;
    $userDetails['table'] = htmlentities($table);
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>#WebSec Level Eleven</title>
    <link rel="stylesheet" href="../static/bootstrap.min.css" />
</head>
    <body>
        <div id="main">
            <div class="container">
                <div class="row">
                    <h1>LevelEleven <small> - User 1 is likely <a href="https://fr.wikipedia.org/wiki/Capitaine_Flam">Cap'tain fla<s>m</s>g</a>.</small></h1>
                </div>
                <div class="row">
                    <p class="lead">
                        This application is used to view the username, with or without the costume, of superheroes, by id.<br>
                        Also, I was told that super-heroes have <em>enemies</em>…<br>
                        <br>
                                    To prevent sql injections, it uses a <em>super-efficient-blacklist-based</em> filter!<br>
                                    No more nasty <mark>UNION</mark> or <mark>JOIN</mark>.<br>
                                    Check the source <a href="./source.php">here </a>.
                    </p>
                </div>
            </div>
            <div class="container">
                <div class="row">
                    <form name="username" method="post" class="form-inline">
                        <div class="form-group">
                            <label for="user_id">User ID:</label>
                            <input type="number" class="form-control" id="user_id" name="user_id" value="2" required>
                        </div>
                        <div class="form-group">
                            <label class="radio-inline" for="costume">With costume </label>
                            <input type="radio" class="form-control" id="costume" name="table" value="costume" checked>

                            <label class="radio-inline" for="civil">Without costume </label>
                            <input type="radio" class="form-control" id="civil" name="table" value="civil">
                        </div>
                        <input type="submit" class="form-control btn btn-default" name="submit">
                    </form>
                </div>
                <?php if (isset ($userDetails) && !empty ($userDetails)): ?>
                <br>
                <div class="row">
                    <p class="well">
                        The hero number <strong><?php echo $userDetails['id']; ?></strong>
                        in <strong><?php echo $userDetails['table']; ?></strong>
                        is <strong><?php echo $userDetails['username']; ?></strong>.
                    </p>
                </div>
                <?php endif; ?>
            </div>
        </div>
        <script type="text/javascript" src="../static/bootstrap.min.js"></script>
    </body>
</html>
