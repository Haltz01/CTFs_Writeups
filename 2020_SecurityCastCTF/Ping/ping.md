# PING

URL: `https://ping.fireshellsecurity.team/#`

This chall is about a web application that performs ping requests through its server for you. There's a simple filter trying to restrain the input and turn it into something where the user can only type the IP. However, the filter can be easily passed by avoiding using spaces.

Our payload can be: `1.1.1.1;HOME=/;cd;A=flag;cat<$A`.
With this, the server will:
1. Send a PING message to 1.1.1.1;
2. Redefine `HOME` as `/` (as default, usually you'll have something like `HOME=/home/your_user`);
3. `cd` without a path changes directory to where "HOME" points to, so we move to `/`;
4. Defines `A` as `flag`
5. Shows in the terminal windows the content of flag (`cat flag` = `cat<$A`).

Done! We have the flag!

**Flag: seccast{a598c2d4294ef7309d9a9b32b5342ac744cf234c}**

