import socket, os
from crypt import cryption

# Utility Functions to send and recieve data
def send(toSend):
    conn.send((cryptInd + cryption[cryptInd](toSend, 2)).encode("utf-8"))


def recv(bufferSize):
    res = conn.recv(bufferSize).decode("utf-8")
    res = cryption[res[0]](res[1:], -2)
    return res


# ? COMMAND ls: LIST FILES IN CURRENT DIR
def listfiles(path):
    send(" ".join(os.listdir(path)))


# ? COMMAND cd: CHANGE CURRENT DIR, SEND STATUS OK or NOK
def changeDir(path):
    if os.access(path, os.F_OK):
        os.chdir(path)
        send(f"OK: Directory changed to {os.getcwd()}")
    else:
        send("NOK: This directory does not exist")


# ? COMMAND cwd: RETURN CURRENT WORKING DIRECTORY
def currentDir(path):
    send(f"Current Directory is {os.getcwd()}")


# ? COMMAND "dwd <filename>": DOWNLOAD <filename> FROM SERVER
def downloadFile(path):
    # CHECKING IF FILE EXISTS AND CLIENT HAS READING RIGHTS
    if os.access(path, os.F_OK):
        if os.access(path, os.R_OK):
            file = open(path, "rb")
            filesize = os.path.getsize(path)

            send(str(filesize))
            res = recv(1024)

            # IF FILESIZE IS RECIEVED
            if res[0:2] == "OK":
                # SENDING FILE IN CHUNKS
                while filesize > 0:
                    filedata = file.read(2048)
                    conn.send(
                        (cryptInd.encode("utf-8") + cryption[cryptInd](filedata, 2))
                    )
                    filesize = filesize - 2048
                    res = recv(1024)
                    while res[0:3] == "NOK":
                        conn.send(
                            (cryptInd.encode("utf-8") + cryption[cryptInd](filedata, 2))
                        )
                        res = recv(1024)

                send(f"OK: Complete File({path}) Downloaded Successfully")
                file.close()
        else:
            send("NOK: You don't have reading rights for this file.")
    else:
        send("NOK: The path does not exists")


# ? COMMAND "upd <filename>": UPLOAD <filename> TO SERVER
def uploadFile(path):
    # RECIEVING FILE SIZE
    res = recv(1024)
    file = open(path, "wb")
    filesize = int(res)
    if filesize > 0:
        send("OK: Filesize recieved")
    else:
        send("NOK: Filesize error")
        return

    # RECIEVING FILE IN CHUNKS
    bufferSize = 2048
    while filesize > 0:
        res = conn.recv(2052)
        res = cryption[str(res[0] - 48)](res[1:], -2)
        file.write(res)
        filesize = filesize - bufferSize
        send("OK: Packet recieved")

    send(f"OK: Complete File({path}) Uploaded Successfully")
    file.close()


SERVER = socket.gethostbyname(socket.gethostname())
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

server.listen()
print(f"[SERVER] LISTENING at {SERVER}: ")

conn, addr = server.accept()
print(f"[NEW CONNECTION] {addr}")

cryptInd = "0"
send(f"You are connected to ({SERVER})")
commandList = {
    "ls": listfiles,
    "cd": changeDir,
    "cwd": currentDir,
    "dwd": downloadFile,
    "upd": uploadFile,
}

connected = True
while connected:
    data = conn.recv(1024).decode("utf-8")
    data = data.strip()
    if len(data) == 0:
        continue

    cryptInd = data[0]
    print(cryptInd)
    data = cryption[data[0]](data[1:], -2)
    print(f"[CLIENT{addr}] {data}")

    if data == "quit" or data == "exit":
        connected = False
    else:
        command = data
        path = "./"

        # IF RECIEVED COMMAND HAS ARGUEMENT
        if " " in data:
            command, path = command.split()

        if command in commandList.keys():
            commandList[command.lower()](path)
        else:
            send(f"NOK: No such command as {command}")

send("Disconnecting....")
print(f"[CLIENT] {addr} Disconnecting...")
print(f"[SERVER] SHUTTING DOWN... ")
conn.close()
