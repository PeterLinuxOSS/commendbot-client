import subprocess
import sys
import os
import socket
import time 
import webbrowser
import a2s
import threading
import shutil
import psutil
import pyautogui
reconnect_timeout = 120
steamid = sys.argv[3]
steam32id = int(steamid) - 76561197960265728
started = False
kill =False
app_path = os.path.join(sys.argv[1], f"steam.exe")
script_dir = os.path.dirname(sys.executable)

gamedata = os.path.join(script_dir,"cfg","game")
cfg = os.path.join(gamedata,"cfg")
local = os.path.join(script_dir,"cfg","local")
rlocal = os.path.join(sys.argv[1],"userdata",str(steam32id),"730","local")
userdata = os.path.join(script_dir,"cfg","userdata")
ruserdata = os.path.join(sys.argv[1],"userdata",str(steam32id),"730","local","cfg")
csgo = os.path.join(sys.argv[2],"csgo")
rcsg = os.path.join(csgo,"cfg")
timer = 0 
trecconect = False
autoreconnect = True

for file_name in os.listdir(local):
	origo_file_path = os.path.join(local, file_name)
	if os.path.exists(origo_file_path):
		target_file_path = os.path.join(rlocal, file_name)
		target_folder_path = os.path.dirname(target_file_path)
		if not os.path.exists(target_folder_path):
			os.makedirs(target_folder_path)
		shutil.copy(origo_file_path, target_file_path)


if not os.path.exists(ruserdata):
    os.makedirs(ruserdata, exist_ok=True)
for file_name in os.listdir(userdata):
	origo_file_path = os.path.join(userdata, file_name)
	if os.path.exists(origo_file_path):
		target_file_path = os.path.join(ruserdata, file_name)
		target_folder_path = os.path.dirname(target_file_path)
		if not os.path.exists(target_folder_path):
			os.makedirs(target_folder_path)
			try:
				shutil.copy(origo_file_path, target_file_path)
			except PermissionError as e:
				print(f"Permission error: {e}")




for file_name in os.listdir(cfg):
		origo_file_path = os.path.join(cfg, file_name)
		if os.path.exists(origo_file_path):
			target_file_path = os.path.join(rcsg, file_name)
			target_folder_path = os.path.dirname(target_file_path)
			if not os.path.exists(target_folder_path):
				os.makedirs(target_folder_path)
			shutil.copy(origo_file_path, target_file_path)
    
    


allserverscs = {
    1: {"ip": "server.example.com", "port": 27994, "password":"CHANGEME"},
    2: {"ip": "server.example.com", "port": 28194, "password":"CHANGEME"},
    3: {"ip": "server.example.com", "port": 27406, "password":"CHANGEME"},
    4: {"ip": "server.example.com", "port": 28441, "password":"CHANGEME"},
    5: {"ip": "server.example.com", "port": 28864, "password":"CHANGEME"}
}
CREATE_NO_WINDOW = 0x08000000
    

def get_server() -> dict:
	beststerver = (0, 9999)
	max_iterations = 5
	num_iterations = 0
	while beststerver[0] == 0 and num_iterations < max_iterations and beststerver[1] >= 1:
		for i in range(0,2):
			for gid, server in allserverscs.items():
				try:
					info = a2s.info((server["ip"], server["port"]),5)
				except:
					print(f"{gid}. not responding")
				else:
					print(f"{gid}. {info.player_count} / {info.max_players} ")
					avg = info.player_count / info.max_players
					if avg < beststerver[1]:
						beststerver = (gid, avg)
			time.sleep(1)
		num_iterations += 1
    
        
        
	if beststerver[0] == 0:
		beststerver = (1,1)
		print("no-connection")
	print(allserverscs[beststerver[0]])
    
	return allserverscs[beststerver[0]]
 

HOST = '127.0.0.1'  # IP address of the host
PORT = 11569  # Port to connect to
first_connect = False 
shutting_msg = "Disconnect: Server shutting down."
relog_msg = "Disconnect: Relog to continue."
timed_msg = "Server connection timed out."
start_msg = "Ping measurement completed"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.sendall(f"id-{steamid}".encode())



def data_loop():
    global reconnect_timeout,s
    while reconnect_timeout >= 0:
        print("data_loop")
        try:
            data = s.recv(1024)
            if not data:
                raise "dissconnected"
        except:
            print("Disconnected from server.")
            s.close()
            while reconnect_timeout >= 0:
                print(f"Trying to reconnect... {reconnect_timeout}s")
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((HOST, PORT))
                except :
                    
                    s.close()
                    reconnect_timeout -= 10
                    time.sleep(10)
                    continue
                else:
                    reconnect_timeout = 60
                    print("Reconnected to server.")
                    s.sendall(f"id-{steamid}".encode())
                    break
            if reconnect_timeout <= 0:
                break
        else:
            edata = data.decode().strip()
            print(f"Received data: {edata}")
            if edata == "ok":
                pass
            elif edata == "reconnect":
                server = get_server()
                webbrowser.open_new(f"steam://connect/{server['ip']}:{server['port']}/{server['password']}")
            elif edata == "close":
                print("Stopping...")
                s.sendall("close".encode())
                kill_app()
            elif edata == "restart":
                global started
                started = False
            elif edata == "open":    
                webbrowser.open_new("steam://rungameid/730")
            
            elif edata == "popen":
                window = pyautogui.getWindowsWithTitle('Steam Sign In')
                if len(window) ==0:
                    time.sleep(5)
                    window = pyautogui.getWindowsWithTitle('Steam Sign In')
                    if len(window) !=0:
                        window = window[0]
                    else:
                        return    
                else:
                    window = window[0]   
                left, top = window.topleft
                width, height = window.size
                region = (left, top, width, height)
                
                s.sendall(("hwnd-"+str(window._hWnd)).encode())
            elif edata.startswith("autoreconnect-"):
                global autoreconnect
                autoreconnect = bool(edata.split("-")[1])
                
                
        finally:
           reconnect_timeout = 60
    print("Stopping csgo and other")
    kill_app()
    sys.exit(1)



    

def kill_app():
    
    for proc in psutil.process_iter():
        if proc.name() == "csgo.exe" or proc.name() == "steam.exe":
            proc.kill()
            
    print("end")
    global kill
    kill = True
    sys.exit(1)
        
    

thread = threading.Thread(daemon=True, name="message", target=data_loop)
thread.start()


gameinfo = """
"GameInfo"
{
	game	"ACCOUNT"
	title	"COUNTER-STRIKE'"
	title2	"GO"
	type multiplayer_only
	nomodels 1
	nohimodel 1
	nocrosshair 0
	bots 1
	hidden_maps
	{
		"test_speakers"		1
		"test_hardware"		1
	}
	nodegraph 0
	SupportsXbox360 1
	SupportsDX8	0
	GameData	"csgo.fgd"


	FileSystem
	{
		SteamAppId				730		// This will mount all the GCFs we need (240=CS:S, 220=HL2).
		ToolsAppId				211		// Tools will load this (ie: source SDK caches) to get things like materials\debug, materials\editor, etc.
		
		//
		// The code that loads this file automatically does a few things here:
		//
		// 1. For each "Game" search path, it adds a "GameBin" path, in <dir>\bin
		// 2. For each "Game" search path, it adds another "Game" path in front of it with _<langage> at the end.
		//    For example: c:\hl2\cstrike on a french machine would get a c:\hl2\cstrike_french path added to it.
		// 3. For the first "Game" search path, it adds a search path called "MOD".
		// 4. For the first "Game" search path, it adds a search path called "DEFAULT_WRITE_PATH".
		//

		//
		// Search paths are relative to the base directory, which is where hl2.exe is found.
		//
		// |gameinfo_path| points at the directory where gameinfo.txt is.
		// We always want to mount that directory relative to gameinfo.txt, so
		// people can mount stuff in c:\mymod, and the main game resources are in
		// someplace like c:\program files\valve\steam\steamapps\<username>\half-life 2.
		//
		SearchPaths
		{
			Game				|gameinfo_path|.
			Game				csgo
		}
	}
}
"""

gameinfo = gameinfo.replace("ACCOUNT",str(steamid))

gameinfo_path = os.path.join(sys.argv[2],"csgo","gameinfo.txt")
console_path = os.path.join(sys.argv[2],"csgo","console.log")
with open(gameinfo_path, "w") as f:
    f.write(gameinfo)


    



command = [ app_path,] + sys.argv[4:]

subprocess.Popen(command,shell=True)
open(console_path, 'w').close()

while True: #porozmyšlal by som o zaimplementovani toho že ked trebarz z csgo cmd niesu žiadne msgs idk 1min tak by som to vyhlasil za to že csgo je vypnute ale zas neviem ako v mainmenu a ako na serveri prichadzaju msgs 
	if kill:
		break
	if os.path.exists(console_path):
		if autoreconnect:
			if os.path.getsize(console_path) > 0:
				
					if not first_connect:
						
						open(console_path, 'w').close()
						first_connect = True
						print("connecting")
						time.sleep(35)
						if kill:
							break
						server = get_server()
						
						webbrowser.open_new(f"steam://connect/{server['ip']}:{server['port']}/{server['password']}")
						
						
						
						
					else:
						
						with open(console_path, encoding='utf-8', errors='ignore') as f:
							lines = f.readlines()
						open(console_path, 'w').close()
						
						if   any(shutting_msg in s or relog_msg in s or timed_msg in s for s in lines):
							print("reconnecting")
							server = get_server()

							trecconect = True
							webbrowser.open_new(f"steam://connect/{server['ip']}:{server['port']}/{server['password']}")

						elif any("Connected to " in s for s in lines):
							if not started: 
								timer = 0 
								started = True
								print("start commending")

								s.sendall("start".encode())
							else:
								trecconect = False
						elif not started or trecconect:
							timer += 20
						elif timer >= 100:
							timer = 0
							print("tring again ")
							server = get_server()
							webbrowser.open_new(f"steam://connect/{server['ip']}:{server['port']}/{server['password']}")
			else:
				print(f"count {trecconect}")
				if first_connect and not started or first_connect and trecconect:
					timer += 20
				elif timer >= 100:
						timer = 0
						print("tring again. ")
						server = get_server()
						webbrowser.open_new(f"steam://connect/{server['ip']}:{server['port']}/{server['password']}")
				
		

	else:
		print("not exist")
	
     
	 
	time.sleep(20)
sys.exit(1)


