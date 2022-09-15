import socket, os
from crypt import cryption

# Utility Functions to send and recieve data
def send(toSend):
	# Adding "cryptInd" as header and encypting the message before sending
    client.send((cryptInd + cryption[cryptInd](toSend, 2)).encode("utf-8"))

def recv(bufferSize):
	# Extracting "cryptInd" from header and decypting the message on receiving
    res = client.recv(bufferSize).decode('utf-8')
    res = cryption[res[0]](res[1:], -2)
    return res

# DEFINING SERVER AND PORT ADDRESSES
# YOU CAN GET SERVER IP WHEN RUNNING server.py "LISTENING AT ....."
# SERVER = socket.gethostbyname(socket.gethostname()) # Can be used when running on same system
SERVER = '10.7.52.153' # Used when running on different system(or VM)
PORT = 55555

# ESTABLISHING SOCKET AND CONNECTING TO SERVER
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

# Recieving connection message from server
res = recv(1024)
print(f'[SERVER]: {res}')

# SETTING UP MODE FOR ENCRYPTION WHICH IS ALSO SEND AS HEADER TO SERVER
cryptInd = '2'
connected = True
while connected:
    # READING COMPLETE COMMAND FROM USER
    command = input('[CLIENT]: ')
    command = command.strip()

    # SKIP ON EMPTY COMMANDS
    if len(command) == 0:
        continue

    #? COMMAND "chcrypt <0-2>": CHANGE CURRENT MODE OF 
    #? ENCRYPTION TO INTEGER BETWEEN 0-2
	# 0 -> Plain Text
	# 1 -> Caesar Cipher(Substitution)
	# 2 -> Transpose
    if command[0:7] == 'chcrypt':
        if ' ' in command:
            cryptInd = command.split()[1]
            print("Crypt mode changed to " + cryptInd)
        else:
            print("NOK: Give a integer between 0 to 2 with command")
        continue
	
    #? COMMAND "shcrypt": SHOW CURRENT MODE OF ENCRYPTION
    if command[0:7] == 'shcrypt':
        print("Crypt mode is " + cryptInd)
        continue

    
    #? COMMAND "upd <filename>"": UPLOAD <filename> TO SERVER
    if command[0:3] == "upd":
        # PATH GETS THE FILENAME AND CONDITIONAL TO CHECK
        # IF FILE EXITS IN THE CLIENT TO UPLOAD
        path = command.split()[1]
        if(os.access(path, os.F_OK)):
            # IF FILE EXISTS SEND COMMAND TO SERVER 
			# ELSE DISPLAY STATUS NOK AND CONTINUE
            send(command)
            file = open(path, 'rb')
            filesize = os.path.getsize(path)

            # SEND FILE SIZE TO SERVER
            send(str(filesize))
            res = recv(1024)

            # IF SERVER RECIEVED FILE SIZE THEN CONTINUE TRANSMISSION
            if res[0:2] == "OK":
                
                # SENDING FILEDATA IN CHUNKS TO ACCOMODATE VARIABLE FILE SIZE
                while filesize > 0:
                    # SENDING 2048 BYTES OF DATA
                    filedata = file.read(2048)
                    client.send((cryptInd.encode("utf-8") + cryption[cryptInd](filedata, 2)))
                    filesize = filesize - 2048
                    # RECEIVING CONFIRMATION
                    res = recv(1024)
                    while res[0:3] == "NOK":
                        client.send((cryptInd.encode("utf-8") + cryption[cryptInd](filedata, 2)))
                        res = recv(1024)
            else:
                print('NOK: There was error in sending file size')
            file.close()
        else:
            print('NOK: The path does not exists')
            continue
        
        # PRINTING RESPONSE FROM SERVER
        res = recv(1024)
        print(f'[SERVER]: {res}')
        continue

    #? SEND COMMANDS OTHER THAN upd(UPLOAD FILE)
    send(command)
    res = recv(1024)

    #? COMMAND "dwd <filename>": DOWNLOAD <filename> FROM SERVER
    if command[0:3] in "dwd":
        # IF RESPONSE STATUS IS NOK(server.py) -> EXIT
        if 'NOK:' not in res:
            command, path = command.split()
            filesize = int(res)

            if filesize > 0:
                send("OK: Filesize recieved")
            else:
                send("NOK: Filesize error")
                break
            
            file = open(path, "wb")
            bufferSize = 2048
            # RECIEVING FILE IN CHUNKS
            while filesize > 0:
                res = client.recv(2052)
                res = cryption[str(res[0] - 48)](res[1:], -2)
                file.write(res)
                filesize = filesize - bufferSize
                # SENDING CONFIRMATION FOR EACH PACKET
                send("OK: Packet recieved")
            
            file.close()
            res = recv(1024)

    
    print(f'[SERVER]: {res}')

    # EXIT LOOP AND CLOSE CONNECTION ON FOLLOWING COMMANDS
    if(command == 'quit' or command == 'exit'):
        connected = False


client.close()
