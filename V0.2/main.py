

import random
import signal
import subprocess
from threading import current_thread,enumerate as t_enumerate
import threading
import webbrowser
from customtkinter import *
from tkinter import  BitmapImage, Button, PhotoImage, messagebox,Canvas,Frame
import pyautogui
from tzlocal import get_localzone
from termcolor import colored,cprint
import regobj
import win32gui
from PIL import Image, ImageTk
from steam import steamid
loopcount = 0
premium = False
import time
import a2s
import pyperclip
import datetime
from tkinter import Widget
from pymongo import MongoClient,ReturnDocument,ASCENDING,DESCENDING
from tkinter import filedialog
import  sys, traceback
import socket
import vdf
event = threading.Event()
from steam import guard
from base64 import b64decode
local = get_localzone()
tz = datetime.timezone(datetime.timedelta(hours=0))
datetime_utc = datetime.datetime.now(tz=tz)
datetime_local = datetime.datetime.now(local)
servers = {}
logs =[]
accounts = {}
csgo_started = None

stop_server = False
CREATE_NO_WINDOW = 0x08000000
HOST = '127.0.0.1'  # IP address of the host
PORT = 11569  # Port to connect to
clients = {}
check_verify = {}
wincounter = 0
version = "2.6.3"
print(version)
def start_server():
    global stop_server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        # Bind the socket to the address and port
        try:
            s.bind((HOST, PORT))
        except Exception as ex:
            print(ex)
            messagebox.showerror("Another panel currently running ","Another panel currently running!")
            os._exit(1)
        # Listen for incoming connections
        s.listen()
        print(f'Server started')
        while True:
            if stop_server:
                break
            # Accept a new client connection
            conn, addr = s.accept()
            # Start a new thread to handle the client
            client_thread = Thread(target=handle_client, args=(conn, addr))
            client_thread.start()


def handle_client(conn: socket.socket, addr):
    steamid = 0
    with conn:
        print(f'Connected by {addr[1]}')
        
        while True:
            # Receive data from the client
            try:
                
                data = conn.recv(1024)
            except:
                break
            
            edata = str(data.decode())
            if edata.startswith("id-"):
                steamid = int(edata.replace("id-",""))
                clients[steamid] = conn
                conn.sendall(f"autoreconnect-{int(auto_reconnect)}".encode())
                print(f"With {steamid}")
            elif edata == "start" and steamid != 0:
                if auto_start == True:
                    acc = db.serverusers.find_one({"steamID64":steamid})
                    if acc:
                        start_waiting(acc)
                    else:
                        print(f"is not in acc db {steamid}")
                    if steamid in accounts:
                        accounts[steamid]["started"] = True
                else:
                    print("Not enabled auto_start, I cant auto-start.")
            elif edata == "check":
                conn.sendall("ok".encode())
            elif edata == "close":
                
                conn.close()
                print(f"Connection closed by client {steamid}")
                break
            elif edata.startswith("hwnd-"):
                if not steamid in accounts:
                    return
                shared_secret = accounts[steamid]["shared_secret"]
                
                code = guard.generate_twofactor_code(b64decode(shared_secret))
                if is_number(edata.split("-")[1]):
                    hwnd = int(edata.split("-")[1])
                    try:
                        win32gui.SetForegroundWindow(hwnd)
                    except:
                        print("retry-window is invalid")
                        time.sleep(2)
                        conn.sendall("popen".encode())
                    else:    
                        rect = win32gui.GetClientRect(hwnd)

                        # get the screen coordinates of the top-left corner of the client area
                        x, y = win32gui.ClientToScreen(hwnd, (rect[0], rect[1]))

                        # get the width and height of the client area
                        width = rect[2] - rect[0]
                        height = rect[3] - rect[1]

                        # create a region object
                        region = (x, y, x + width, y + height)
                        print(region)
                        time.sleep(0.5)
                        signin_button_location = pyautogui.locateOnScreen(root.login_place, region=region, confidence=0.8)
                        if signin_button_location:
                            x, y = pyautogui.center(signin_button_location)
                            pyautogui.click(x, y)
                            time.sleep(0.5)
                            pyautogui.write(code)
                            time.sleep(20)
                            
                            timeout = 5
                            while win32gui.IsWindow(hwnd):
                                time.sleep(5)
                                timeout=-1
                                if timeout <=0:
                                    break
                            else:
                                print("retry IsWindow")
                                conn.sendall("popen".encode())
                                
                                    
                                
                            
                            
                        else:
                            time.sleep(5)
                            print("cant find image retry")
                            conn.sendall("popen".encode())
                else:
                    print("retry")
                    time.sleep(3)
                    conn.sendall("popen".encode())
            
            print(f'Received from {addr}: {data.decode()}')
        print(f'Disconnected from {addr}')
        del clients[steamid]
        
# Start the server in a separate thread




userid = None
PATH = os.path.dirname(os.path.realpath(__file__))
IMG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),"images")


if getattr(sys, 'frozen', False):
    # we are running in a bundle
    script_dir = os.path.dirname(sys.executable)
else:
    # we are running in a normal Python environment
    script_dir = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(script_dir,"lib")






cluster = None 

def connect():
    global cluster,db
    try:
        if cluster is None:
            try:
                
                cluster = MongoClient("mongodb+srv://panel:LetTLam4mHEeusSp@cluster0.homz8.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",connectTimeoutMS=3000,)
                
            except:
                error_label.configure(text="unable to connect to server",text_color="red")  
            else:
                
                class db():
            
                    servers = cluster["servers"]
                    users_database = cluster["usersdb"]
                    guildsetting = servers["guildsetting"]
                    ticketsdb = servers["privatechannels"]
                    balancesdb = users_database["balancesdb"]
                    usersdb = users_database["usersdb"]
                    serverusers = servers["serverusers"]
                    slotsdb = servers["commendbotstatus"]
                    subdb = servers["sub"]
                    truserdb = servers["translateuserdb"]
                    timedb = servers["timer"]
                    statsdb = servers["stats"]
                    blacklistdb = servers["blacklistdb"]
                    userssubscriptions = servers["userssubscriptions"]
                    sellsds = servers["sellsdb"]
                    refresh = servers["refresh"]
                    waitinglist = servers["waitinglist"]
                    keysdb = servers["keysdb"]
                    learn = servers["slots_ai"]
                    errorlog = servers["errors"]
                    localdb = cluster["local"]
                    
                    oplogs = localdb["oplog.rs"]
    except Exception as e:
        print(e)


def get_id() -> str:
    cmd = 'wmic csproduct get uuid'
    uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n")+2
    uuid = uuid[pos1:-15]
    return uuid
allserverscs = {1:{"ip":"server.example.com","port":27642,"password":"CHANGEME"},2:{"ip":"server.example.com","port":28468,"password":"CHANGEME"},3:{"ip":"server.example.com","port":28234,"password":"CHANGEME"},}

def callback(id:int):
    server  = allserverscs[id]
    webbrowser.open_new(f"steam://connect/{server['ip']}:{server['port']}/{server['password']}")
    
    
    
    
def callback_link(id:int):
    server  = allserverscs[id]
    pyperclip.copy(f"connect {server['ip']}:{server['port']}; password {server['password']}")
    






   
        
                    
                
                
                
            
            
    
    
            
            
            
    

hwid = get_id()

class Login_Window(CTkToplevel):
    def __init__(self,master, *args, **kwargs):
        super().__init__(master,*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)
     
       
        
        self.resizable(width=False, height=False)
        window_width = 320
        window_height = 350
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        

        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)

        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

        self.title("CB Panel")
        self.iconbitmap(IMG_PATH + "/test.ico")
        
        frame = CTkFrame(master=self)
        frame.pack(fill="both",expand=True)
        
        
            
            
        label= CTkLabel(master=frame,text="CommendBot",font=("Roboto",20,"bold"),).pack(pady=10 ,padx=12)


        global login_entry ,password_entry,error_label
        
        
        login_entry = CTkEntry(master=frame,placeholder_text="Login" )
        password_entry = CTkEntry(master=frame,placeholder_text="Password",show="*")
        if  "CommendBotPR" in regobj.HKEY_CURRENT_USER.Software and "login" in regobj.HKEY_CURRENT_USER.Software.CommendBotPR.values():
            dir =regobj.HKEY_CURRENT_USER.Software.CommendBotPR
            login_entry.insert(END,str(dir["login"].data))
            password_entry.insert(END,str(dir["password"].data))
        login_entry.pack(pady=10 ,padx=12)
        

        
        password_entry.pack(pady=5 ,padx=6)
        error_label = CTkLabel(frame,text="")
        error_label.pack()
        button = CTkButton(master=frame,text="Login",command=login).pack()
        server_thread = Thread(target=start_server, daemon=True, name='server')
        server_thread.start()
        
        
       
        
    def on_window_close(self):
        global stop_server
        stop_server = True
        print("bye")
        

            
        
        sys.exit()
        


class Thread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
    def run(self):
        try:
            super().run()
        except Exception:
            exc_info = sys.exc_info()
            message = ''.join(traceback.format_exception(*exc_info))
            messagebox.showerror('Thread-Error', message)
            try:
                db.errorlog.insert_one({"hwid":hwid,"msg":message,"datetime":datetime_utc,"version":version})
            except Exception as ex :
                print(ex)
    
        

                

            

   
        
class App(CTk):

    

    def __init__(self):
        super().__init__()
        self.withdraw()
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")
        
        self.resizable(width=False, height=False)
        
        
        window_width = 750
        window_height = 450
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        

        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)

        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
        self.font = CTkFont(family="<Roboto>")
        
        
        self.home_ico_black = load_image("/home-gray.png",20)
        self.home_ico_white = load_image("/home-white.png",20)
        self.money_bag_black = load_image("/money_bag-gray.png",20)
        self.money_bag_white = load_image("/money_bag-white.png",20)
        self.settings_ico_black = load_image("/settings-gray.png",20)
        self.settings_ico_white = load_image("/settings-white.png",20)
        self.commend_ico_black = load_image("/smile-gray.png",20)
        self.commend_ico_white = load_image("/smile-white.png",20)
        self.login_place = Image.open(IMG_PATH + "/login_selector.png")
        self.iconphoto = load_image("/logo.ico",100)
        self.importico = CTkImage(Image.open(IMG_PATH + "/import.png"),size=(15,15))
        self.green = CTkImage(Image.open(IMG_PATH + "/green.png"),size=(8,8))
        self.red = CTkImage(Image.open(IMG_PATH + "/red.png"),size=(8,8))
        self.iconbitmap(IMG_PATH + "/test.ico")
        self.title("CB Panel")
        self.login_window = Login_Window(self)
        
        connect()
        
        
    def report_callback_exception(self, exc_type, exc_value, exc_traceback):
        message = ''.join(traceback.format_exception(exc_type,
                                                     exc_value,
                                                     exc_traceback))
        messagebox.showerror('Error', message)
        try:
            db.errorlog.insert_one({"hwid":hwid,"msg":message,"datetime":datetime_utc,"version":version})
        except Exception as ex :
            print(ex)
    
    
     
        

def load_image(path, image_size):
        """ load rectangular image with path relative to PATH """
        
        return CTkImage(Image.open(IMG_PATH + path).resize((image_size, image_size)))
    



def login():
    
    connect()
    
    
    login_info = login_entry.get()
    password_info = password_entry.get()
    
    if (login_info == "" or password_info == ""):
        error_label.configure(text="Incorrect username or password.",text_color="red")
    else:
        global userdb
        try:
 
            userdb = db.usersdb.find_one({"login":login_info.strip(),"password":password_info.strip()})
        except:
            error_label.configure(text="unable to connect to server",text_color="red")  
            
        
        else:
            
            
            if userdb :
                    if "expired" in userdb:
                        global premium
                        premium = not userdb["expired"]
                
                    if  "CommendBotPR" in regobj.HKEY_CURRENT_USER.Software:
                        dir =regobj.HKEY_CURRENT_USER.Software.CommendBotPR
                        if str(dir["login"].data) != login_info or str(dir["password"].data) != password_info:
                            regobj.HKEY_CURRENT_USER.Software.set_subkey("CommendBotPR",{"login":login_info,"password":password_info})
                    else:
                        regobj.HKEY_CURRENT_USER.Software.set_subkey("CommendBotPR",{"login":login_info,"password":password_info})
                    regobj.HKEY_CURRENT_USER.Software.set_subkey("CommendBotPR",{"login":login_info,"password":password_info})
                    
                    global userid
                    userid  = int(userdb["userid"])
                    blackilist = db.blacklistdb.find_one({"userid":userid})
                    
                    if not blackilist:
                        if not "hwid" in userdb:
                            db.usersdb.update_one({"_id":userdb["_id"]},{"$set":{"hwid":hwid}})
                            root.winfo_children()[0].destroy()
                            panel_screen()
                        elif userdb["hwid"] == hwid:
                            root.winfo_children()[0].destroy()
                            panel_screen()
                            
                            
                        else:
                            error_label.configure(text="Panel is linked!",text_color="red") 
                            
                    else:
                        error_label.configure(text="You are blacklisted!",text_color="red")
                
            else:
                error_label.configure(text="Wrong username or password.",text_color="red")
            
            
    
def init_all():
    
    home_screen.init()

    commend_screen.init()

    balance_screen.init()

    settings_screen.init()

    
    

def get_steamID64(steamlink:str) -> int:
    if len(str(steamlink.strip())) == 17:
        try:
            steamID64 = int(steamlink)
        except:
            return None
        else:
            return steamID64

    elif "/id/" in steamlink or "/profiles/"  in steamlink:
                                                
        try:    
            urls = steamid.steam64_from_url(steamlink, http_timeout=80)
        except:
            return None
        else:
            return urls
    else:
        return None   



    

    
def panel_screen():
    
    
    frame = CTkFrame(master=root,width=50,height=50)
    frame.pack(fill="y",side=LEFT)
    Frame(master=root,width=2,height=40,bg="gray").pack(fill="y",side=LEFT)

    
    logo_button = CTkButton(master=frame,text="",image=root.iconphoto,fg_color="transparent",hover=False,height=40,width=40)
    
    logo_button.pack()
    init_all()
    database_thread = Thread(target=watch_mongodb, daemon=True, name='database')
    database_thread.start()
    daemon = Thread(target=do_stuff, daemon=True, name='bg_tasks',args=[0])
    daemon.start()
    
    
    
    
    
    global home_page,balance_page,settings_page,commend_page
    home_page = CTkButton(master=frame, image=root.home_ico_black, text="", width=25, height=25,command=home_screen.pop_up,hover_color="#add8e6",fg_color="transparent")
    
   
    home_page.pack(pady=10,padx=12)
    
    commend_page = CTkButton(master=frame, image=root.commend_ico_black, text="", width=25, height=25,command=commend_screen.pop_up,hover_color="#add8e6",fg_color="transparent")
    commend_page.pack(pady=10,padx=12)
    
    balance_page = CTkButton(master=frame, image=root.money_bag_black, text="", width=25, height=25,command=balance_screen.pop_up,hover_color="#add8e6",fg_color="transparent")
    balance_page.pack(pady=10,padx=12)
    settings_page = CTkButton(master=frame, image=root.settings_ico_black, text="", width=25, height=25,command=settings_screen.pop_up,hover_color="#add8e6",fg_color="transparent")
    settings_page.pack(pady=10,padx=12)
    home_screen.pop_up()
    root.deiconify()
    CTkLabel(frame,text=f"V{version}",font=("Roboto",8)).pack(side=BOTTOM)
    
    
    

    
    


def clear_all(stay:CTkButton,frames:list[CTkFrame]):
    for child in root.winfo_children()[2:]:
        if not child in frames:
            if type(child) != CTkToplevel:
            
                child.pack_forget()
            
        
    
    
    if not home_page == stay:
        
        if home_page._image != root.home_ico_black:
            
            home_page.configure(image=root.home_ico_black,hover=True)
            home_page._update_image()
        
            
    else:
        img = root.home_ico_white
    
    if not commend_page == stay:
        if commend_page._image != root.commend_ico_black:
            
            commend_page.configure(image=root.commend_ico_black,hover=True)
            commend_page._update_image()
        
            
    else:
        img = root.commend_ico_white
        
    
    if not balance_page == stay:
        if balance_page._image != root.money_bag_black:
            balance_page.configure(image=root.money_bag_black,hover=True)
            balance_page._update_image()
         
        
    else:
        img = root.money_bag_white
    if not settings_page == stay:
        if settings_page._image != root.settings_ico_black:
            settings_page.configure(image=root.settings_ico_black,hover=True)
            settings_page._update_image()
    else:
        img = root.settings_ico_white
    
       
    stay.configure(image=img,hover=False)
    stay._update_image()
    #stay.configure(state=DISABLED)
    
class home_screen():
    
    def init():
        global home_frame
        home_frame = CTkFrame(master=root,width=150,height=100)  
        home_frame.pack_forget()
        
    def pop_up():
        home_frame.pack(fill=Y,expand=False,side=TOP,anchor=NW,padx=25,pady=20)
        
        clear_all(home_page,[home_frame])
        
        

current_account = None        


def pause_cancel_func():
    
    if pause_cancel._text == "Pause":
        pass
        
    else:
        """ if current_account in check_verify:
            del check_verify[current_account]"""
        servercheck = db.serverusers.find_one_and_delete({"steamID64":current_account})
        
        slotdb =db.slotsdb.find_one_and_update({"_id":servercheck["slot_id"]}, {"$inc": {"currency":+servercheck["amount"]}},return_document = ReturnDocument.AFTER)
        

def stop_confirm_func():
    servercheck = db.serverusers.find_one({"steamID64":current_account})
    if stop_confirm._text == "Confirm":
        
        start_waiting(servercheck)
        
        
    else:
        
        
        
        dictlist ={"slot_id":servercheck["slot_id"], "steamID64":current_account,"amount":servercheck["amount"],"status":"wait","waitchannelid":servercheck["commend_channelid"], "hwid":hwid,"datetime":datetime_utc,"type":"stop"}
        db.waitinglist.insert_one(dictlist)
        print("stopfnc")
        stop_confirm.configure(text="Stop",state=DISABLED)
        pause_cancel.configure(text="Pause",state=DISABLED) 
        
def start_waiting(servercheck:dict):
    
    dictlist ={"slot_id":servercheck["slot_id"], "steamID64":servercheck["steamID64"],"amount":servercheck["amount"],"status":"wait","waitchannelid":servercheck["commend_channelid"], "hwid":hwid,"datetime":datetime_utc,"type":"start"}
    db.waitinglist.insert_one(dictlist)
    print("startw8")
    global current_account 
    if int(current_account) == servercheck["steamID64"]:
        stop_confirm.configure(text="Stop",state=DISABLED)
        pause_cancel.configure(text="Pause",state=DISABLED) 
    



class VerticalScrolledFrame:
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    :width:, :height:, :bg: are passed to the underlying Canvas
    :bg: and all other keyword arguments are passed to the interior Frame
    note that a widget layed out in this frame will have a self.master 3 layers deep,
    (outer Frame, Canvas, interior Frame) so 
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """
    def __init__(self, master, **kwargs):
        
        width = kwargs.pop('width',420 )
        height = kwargs.pop('height', 150)

        
        
        
        
        self.outer = CTkFrame(master, fg_color="transparent",width=420,height=150 )

        self.vsb = CTkScrollbar(self.outer,height =150,)
        self.vsb.pack(fill=Y, side=RIGHT)
        self.canvas = CTkCanvas(self.outer, highlightthickness=0, width=width, height=height,bg="#202120")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb.configure(command=self.canvas.yview) 

        self.interior = CTkFrame(self.canvas, fg_color="transparent")
        # pack the interior Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.interior, anchor='nw')
        self.interior.bind("<Configure>", self._on_frame_configure)
        
        self.outer_attr = set(dir(Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.interior
            return getattr(self.interior, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units" )

    def __str__(self):
        return str(self.outer)


def start_mass_commend():
    if CSGOPath:
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a file", filetypes=[("Text file", "*.txt")])
        if file_path:
            with open(file_path,"r") as f :
                lines = f.readlines()
            dlist = []
            for id,line in enumerate(lines,start=1):
                param = line.strip().split(":")
                if len(param) == 3 and is_number(param[2]) or len(param) == 4 and is_number(param[2]):
                    dlist.append({"login":param[0],"pwd":param[1],"amount":param[2],"shared_secret":(param[3]if len(param) == 4 else None)})
                else:
                    messagebox.showerror("Syntax error",f"The line {id} have incorrect syntax\nMake sure its:\nlogin:password:amount_of_commends(number):shared_secret(optional)")
                    return
            bot_thread = Thread(target=process_mass_commend, args=[dlist])
            bot_thread.start()
    else:
        messagebox.showerror("Setup Error","Please first setup correct path/s for csgo and steam in settings")        
            
                
        
def process_mass_commend(dlist):  
    slot = commend_frame.slots_menu2.get()
    slot_id = int(slot.split(".")[0])
    ruserdata = os.path.join(SteamPath,"config","loginusers.vdf")
    steamID64 = None
    with open(ruserdata, 'r',encoding='utf-8') as f:
        vdf_dict = vdf.load(f)
        
        
        
        
    for account in dlist:
        login = account["login"]
        password = account["pwd"]
        amount = account["amount"]
        if "shared_secret" in account:
            shared_secret = account["shared_secret"]
        else:
            shared_secret = None
        
        for user_id, user_dict in vdf_dict['users'].items():
            if 'AccountName' in user_dict and user_dict['AccountName'] == login:
                steamID64 = int(user_id)
                break
        if steamID64 is None:
            app_path = os.path.join(SteamPath, f"steam.exe")
            subprocess.Popen([ app_path, "-login",login,password] )
            if len(check_verify) == 0:
                
                check_verify[random.randint(0,100)] = {"login":login,"password":password,"amount":amount,"slot_id":slot_id,"shared_secret":shared_secret}
                
                
            else:
                while len(check_verify) != 0:
                    print("checking for free")
                    time.sleep(5)
                check_verify[random.randint(0,100)] = {"login":login,"password":password,"amount":amount,"slot_id":slot_id,"shared_secret":shared_secret}
                
        else:
            print(f"starting {steamID64}")
            error = local_commend(steamID64,slot_id,int(amount),login,password,shared_secret)
            if  error :
                print("error raised stopped masscommend")
                break
               
            print("waiting")
            time.sleep(20)
        
        
    
    
    

class CommendView(CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        linkpage = self.add("Link")
        loginpage = self.add("Login")
        self.steam_link_entry = CTkEntry(master=linkpage,placeholder_text="Profile link",width=200,justify=CENTER)
        self.steam_link_entry.pack(padx=5,pady=5)
        self.amount_entry = CTkEntry(master=linkpage,placeholder_text="amount of commends",justify=CENTER,width=160)
        self.amount_entry.pack(padx=5,pady=5)
        
        self.importbtn = CTkButton(master=loginpage,image=root.importico,text="", width=10, height=10,fg_color="transparent",hover=False,command=start_mass_commend)
        self.importbtn.place(x=-2,y=155 ,)
        
        self.steam_login_entry = CTkEntry(master=loginpage,placeholder_text="Login",width=200,justify=CENTER)
        self.steam_login_entry.pack(padx=5,pady=(0,5))
        self.steam_password_entry = CTkEntry(master=loginpage,placeholder_text="Password",width=200,justify=CENTER,show="*")
        self.steam_password_entry.pack(padx=5,pady=0)
        self.steam_amount_entry = CTkEntry(master=loginpage,placeholder_text="amount of commends",justify=CENTER,width=160)
        self.steam_amount_entry.pack(padx=5,pady=5)
        slots = list(db.slotsdb.find({}))
        
        slots_name = []
    
        for slot in slots:
            slots_name.append(f"{slot['_id']}.{slot['name']}")
        
        self.slots_menu = CTkOptionMenu(master=linkpage,values=slots_name)
        
        self.slots_menu.pack(padx=5,pady=5)
        self.slots_menu2 = CTkOptionMenu(master=loginpage,values=slots_name)
        self.slots_menu2.pack(padx=5,pady=0)
        
        
        self.error_show = CTkLabel(master=linkpage,text="",text_color="red",font=("Roboto",11),height=5)
        self.error_show.pack(padx=5,pady=0)
        
        CTkButton(master=linkpage,text="Start",command=link_commend).pack(padx=10,pady=(12,5))
        CTkButton(master=loginpage,text="Start",command=start_local_commend).pack(padx=10,pady=(5,5))
        


class commend_screen:  
    
        
    def init():
        
        global commend_head_frame, commend_stats,userlist,commend_stats_buttons,stop_confirm,crlframe,commend_frame
        commend_head_frame = CTkFrame(master=root,fg_color="transparent")
        
        commend_top_frame = CTkFrame(master=commend_head_frame,width=740,height=300,fg_color="transparent")
        commend_frame = CommendView(commend_top_frame, width=210,height=220,)
        
        
        
        
        
        
        commend_frame_logs = CTkFrame(master=commend_top_frame,width=400,height=135)
        
        
        
        commend_frame_logs.pack(side=RIGHT,padx=(0,20),pady=(20,0),expand=TRUE,fill=BOTH)
        CTkLabel(master=commend_frame_logs,text="Logs",font=("Roboto",15,"bold")).pack(pady=(5,0),padx=20,anchor=NW)
        crlframe = VerticalScrolledFrame(commend_frame_logs,)
        
        crlframe.pack()
        
        #conectnow_pop_up()
        
        
        
        
        
        
        accs = list(db.serverusers.find({"hwid":hwid}).sort("_id", ASCENDING))
        
        
        for id,commend in enumerate(accs):
            if commend["steamID64"] in accounts:
                pass
            else:
                accounts[commend["steamID64"]] = {"started":False} 
            
        
        
        commend_stats = CTkFrame(master=commend_head_frame,width=700,height=200)
        commend_stats.pack_propagate(False)
        commend_stats_buttons = CTkFrame(master=commend_stats,width=200,height=220)
        commend_stats_buttons.pack_propagate(False)
        userlist = CTkOptionMenu(master=commend_stats_buttons,command=select_profile,values=[str(k) for k in accounts.keys()])
        userlist.set(str(list(accounts.keys())[0]) if len(accounts)!= 0 else " ")
        
        userlist.pack(padx=10,pady=12)
          
        stop_confirm = CTkButton(master=commend_stats_buttons,text="Stop",state=DISABLED,command=stop_confirm_func)
        stop_confirm.pack(pady=10,padx=5)
        global pause_cancel
        pause_cancel= CTkButton(master=commend_stats_buttons,text="Pause",state=DISABLED,command=pause_cancel_func)
        pause_cancel.pack(pady=10,padx=5)
        
        stats_only = CTkFrame(master=commend_stats,width=450,height=200)
        stats_only.pack_propagate(False)  
        stats_only.pack(side=RIGHT,pady=15,padx=15) 
        stats_top = CTkFrame(master=stats_only,width=450,height=200,fg_color="transparent")
        stats_top.pack(side=TOP)
        stats_bottom = CTkFrame(master=stats_only,width=450,height=200,fg_color="transparent")
        stats_bottom.pack(side=BOTTOM)
        global recieved_num,pending_num,end_time_num,status_num,chunk_num,total_num
        recieved_frame = CTkFrame(master=stats_top,width=75,height=55,border_width=2,)
        recieved_frame.pack_propagate(False)  
        recieved_frame.pack(pady=(20,10),padx=37.5,side=LEFT,anchor=NW)    
        CTkLabel(master=recieved_frame,text="Received",font=("Roboto",15,"bold")).pack(pady=(3,0))
        recieved_num = CTkLabel(master=recieved_frame,text="0",font=("Roboto",14,"bold"))
        recieved_num.pack(pady=(0,3),anchor=CENTER)
        
        pending_frame = CTkFrame(master=stats_top,width=75,height=55,border_width=2,)
        pending_frame.pack_propagate(False)  
        pending_frame.pack(pady=(20,10),padx=37.5,side=LEFT,anchor=NW)    
        CTkLabel(master=pending_frame,text="Pending",font=("Roboto",15,"bold")).pack(pady=(3,0))
        pending_num =CTkLabel(master=pending_frame,text="0",font=("Roboto",14,"bold"))
        pending_num.pack(pady=(0,3),anchor=CENTER)
        
        total_frame = CTkFrame(master=stats_top,width=75,height=55,border_width=2,)
        total_frame.pack_propagate(False)  
        total_frame.pack(pady=(20,10),padx=37.5,side=LEFT,anchor=NW)    
        CTkLabel(master=total_frame,text="Total",font=("Roboto",15,"bold")).pack(pady=(3,0))
        total_num = CTkLabel(master=total_frame,text="0",font=("Roboto",14,"bold"))
        total_num.pack(pady=(0,3),anchor=CENTER)
        
        
        
        
        status_frame = CTkFrame(master=stats_bottom,width=75,height=55,border_width=2,)
        status_frame.pack_propagate(False)  
        status_frame.pack(pady=(10,20),padx=37.5,side=LEFT,anchor=SW)    
        CTkLabel(master=status_frame,text="Status",font=("Roboto",15,"bold")).pack(pady=(3,0))
        status_num = CTkLabel(master=status_frame,text="free",font=("Roboto",12,"bold"))
        status_num.pack(pady=(0,3),anchor=CENTER)
        
        chunk_frame = CTkFrame(master=stats_bottom,width=75,height=55,border_width=2,)
        chunk_frame.pack_propagate(False)  
        chunk_frame.pack(pady=(10,20),padx=37.5,side=LEFT,anchor=SW)    
        CTkLabel(master=chunk_frame,text="Chunk",font=("Roboto",15,"bold")).pack(pady=(3,0))
        chunk_num = CTkLabel(master=chunk_frame,text="#0・[0/0]",font=("Roboto",12,"bold"))
        chunk_num.pack(pady=(0,3),anchor=CENTER)
        
        end_time_frame = CTkFrame(master=stats_bottom,width=75,height=55,border_width=2,)
        end_time_frame.pack_propagate(False)  
        end_time_frame.pack(pady=(10,20),padx=37.5,side=LEFT,anchor=SW)    
        CTkLabel(master=end_time_frame,text="End time",font=("Roboto",15,"bold")).pack(pady=(3,0))
        end_time_num = CTkLabel(master=end_time_frame,text="0",font=("Roboto",12,"bold"))
        end_time_num.pack(pady=(0,3),anchor=CENTER)
        
        
       
        
        
        
        
        select_profile(current_account)
        global cb_logs
        cb_logs =commend_logs()
            
        
        
        
        
        
        
        
        commend_top_frame.pack(expand=False,fill=X,side=TOP,pady=0)
        
        commend_frame.pack(fill=None,expand=False,padx=20,pady=(10,0),side=LEFT)
        
        
        commend_stats.pack(side=RIGHT,padx=20,pady=(10,10))
        commend_stats_buttons.pack(pady=15,padx=(15,0),side=LEFT)
        
        
        
        
        
    
        
    def pop_up():
        
        clear_all(commend_page,[commend_head_frame])
        commend_head_frame.pack(fill=BOTH,expand=YES)
        
    def update():
        
        
        
        try:
            slots = list(db.slotsdb.find({}))
        except:
            pass
        else:
            
        
            slots_name = []
        
            for slot in slots:
                slots_name.append(f"{slot['_id']}.{slot['name']}")
            commend_frame.slots_menu.configure(values=slots_name)
            commend_frame.slots_menu.set(slots_name[0])
            
        try:
            
            database = list(db.serverusers.find({"hwid":hwid}).sort("_id", ASCENDING))
        except:
            accdb = list()
        else:
            
            
            
            global current_account,accounts
            


 
def watch_mongodb():
    
    global current_account,accounts,userlist
    changes = db.servers.watch()
    for change in changes:
        
        
        db_name = change["ns"]["coll"]
        if change["operationType"] == "insert":
            idb = change["fullDocument"]
        elif change["operationType"] == "delete" :
            if isinstance(change["documentKey"]["_id"],int):
                if int(change["documentKey"]["_id"]) in accounts.keys():
                    
                    del accounts[int(change["documentKey"]["_id"])]
                    userlist.configure(values=[str(k) for k in accounts.keys()])
                    if len(accounts) == 0:
                        current_account = None
                        userlist.set(" ")
                        change_stats(None)
                    else:
                        if not current_account in accounts.keys():
                            current_account = int(list(accounts.keys())[0])
                            userlist.set(str(current_account))
                            edb = db.serverusers.find_one({"steamID64":current_account})
                            change_stats(edb)
            continue
                
        else:
            idb = db.servers[db_name].find_one({"_id":change["documentKey"]["_id"]})
            
        
        if  db_name == "waitinglist":
            pass
        elif db_name == "serverusers":
            
            if idb and "hwid" in idb and idb["hwid"] == hwid:
                
                if change["operationType"] == "insert":
                    if not idb["steamID64"] in accounts:
                        accounts[idb["steamID64"]] = {"started":False} 
                        userlist.configure(values=[str(k) for k in accounts.keys()])
                        
                        current_account = idb["steamID64"]
                        userlist.set(str(idb["steamID64"]))
                        
                        
                        
                elif change["operationType"] == "update":    
                    if not "done" == idb["status"] and not "error" == idb["status"]:
                        if idb["status"] == "confirmed":
                            if not f"confirmed-{idb['_id']}" in logcheck:
                                logs.append(f"Start Commending for\n{idb['steamID64']}")
                                logcheck.append(f"confirmed-{idb['_id']}")
                            
                            
                            
                            if current_account == idb["steamID64"]:
                                
                                select_profile(current_account,idb)
                    else:
                        db.serverusers.delete_one({"_id":idb["_id"]})
                        if idb["steamID64"] in accounts:
                            del accounts[idb["steamID64"]]
                            userlist.configure(values=[str(k) for k in accounts.keys()])
                        if len(accounts) == 0:
                            select_profile()
                            current_account = None
                            userlist.set(" ")
                            change_stats(None)
                        else:
                            if not current_account in accounts.keys():
                                current_account = int(list(accounts.keys())[0])
                                userlist.set(str(current_account))
                                edb = db.serverusers.find_one({"steamID64":current_account})
                                change_stats(edb)
                                
                                
                        
                        if "error" == idb["status"]:
                            
                            logs.append(f"End Commending for\n{idb['steamID64']}")
                            
                            messagebox.showerror(f"Start Error",f"We cant start commending for \naccount: {idb['steamID64']} \nReason: {idb['reason']}")
                            
                        else:
                            print("done commending")
                            
                        
                            print(idb["steamID64"])
                            
                            state = end_task.get()
                            if "Turn off PC" == state :
                                print("pc off")
                                os.system("shutdown /s /t 1")
                                
                            elif "Close Panel&CS:GO" == state :
                                print("close cs@p")
                                if idb["steamID64"] in clients:
                                    s = clients[idb["steamID64"]]
                                    s.sendall(f"close".encode())
                                print(accounts)
                                if len(accounts) == 0 :
                                    os._exit(1)    
                                    
                                    
                                    
                                
                            elif "Close CS:GO" == state :
                                print("close cs")
                                if idb["steamID64"] in clients:
                                    s = clients[idb["steamID64"]]
                                    s.sendall(f"close".encode())
                                
                                
                                    
                                    
                                    
                            if not f"done-{idb['_id']}" in logcheck:
                                logs.append(f"End Commending for\n{idb['steamID64']}\n{idb['actualamount']}/{idb['amount']}")
                                logcheck.append(f"done-{idb['_id']}")
                            
                            
                       
                    
                    commend_logs.update(cb_logs) 
                    print(logs)
    print("session crashedmongodb")
    time.sleep(2)
    watch_mongodb()
   
def conectnow_pop_up():
    beststerver = (1,1)
    for gid,server in allserverscs.items():
        try:
            info: a2s.SourceInfo = a2s.info((server["ip"],server["port"]))
        except:
            pass
                
                    
        else:
            avg =  info.player_count / info.max_players 
            if avg < beststerver[1]:
                beststerver = (gid,avg)
    conectnow_window = CTkToplevel(root)
    conectnow_window.geometry("400x200")
    commend_frame_connect = CTkFrame(master=conectnow_window,width=400,height=50)
    commend_frame_connect.pack(padx=20,side=TOP,pady=12)
    CTkLabel(master=commend_frame_connect,text="Connect to:",font=("Roboto",15,"bold")).pack(side=TOP)
    
          
    
    

    connect_now = CTkButton(master=commend_frame_connect,text=f"#{beststerver[0]} Connect Now",command=lambda:callback(beststerver[0]),border_color=None,hover=False,fg_color="transparent")
    connect_now.pack(side=LEFT)
    copy_now = CTkButton(master=conectnow_window,text=f"Copy",command=lambda:callback_link(beststerver[0]),hover_color=None,border_color=None,fg_color="transparent",hover=False)
    copy_now.pack(side=RIGHT)  
            
def tempfr() -> CTkFrame:
     
    tempframe =CTkFrame(master=crlframe.interior,width=390,height=60,fg_color="transparent")
    tempframe.pack_propagate(False)  
    tempframe.pack(padx=0)
    return tempframe

class commend_logs():
    def __init__(self) -> None:
        self.counter = 1     
        self.sitecounter = 1
        self.tempframe = tempfr()
        self.siteframe = CTkFrame(master=self.tempframe,height=60,fg_color="transparent")
        self.siteframe.pack(side=LEFT,pady=(0,10))
        
        
    def update(self):
    
        
    
    
    
        
        
        for log in logs:
            
            
            tfold = CTkFrame(master=self.siteframe,width=120,height=60,border_width=1,fg_color="transparent")
            tfold.pack_propagate(False)  
            
            if self.sitecounter == 1:
                tfold.pack(side=LEFT,padx=5) 
            elif self.sitecounter == 2:
                tfold.pack(side=RIGHT,padx=5) 
            
            CTkLabel(master=tfold,text=log,font=("Roboto",11,"bold")).pack(pady=(2,0),side =TOP)
            dt = datetime.datetime.now(tz=local)
            if 9>dt.minute:
                min = ("0"+str(dt.minute))
            else:
                min = dt.minute
            CTkLabel(master=tfold,text=f"{dt.hour}:{min}",font=("Roboto",10)).pack(pady=(0,2,),side=BOTTOM,anchor=SE,padx=(0,1))
            if self.counter == 3:
                self.counter = 1
                self.tempframe = tempfr()
                self.siteframe = CTkFrame(master=self.tempframe,height=60,fg_color="transparent")
                self.siteframe.pack(side=LEFT,padx=0,pady=(0,10))
                print("-",self.sitecounter)
            else:
                self.counter +=1
            
                if self.sitecounter == 2:
                    self.sitecounter = 1
                    self.siteframe = CTkFrame(master=self.tempframe,height=60,fg_color="transparent")
                    print(self.counter)
                    if self.counter == 2:
                            
                        self.siteframe.pack(side=LEFT,padx=0,pady=(0,10))
                    else:
                        self.siteframe.pack(side=RIGHT,padx=0,pady=(0,10))
                else:

                    self.sitecounter+=1
            logs.remove(log)
            
        
logcheck = []    
        
    
    
def change_stats(serverdb:dict):
    if serverdb:
        if recieved_num._text != str(serverdb["actualamount"]):
            recieved_num.configure(text=str(serverdb["actualamount"]))
                
        if pending_num._text != str(serverdb["lastpending"]):
            pending_num.configure(text=str(serverdb["lastpending"]))
        
        if total_num._text != str(serverdb["amount"]):
            total_num.configure(text=str(serverdb["amount"]))
        
        status = serverdb["status"]
        decrypt = {"w8connect":"Connecting","confirmed":"Commending","stoped":"Paused","done":"Finished","error":"Error"}
        if status_num._text !=decrypt[status]:
            status_num.configure(text=decrypt[status])
            
        
            
        if serverdb["status"] == "stoped":
            """if not f"stoped-{serverdb['_id']}" in logcheck:
                logs.append(f"Pause Commending for\n{serverdb['steamID64']}")
                logcheck.append(f"stoped-{serverdb['_id']}")"""
        
            
                
            
        if  chunk_num._text != f"{serverdb['chunk']}・{serverdb['chunk-info']}":
            chunk_num.configure(text=f"{serverdb['chunk']}・{serverdb['chunk-info']}")
        
        if "endeta" in serverdb:
            dt_obj = (datetime.datetime.fromtimestamp(serverdb["endeta"],tz=local))
            
            minutes = ((( dt_obj - datetime.datetime.now(tz=local)).total_seconds()) / 60)
            if minutes > 60:
                txt = f"{(round(minutes/60,2))} hr"
            else:
                txt = f"{(int(minutes))} min"
            
            if  txt != end_time_num._text:
                end_time_num.configure(text=txt)
        else:
            end_time_num.configure(text="0 min")  
    else:
        
        recieved_num.configure(text="0")     
        pending_num.configure(text="0")      
        total_num.configure(text="0")   
        status_num.configure(text="Free")  
        chunk_num.configure(text=f"#0・[0/0]")   
        end_time_num.configure(text="0 min")  
                
                
def select_profile(select=None,serverdb=None):
    
    
    if select:
        global current_account
        steamid = int(select)
        current_account = steamid
        if  serverdb is None:
            
            serverdb = db.serverusers.find_one({"steamID64":current_account})
        waitlist = db.waitinglist.find_one({"steamID64":current_account})
        if waitlist:
            if waitlist["status"] == "start":
                print("starting for it")
                stop_confirm.configure(text="Stop",state=DISABLED)
                pause_cancel.configure(text="Pause",state=DISABLED) 
            else:
                stop_confirm.configure(text="Stop",state=DISABLED)
                pause_cancel.configure(text="Pause",state=DISABLED)
                
        else:
            
            
            
            
            if serverdb["status"] == "w8connect":
                stop_confirm.configure(text="Confirm",state=NORMAL)
                pause_cancel.configure(text="Cancel",state=NORMAL)
            elif serverdb["status"] == "confirmed":
                stop_confirm.configure(text="Stop",state=NORMAL)
                pause_cancel.configure(text="Pause",state=NORMAL)
            elif serverdb["status"] == "stopped":
                stop_confirm.configure(text="Confirm",state=NORMAL)
                pause_cancel.configure(text="Cancel",state=NORMAL)
        
            
            
            
    else:
        
        stop_confirm.configure(text="Stop",state=DISABLED)
        pause_cancel.configure(text="Pause",state=DISABLED) 
        
    change_stats(serverdb)
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        
        return False        
        
def start_local_commend():
    if CSGOPath:
        login = commend_frame.steam_login_entry.get()
        password = commend_frame.steam_password_entry.get()
        amount = commend_frame.steam_amount_entry.get()
        commend_frame.steam_login_entry.delete(0, END)
        commend_frame.steam_password_entry.delete(0, END)
        commend_frame.steam_amount_entry.delete(0, END)
        slot = commend_frame.slots_menu2.get()
        if (login == "" or password == "" or amount == ""):
            messagebox.showerror("Please set steam login,password and amount.","Please set steam login,password and amount.")

        else:
            slot_id = int(slot.split(".")[0])
            if not is_number(amount):
                messagebox.showerror("The amount is not a number!","The amount is not a number.")
                return 
            amount = int(amount)
            
            ruserdata = os.path.join(SteamPath,"config","loginusers.vdf")
            steamID64 = None
            with open(ruserdata, 'r',encoding='utf-8') as f:
                vdf_dict = vdf.load(f)
            for user_id, user_dict in vdf_dict['users'].items():
                if 'AccountName' in user_dict and user_dict['AccountName'] == login:
                    steamID64 = int(user_id)
                    break
            if steamID64 is None:
                app_path = os.path.join(SteamPath, f"steam.exe")
                subprocess.Popen([ app_path, "-login",login,password] )
                if len(check_verify) == 0:
                    
                    check_verify[random.randint(0,100)] = {"login":login,"password":password,"amount":amount,"slot_id":slot_id}
                    
                else:
                    messagebox.showerror("Error","You cant start next account when the one is not started!")
            else:
                local_commend(steamID64,slot_id,amount,login,password)
    else:
        messagebox.showerror("Setup Error","Please first setup correct path/s for csgo and steam in settings")        
            
        
        
        
        
    
                                
                                    
                                    

        
        
        
        
        
    
    
    
    
    
    
        
        

def link_commend():
    
    steam_link = commend_frame.steam_link_entry.get()
    amount = commend_frame.amount_entry.get()
    commend_frame.steam_link_entry.delete(0, END)
    commend_frame.amount_entry.delete(0, END)
    slot  = commend_frame.slots_menu.get()
    
    if (steam_link == "" or amount == ""):
        commend_frame.error_show.configure(text="Please set link and amount.")
    else:
        steamID64 = get_steamID64(steam_link)
        if not steamID64:
            commend_frame.error_show.configure(text="Your link is wrong!")
        else:
            commend_frame.error_show.configure(text="")
            amount = int(amount)
            slot_id = int(slot.split(".")[0])
            slotdb = db.slotsdb.find_one({"_id":slot_id},)
            if not slotdb["enable"]:
                commend_frame.error_show.configure(text="This slot is disabled!")
            else:
                
                if amount <  0:     
                   commend_frame.error_show.configure(text=f"You cant use less than {slotdb['min_commends']} commends!")
                else:
                     
                    max_commends = (slotdb["max_commends"] if slotdb["max_commends"] != 0 else 9999999999) 
                    if amount >= max_commends: 
                        commend_frame.error_show.configure(text=("You cant you more than 0x commends!".replace("0x",str(max_commends))))
                        
                    else:  
                        
                          
                        gvalue = slotdb["currency"]  - amount
                        if  gvalue < 0:
                            commend_frame.error_show.configure(text="Slot balance is fully used till 00:00UTC")
                        
                        else:
                            
                            
                            balancedb = db.balancesdb.find_one({"userid":userid,"slot_id":slot_id}) ##### when user have idk 50 commends and start waiting and then again start waitng for 50 it ll allow it!!!
                            today_used = balancedb["today_used"] +amount
                            if today_used >= (slotdb["max_daily_commends"] if slotdb["max_daily_commends"] != 0 else 9999999): 
                                calc = slotdb["max_daily_commends"] -balancedb["today_used"]
                                max_daily = slotdb["max_daily_commends"]
                                messagebox.showerror("Balance Error",f"Your daily balance was used! u can use only {calc} of {max_daily}")
                                
                            else:
                                newamount = balancedb["amount"] - amount
                                                
                                if not newamount < 0:
                                    
                                    blacklist2 = db.blacklistdb.find_one({"steamID64":steamID64})
                                    if blacklist2 :
                                        messagebox.showerror("Blacklist Error",f"This steam account is blacklisted!\nTo get unban [join](https://discord.gg/jf5HT9feFu) in to support server https://discord.gg/jf5HT9feFu")
                                    else:
                                        print("s1")
                                        commenddb = db.serverusers.find_one({"steamID64":steamID64})
                                        reseller = userdb["reseller"] #idk reseller 
                                        if commenddb is None :
                                            tdb = db.serverusers.count_documents({"hwid":hwid})
                                            
                                            if tdb >= 5 or tdb >= 5 and userid != 640961296665149440:
                                                messagebox.showerror("Multicommending Error",f"You reach maximal limit of multicommending ({tdb})!")
                                                
                                            else:
                                                
                                                
                                                if tdb <= 3 or reseller:
                                                    start = False
                                                    if reseller and tdb !=0:
                                                        start = True
                                        
                                                                
                                                    else:
                                                        
                                                        start = True 
                                                    if start == True:
                                                        
                                                        start_commend_command(slot_id,amount,steamID64,balancedb)
                                                        

                                                                 
                                                                
                                                            
                                                        
                                                        
                                                    
                                                else:
                                                    messagebox.showerror("Multicommending Error","You cant commend more than 3 peoples!")
                                        else:
                                            commend_frame.error_show.configure(text="This account is commending!")
                                else:
                                    commend_frame.error_show.configure(text="Not enough commends!")
   

class balance_screen():
    def init():
        global  fr
        fr = CTkFrame(master=root)
        
    def pop_up():
        
        clear_all(balance_page,[fr])
        fr.pack()
       


def start_commend_command(slot_id,amount,steamID64,balancedb):
    slotdb = db.slotsdb.find_one_and_update({"_id":slot_id}, {"$inc": {"currency": -amount}},return_document = ReturnDocument.AFTER)      
    svdb = {"_id":steamID64,"userid":userid, "hwid":hwid, "amount": amount, "actualamount":0,"steamID64": steamID64, "status":"w8connect", "pendingmany":0, "commended":False,"lastup":datetime_utc, "slot_id":slot_id,  "chunk":"#0","chunk-info":"[0/0]","actualamount":0, "lastpending":0,"auto":False,"commend_channelid":slotdb["commend_channelid"],"old_balance":balancedb["amount"]}
    _id = db.serverusers.insert_one(svdb).inserted_id
    svdb["_id"] =_id
    select_profile(steamID64,svdb)
    commend_screen.update()
    



class CustomEntry(CTkEntry):
    def __init__(self, parent, valueChangeCallback=lambda x: print(x),tp="None", **kwargs):
        super().__init__(parent, **kwargs)

        # bind function callback when value of the text is changed
        self.bind("<KeyRelease>", lambda e: valueChangeCallback(tp,self.text))


    @property
    def text(self) -> str:
        return self.get()


    @text.setter
    def text(self, value) -> None:
        self.delete(0, 'end')
        self.insert(0, value)

class settings_screen():
    pass

    def init() :
        if  not "Settings" in regobj.HKEY_CURRENT_USER.Software.CommendBotPR:
            regobj.HKEY_CURRENT_USER.Software.CommendBotPR.set_subkey("Settings",{"SteamPath":"C:/Program Files (x86)/Steam","CSGOPath":"C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive","autoreconnect":False,"autostart":False})
        
        settings = regobj.HKEY_CURRENT_USER.Software.CommendBotPR.Settings
        
        global auto_reconnect,SteamPath,CSGOPath,auto_start,Arguments
        auto_reconnect =     ((True if settings["autoreconnect"].data == 1 else False)  if "autoreconnect" in settings else False)
        auto_start = ((True if settings["autostart"].data == 1 else False) if "autostart" in settings else False)
        SteamPath = (settings["SteamPath"].data if "SteamPath" in settings and os.path.exists(settings["SteamPath"].data) else None) 
        
        #defaultPath = os.path.join(SteamPath,f"steam.exe",)
        
        #shutil.copy2(defaultPath,appPath)            
        
        CSGOPath = (settings["CSGOPath"].data if "CSGOPath" in settings and os.path.exists(settings["CSGOPath"].data) else None)
        
        defarg = "-no-browser -noreactlogin -nodircheck -noconsole -skipinitialbootstrap -silent -noverifyfiles -norepairfiles -single_core -worldwide -language english -applaunch 730 -port 27020 -swapcores -noqueuedload -d3d9ex -disable_d3d9_hacks -dxlevel 90 -vrdisable -windowed -nopreload -limitvsconst -softparticlesdefaultoff -nohltv -noaafonts -nosound -novid -nojoy +violence_hblood 0 +sethdmodels 0 +mat_disable_fancy_blending 1 +r_dynamic 0 +exec autoexec.cfg -w 640 -h 480 -nomouse"
        Arguments = (settings["Arguments"].data if "Arguments" in settings else defarg)
        
        
        
        global settings_frame
        settings_frame = CTkFrame(master=root,width=650,height=400,fg_color="transparent")
        
        settings_frame.pack_propagate(False)
        settings_frame.pack_forget()
        
        CTkLabel(settings_frame,font=("Roboto",24,"bold"),text="Settings").pack(side=TOP,anchor=NW,padx=5)
        settings_body = CTkFrame(master=settings_frame,width=650,height=400,)
        settings_body.pack_propagate(False)
        settings_body.pack(fill=BOTH,expand=True,pady=(15,0))
        
        settings_left = CTkFrame(master=settings_body,width=433,height=400,fg_color="transparent")
        settings_left.pack_propagate(False)
        settings_left.pack(fill=BOTH,expand=True,side=LEFT)
        
        settings_right = CTkFrame(master=settings_body,width=216,height=400,fg_color="transparent")
        settings_right.pack_propagate(False)
        settings_right.pack(fill=BOTH,expand=True,side=RIGHT)
        
        settings_body_left = CTkFrame(master=settings_left,width=216,height=400,fg_color="transparent")
        settings_body_left.pack_propagate(False)
        settings_body_left.pack(fill=BOTH,expand=True,side=LEFT)
        
        settings_body_top = CTkFrame(master=settings_left,width=216,height=400,fg_color="transparent")
        settings_body_top.pack_propagate(False)
        settings_body_top.pack(fill=BOTH,expand=True,side=RIGHT)
        
        settings_body_right = CTkFrame(master=settings_right,width=216,height=400,fg_color="transparent")
        settings_body_right.pack_propagate(False)
        settings_body_right.pack(fill=BOTH,expand=True,)
        
        
        
        
        
        
        steam_frame = CTkFrame(settings_body_left,width=150,height=30,fg_color="#353639")
        steam_frame.pack_propagate(False)
        steam_frame.pack(pady=(10,5))
        
        if SteamPath and os.path.exists(SteamPath):
            
            imgl = CTkLabel(steam_frame,image=root.green,text=None)
            
            
        else:
            imgl = CTkLabel(steam_frame,image=root.red,text=None)
        
        imgl.pack(side=LEFT,padx=(15,0))
        CTkButton(steam_frame,command=lambda :select_dir("SteamPath",imgl),fg_color="transparent",text="Steam Path",hover_color=None,hover=False,border_spacing=0,width=120).pack(padx= 0)
        
        csgo_frame = CTkFrame(settings_body_left,width=150,height=30,fg_color="#353639")
        csgo_frame.pack_propagate(False)
        csgo_frame.pack(pady=5)
        
        if CSGOPath and os.path.exists(CSGOPath):
            imgls = CTkLabel(csgo_frame,image=root.green,text=None)
            
        else:
            imgls = CTkLabel(csgo_frame,image=root.red,text=None)
        imgls.pack(side=LEFT,padx=(15,0))
        CTkButton(csgo_frame,command=lambda :select_dir("CSGOPath",imgls),fg_color="transparent",text="CS:GO Path",hover_color=None,hover=False,border_spacing=0,width=120).pack(padx= 0)
        
        CTkButton(csgo_frame,command=lambda :clients[76561199095301693].sendall(f"open".encode()),fg_color="transparent",text="open",hover_color=None,hover=False,border_spacing=0,width=120).pack(padx= 0)
       
        
        
        arguments_frame = CTkFrame(settings_body_left)
        arguments_frame.pack(pady=5)
        CTkLabel(arguments_frame,font=("Roboto",13),text="Arguments",).pack(anchor=NW)
        arg_entry = CustomEntry(arguments_frame,settings_screen.update, "Arguments",fg_color="#353639")
        
        arg_entry.insert(END,Arguments)
        arg_entry.pack()
        boxframe = CTkFrame(settings_body_left)
        boxframe.pack(pady=10)
        
        
        autoreconnect_check = CTkCheckBox(boxframe,text="Auto-Reconnect",command=lambda  :settings_screen.update("autoreconnect",autoreconnect_check),checkbox_height=20,checkbox_width=20,font=("Roboto",13),border_width=0.5)
        if auto_reconnect:
            autoreconnect_check.select(True)
        else:
            autoreconnect_check.deselect(True)
        print(auto_reconnect)
        autoreconnect_check.pack(pady=(0,2),anchor=W)
        global autostart_check
        autostart_check = CTkCheckBox(boxframe,text="Auto-Start",command=lambda  :settings_screen.update("autostart",autostart_check),checkbox_height=20,checkbox_width=20,font=("Roboto",13),border_width=0.5,)
        if auto_start:
            autostart_check.select(True)
        else:
            autostart_check.deselect(True)
        if auto_reconnect == True:
            
            autostart_check.configure(state=NORMAL)
        else:
            autostart_check.configure(state=DISABLED)
        autostart_check.pack(pady=(2,0),anchor=W)
        
        
        
        
        
        
        end_commend = CTkFrame(settings_body_left)
        CTkLabel(end_commend,font=("Roboto",13),text="On Commending Finish",).pack(anchor=NW)
        global end_task
        end_task = CTkOptionMenu(end_commend,values=["Do nothing","Turn off PC","Close CS:GO","Close Panel&CS:GO"],command=lambda i :settings_screen.update("endtask",i),dynamic_resizing=False)
        
        end_task.pack()
        if "endtask" in settings:
            end_task.set(settings["endtask"].data)
        end_commend.pack()
        
        
        #CTkButton(settings_body_right,command=run_command).pack()
        
        
    
    def pop_up():
        clear_all(settings_page,[settings_frame])
        settings_frame.pack(fill=BOTH,expand=True,pady=(15,15),padx=20)
    def update( type,txt ):
        
        if type == "Arguments":
            regobj.HKEY_CURRENT_USER.Software.CommendBotPR.set_subkey("Settings",{str(type):str(txt)})
            global Arguments
            Arguments = str(txt)
        elif type == "autoreconnect":
            
            regobj.HKEY_CURRENT_USER.Software.CommendBotPR.set_subkey("Settings",{str(type):txt._check_state})
            global auto_reconnect,autostart_check
            auto_reconnect = txt._check_state
            if auto_reconnect == True:
            
                autostart_check.configure(state=NORMAL)
            else:
                
                autostart_check.configure(state=DISABLED)
            for id,client in clients.items():               
                client.sendall(f"autoreconnect-{int(auto_reconnect)}".encode())
                
        elif type == "autostart":
            
            regobj.HKEY_CURRENT_USER.Software.CommendBotPR.set_subkey("Settings",{str(type):txt._check_state})
            global auto_start
            auto_reconnect = txt._check_state
        elif type == "endtask":
            
            regobj.HKEY_CURRENT_USER.Software.CommendBotPR.set_subkey("Settings",{str(type):txt})
        
            
         
            




def select_dir(save_as,imgl):
    dir = filedialog.askdirectory(mustexist=True)
    if os.path.exists(dir):
        regobj.HKEY_CURRENT_USER.Software.CommendBotPR.set_subkey("Settings",{save_as:dir})
        imgl.configure(image=root.green)
        if "CSGOPath" == save_as:
            global CSGOPath
            CSGOPath = dir
        else:
            global SteamPath
            SteamPath = dir
            
        
        
    
        
shutting_msg = "Disconnect: Server shutting down."
relog_msg = "Disconnect: Relog to continue."
timed_msg = "Server connection timed out."
start_msg = "Ping measurement completed"
sleep_sec = 20

    
    





def get_server() -> dict:
    beststerver = (1,1)
    
    for gid,server in allserverscs.items():
        try:
            info: a2s.SourceInfo = a2s.info((server["ip"],server["port"]))
        except:
            pass
                    
        else:
            avg =  info.player_count / info.max_players 
            if avg < beststerver[1]:
                beststerver = (gid,avg)     
    return allserverscs[beststerver[0]]    
     

def do_stuff(count=0):
    
    while True:
        time.sleep(10)
        
        checker()
        commend_screen.update()
        count+=10
        if count >= 3600:
            global userdb
            if userdb:=db.usersdb.find_one({"_id":userdb["_id"]}):
                print("sub-check")
                pass
        
    
    
    
    

def checker():
    if len(check_verify) != 0:
        if SteamPath:
            
            app_path = os.path.join(SteamPath, f"steam.exe")
            
            for id ,data in  check_verify.items():
                del check_verify[id]
                subprocess.Popen([ app_path, "-shutdown"] )
                time.sleep(1)
                steamID64 = None 
                with open(os.path.join(SteamPath,"config","loginusers.vdf"), 'r',encoding='utf-8') as f:
                    vdf_dict = vdf.load(f)
                    
                for user_id, user_dict in vdf_dict['users'].items():
                    if 'AccountName' in user_dict and user_dict['AccountName'] == data["login"]:
                        steamID64 = int(user_id)
                        break
                if steamID64 is None:
                    messagebox.showerror("Account init error",f"The account {data['login']} was not init")
                else:
                    if "shared_secret" in data:
                        shared_secret = data["shared_secret"]
                    else:
                        shared_secret = None
                    local_commend(steamID64,data["slot_id"],data["amount"],data["login"],data["password"], shared_secret)
        else:
            print("Steam path is not set ")            


                    
def local_commend(steamID64:int ,slot_id:int,amount:int,login:str,password:str,shared_secret=None): # login commending
    
    slotdb = db.slotsdb.find_one({"_id":slot_id})
    if not slotdb["enable"]:
        messagebox.showerror("Slot error","This slot is disabled!")
        return True
    else:
        
        if amount <  0:     
            messagebox.showerror("Slot balance error",f"You cant use less than {slotdb['min_commends']} commends!")
            return True
        else:
                
            max_commends = (slotdb["max_commends"] if slotdb["max_commends"] != 0 else 9999999999) 
            if amount >= max_commends: 
                messagebox.showerror("Slot balance error",("You cant you more than 0x commends!".replace("0x",str(max_commends))))
                return True
                
            else:  
                
                    
                gvalue = slotdb["currency"]  - amount
                if  gvalue < 0:
                    messagebox.showerror("Slot balance error","Slot balance is fully used till 00:00UTC, try different amount.")
                    return True
                
                else:
                    
                    
                    balancedb = db.balancesdb.find_one({"userid":userid,"slot_id":slot_id}) ##### when user have idk 50 commends and start waiting and then again start waitng for 50 it ll allow it!!!
                    today_used = balancedb["today_used"] +amount
                    if today_used >= (slotdb["max_daily_commends"] if slotdb["max_daily_commends"] != 0 else 9999999): 
                        calc = slotdb["max_daily_commends"] -balancedb["today_used"]
                        max_daily = slotdb["max_daily_commends"]
                        messagebox.showerror("Balance Error",f"Your daily balance was used! u can use only {calc} of {max_daily}")
                        return True
                        
                    else:
                        newamount = balancedb["amount"] - amount
                                        
                        
                        if not newamount < 0:
                
                            blacklist2 = db.blacklistdb.find_one({"steamID64":steamID64})
                            if blacklist2 :
                                messagebox.showerror("Blacklist Error",f"This steam account is blacklisted!\nTo get unban [join](https://discord.gg/jf5HT9feFu) in to support server https://discord.gg/jf5HT9feFu")
                                return True
                            else:
                                print("s1")
                                commenddb = db.serverusers.find_one({"steamID64":steamID64})
                                reseller = userdb["reseller"] #idk reseller 
                                if commenddb is None :
                                    tdb = db.serverusers.count_documents({"hwid":hwid})
                                    
                                    if tdb >= 5 or tdb >= 5 and userid != 640961296665149440:
                                        messagebox.showerror("Multicommending Error",f"You reach maximal limit of multicommending ({tdb})!")
                                        return True
                                        
                                    else:
                                        
                                        
                                        if tdb <= 3 or reseller:
                                            
                                            
                                            print("start commend")
                                            
                                            
                                            
                                            global csgo_started
                                            
                                            
                                            clientPath = os.path.join(LIB_PATH,"client.exe")
                                            
                                            
                                            if not steamID64 in clients:
                                                print("starting")
                                                steam32id = int(steamID64) - 76561197960265728
                                                ruserdata = os.path.join(SteamPath,"userdata",str(steam32id))
                                            
                                                start_commend_command(slot_id,amount,steamID64,balancedb)
                                                global wincounter
                                                


                                                print(wincounter)
                                                
                                                subprocess.Popen([ clientPath,SteamPath,CSGOPath,str(steamID64),"-login",login,password,"-no-browser" ,"-noreactlogin" ,"-silent" ,"-worldwide" ,"-language" ,"english","-applaunch", "730", '+con_logfile' ,'console.log' ] + Arguments.strip().split(" ")+ ["-x", str(wincounter), "-y", "0" ],creationflags=subprocess.CREATE_NEW_CONSOLE)
                                                wincounter += 383
                                                if shared_secret:
                                                    accounts[steamID64]["shared_secret"] = shared_secret
                                                    
                                                    while not steamID64 in clients:
                                                        time.sleep(2)
                                                    s = clients[steamID64]
                                                    print("popen start")
                                                    time.sleep(10)
                                                    s.sendall(f"popen".encode())
                                                                                                                    
                                                
                                            else:
                                                    start_commend_command(slot_id,amount,steamID64,balancedb)
                                                
                                                        
                                                    
                                                
                                                
                                                
                                            
                                        else:
                                            messagebox.showerror("Multicommending Error","You cant commend more than 3 peoples!")
                                            return True
                                else:
                                    commend_frame.error_show.configure(text="This account is commending!")
                                    return True
                        else:
                            commend_frame.error_show.configure(text="Not enough commends!")
                            return True
                       
                                                
                    
                
                #global wincounter
                #subprocess.Popen([ clientPath,SteamPath,CSGOPath,str(steamID64), "-login","*","*","-applaunch", "730", '+con_logfile' ,'console.log' ] + Arguments.strip().split(" ") + ["-x", str(wincounter), "-y", "0" ],creationflags=subprocess.CREATE_NEW_CONSOLE)
                #wincounter += 383
       


if __name__ == "__main__":
    
    
    root = App()
    
    root.mainloop()
    
    stop_server = True
    print("bye") 
    
    os.kill(os.getpid(), signal.SIGTERM)
    
    
    
    
    


