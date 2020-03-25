# level28 - 1 point
[Link to the challenge](http://websec.fr/level28)

## Description
```
Guessing is fun!
```
Like a lot of CTF, we're doing some ucucuga guessing challenges now, because everyone loves them.
You can check the source here. 

## Write-up
They provided us the PHP file with the page's source code:

``` PHP
 <?php
if(isset($_POST['submit'])) {
    if ($_FILES['flag_file']['size'] > 4096) {
        die('Your file is too heavy.');
    }
    $filename = md5($_SERVER['REMOTE_ADDR']) . '.php';

    $fp = fopen($['flag_file']['tmp_name'], 'r');
    $flagfilecontent = fread($fp, filesize($_FILES['flag_file']['tmp_name']));
    @fclose($fp);

    file_put_contents($filename, $flagfilecontent);
    if (md5_file($filename) === md5_file('flag.php') && $_POST['checksum'] == crc32($_POST['checksum'])) {
        include($filename);  // it contains the `$flag` variable
    } 
    else {
        $flag = "Nope, $filename is not the right file, sorry.";
        sleep(1);  // Deter bruteforce -> sleeps for 1 seflag_filecond
    }

    unlink($filename);
}
?>
<label for='user_id'>Please upload the <code>flag.php</code> file, and enter its checksum:</label>
<form action='' method='post' enctype='multipart/form-data' class="form-inline">
    <div class='form-group'>
        <label class="btn btn-default">
            Select file <input type='file' name='flag_file' id='flag_file' hidden class="hidden">
        </label>
    </div>
    <div class="form-group">
        <div class="input-group">
        <div class="input-group-addon">checksum</div>
        <input type='text' name='checksum' id='checksum' class="form-control"> <br>
    </div>
    </div>
    <div class="form-group">
    <input type='submit' value='Upload and check' class="btn btn-default" name='submit'>
    </div>
</form>

<div class='container'>
    <p class="well"><?php if (isset($flag)){ echo $flag; } else { echo 'Can you guess it?'; }?></p>
</div>

```

`http://websec.fr/level28/flag.php` exists (returns `200 OK` code) and it has 368B


https://www.php.net/manual/en/function.md5-file.php