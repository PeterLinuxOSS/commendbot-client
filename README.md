# commendbot-client

Client agent of the **CommendBot** system. It runs on the end machine where it drives Steam and CS2
(starting/stopping `steam.exe` and `csgo.exe`, logging in accounts and performing commends) and
communicates with the server-side **[commendbot-panel](https://github.com/PeterLinuxOSS/commendbot-panel)**
over sockets. The panel launches this client and dispatches tasks to it automatically.

## Components
- `V0.2/` — current client (CustomTkinter GUI + core)
- `run/` — launcher / runtime that talks to the panel
- `lib/cfg/` — CS2 config files (GSI, autoexec)

## CommendBot family
- **commendbot** — core bot (commend logic)
- **commendbot-panel** — server-side control panel (dispatches & manages clients)
- **commendbot-client** — client agent running on the machine (drives Steam/CS2)
- **commendbot-slots** — slot-based instance manager
- **shopmanager** — Discord sales/order bot (keys, licenses)

_Part of the gameboosting service ecosystem._

> Game servers and login credentials were removed from the public version — add your own in the config.
