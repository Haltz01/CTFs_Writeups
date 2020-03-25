# FireshellCTF2020_URL_to_PDF - Write-up
Web challenge solved during Fireshell CTF 2020 (by Ganesh - USP)

## Challenge description
``` 
Please test our brand new service.

flag is on /flag

https://urltopdf.fireshellsecurity.team/
```

## Write-up
By analysing the request send from the website to convert the URL into a PDF we discovered that it used WeasyPrint to do this process. Also, there was a RegEx preventing us to send URLs that didn't start with `http://` or `https://` (haven't tried hard to bypass it).

The converting "ignored" tags like `<img>`, `<script>`, `<iframe>`, but after searching about WeasyPrint (which is open-source) we've discovered that it accepted `<link>` tags with `rel=attachment`. Therefore, we've made the server get a file from my server that contained `<link rel=attachment href="file:///flag">`. After that, we've downloaded the resulting PDF and decompressed it. In terminal, we've used `strings decompressed_pdf_file.pdf` and got the flag!

**Flag:** `F#{th4nk5_t0_Ben_Sadeghipour_&_Cody_Brocious}`