# Chatroom Socket/Threading Project

## Overview
This project is a simple multi-client chatroom built using Python sockets and threading.  

It includes a server that manages connections and a client that allows users to join and send messages.

## Features
- Username + passcode authentication  
- Multi-user chat broadcasting  
- Direct messaging between users  
- Active user list lookup  
- Time commands and simple emoji-style status commands  

## Files
- `server.py` – Runs the chat server and manages connected clients  
- `client.py` – Connects users to the server and handles sending/receiving messages  

## Requirements
- Python 3.x  
- Standard libraries only (socket, threading, argparse, json, etc.)

## How to Run

### Start Server
```
python server.py -start -port <PORT> -passcode <PASSCODE>
```

### Start Client
```
python client.py -join -host <HOST> -port <PORT> -username <USERNAME> -passcode <PASSCODE>
```

Example:
```
python server.py -start -port 1234 -passcode 123

python client.py -join -host 127.0.0.1 -port 1234 -username user1 -passcode 123
```

## Commands (In Chat)
- `:]` → happy status  
- `:[` → sad status  
- `:mytime` → show current server time  
- `:+1min` → show current time + 1 minute  
- `:Users` → list active users
- `:dm <username> <message>` → direct message  
- `:Exit` → leave chat  
