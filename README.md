# CS433-Assignment1

### Overview:
To understand the concepts of computer networking and learning how communication happens progress between two systems a python based server-client system is implemented in this assignment. It uses the TCP protocol for communication and supports five different commands at the client side.

1. cwd
2. ls
3. cd <dir>
4. dwd <file>
5. upd <file>

Working and explaination in DESIGNDOC file.
----

### How to run?
  > If files are running on same system
  * Download the code from the repo.
  * Run server.py with `python server.py`
  * Run client.py with `python client.py`
  * Enter commands as input to client.py
  
  > If files are running on different system (I tried on WSL:Ubuntu)
  * Download the code from the repo.
  * Run server.py with `python server.py`
    * Copy the IP address shown at terminal after running server.py for e.g, `[SERVER] LISTENING at 10.xx.xx.xx: `
  
  * Open client.py in any text editor
  * Comment line 17 and uncomment line 18
  * Paste the IP address on line 18 for e.g, `SERVER = '10.xx.xx.xx'`
