# Mysqlimit
### TetCTF 2021

We had access to the source code (check [sourcecode.php](https://github.com/Haltz01/CTFs_Writeups/blob/master/2021_TetCTF/mysqlimit/sourcecode.php)). Afte reading it, we can assume that we must bypass the filter to do some kind of SQL Injection...

Testing `id=1` we get "handsome_flag" as query result. Similarly, `id=2` returns "ugly_flag" and `id=3` "amazing_goodjob_flag"

Tried id=(SELECT%201%20FROM%20flag_here_hihi%20LIMIT%201) and it gave me a result. Possibly, we can do a Blind SQL Injection to get the first column's name (which contains the flag) (??)

When we cause an error, we discover we're dealing with MySQL.

We can use something like id=(SELECT 0x31), but I don't know how to exploit this (and even if we can)... 
_This idea will be important (using hex values instead of ASCII chars)_

Tried to use `/**/` but it doesn't work - gives an error with `UNIO/**/N` and don't pass the filter using `UNI/**/ON` or any other combination.

Using `GROUP BY 1`, the page returns `Expression #2 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'flag_here_hoho.flag_here_hihi.t_fl4g_name_su' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by`. That's great! Now we know:
- Column we are getting as response has name "t_fl4g_name_su"
- Database/Schema name = "flag_here_hoho"
- Table name = "flag_here_hihi"

Using `GROUP BY 2`, the page returns another similar error: `Expression #3 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'flag_here_hoho.flag_here_hihi.t_fl4g_v3lue_su' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by`. That's even better, because we discovered that the flag value is in column "t_fl4g_v3lue_su"!!

Returning to the idea of Blind SQL Injection, we can start guessing which one is the correct flag and how it's written.
"AND" is blocked, so we can use "&&": `id=1%26%26true` returns handsome_flag; `id=1%26%26false` returns nothing. Nice.

Now, we must find a way to start guessing chars from the flag.
We can use STRCMP() to compare strings. We don't know the real flag value, so we can use the column name and start comparing with all characters.
STRCPM(s1, s2) returns:
- 0 if strings are the same;
- -1 if s1 < s2;
- 1 if s1 > s2.
_Obs.: In MySQL, 0 = false and any non-zero value is true._

We "know" the flag starts with `TetCTF` (probably). Trying `id=1 && STRCPM(t_fl4g_v3lue_su, 'T')` we get an error: `You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '&& STRCMP(t_fl4g_v3lue_su, \'T\')' at line 1`. Our `'` was escaped. That's a problem.

We can use the idea explored earlier. Using hex values instead of literal ASCII chars we can avoid the escaping. T = 0x54. Trying `id=1%26%26STRCMP(t_fl4g_v3lue_su,0x54)` we get "handsome_flag" as a resul, which means that the return value of strcmp() was 1 or -1.

The problem now is that obviouly the flag is greater than "T", so the return value was -1... To avoid this problem and only get a TRUE response when `our_guess >= real_flag` we can add 1 to the result of the strcmp(). By doing this, we'll have: 0 when `flag > our_guess` and 1 or 2 when `our_guess >= real_flag`. Trying `id=1 && 1+STRCMP(t_fl4g_v3lue_su, 0x54)` (URL encoded: `1%26%261%2BSTRCMP(t_fl4g_v3lue_su,0x54)`) we get "handsome_flag" as result, which means our guess is equal or greater than the real flag value. Trying the same test with `id=2` and `id=3` we get nothing, which means that the flag really has `id=1`

I almost forgot one important thing: strcmp() is case-insensitive. So, we must add BINARY before our guess to transform this into a case-sensitive comparison. Correct payload idea -> `1%26%261%2bSTRCMP(t_fl4g_v3lue_su,BINARY%200x54)`

Using a Python script (check [pwn.py](https://github.com/Haltz01/CTFs_Writeups/blob/master/2021_TetCTF/mysqlimit/pwn.py)), we can continue our Blind SQL Injection to discover the entire flag!!

**FLAG: `TetCTF{_W3LlLlLlll_Pl44yYyYyyYY_<3_vina_*100*28904961445554#}`**
