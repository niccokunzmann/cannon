import socket,thread,random,time

__version__=("cannoncom",0,0)
socket.setdefaulttimeout(5)

schreiben=False

def schreibe(*nachricht):
    global schreiben
    if schreiben:
        s=""
        for i in nachricht:
            s+=str(i)+" "
        print s

split="<:::>"

def addrtest(addr=('localhost',0)):
    if addr[0] in ('0.0.0.0',"localhost"):
        return socket.gethostbyname(socket.gethostname()),addr[1]
    return addr

class com:
    def __init__(self,name="random"):
        if name=="random":
            from main import files
            self.name="com"+files.int_string(int((255**2)*random.random()),(split[0],))
        else:
            self.name=name
        self.socket=socket.socket(2,1)
        self.socket.bind(("",0))
        self.socket.listen(1)
        self.clients={}#name:[str1, ...]
        self.server_connection={}#name:obj
        self.accept=True
        self.accepting=False#ob _accept_thread noch in process
        self.empfunk=[]#[ (funk ,(args,)), ... ]
        self.wait_accept={}#str(addr):name/None
        self.block_connect={}#ip:port
        self.intfunk=[]#[ (funk ,(args,)), ... ]
        
        self.accept_thread()

    def get_addr(self,):
        """=> (ip,port)
        => eigene netzwerkadresse
        sie ist die adresse,
            unter der man das objekt im netzwerk erreichen kann"""
        return addrtest()[0],self.socket.getsockname()[1]

    def accept_thread(self):
        """
        benutze lieber start_accept.
        """
        thread.start_new(self._accept_thread,())
    def _accept_thread(self):
        self.accepting=True
        while self.accept:
            obj=0
            while not obj:
                try:
                    obj,addr=self.socket.accept()
                except socket.timeout:
                    pass
#                    print "time out"
            if addr[0] not in self.block_connect and self.accept:
                thread.start_new(self.recv,(obj,addr))
            else:
                schreibe("hack blocked:",addr)
        self.accepting=False
    def start_accept(self):
        """startet den thread zur annahme vom verbindungen.
        """
        self.accept=True
        if not self.accepting:
            self.accept_thread()
    def stop_accept(self):
        """stoppt die annahme von verbindungen.
        es werden keine weiteren verbindungen angenommen."""
        self.accept=False

    def recv(self,obj,addr):
        """wird genutz, wenn eine verbindung eingegangen ist.
        sollte nicht manuell genutzt werden."""
        try:
            nachricht=obj.recv(1024)
        except socket.timeout:
            nachricht=[]
        nachricht=nachricht.split(split)
        schreibe(nachricht)
        if len(nachricht)>=2:
            name,addr2=nachricht[:2]
            name=self.testname(name)
        if len(nachricht)==2:
            try:
                self._connect(name,eval(addr2),)
            except socket.timeout:
                schreibe("connectin to",addr2,"refused")
                return
        elif len(nachricht)==4 and nachricht[3]=="accepted" and nachricht[1]==str(self.get_addr()):
            schreibe(self.name,self.wait_accept)
            self.wait_accept[nachricht[2]]=nachricht[0]
            schreibe(self.name,self.wait_accept)
        else:
            schreibe("hack failed",addr)
            self.block_connect[addr[0]]=addr[1]
            return
        self.clients[name]=[]
        while name in self.clients:
            try:
                while name in self.clients:
                    nachricht=obj.recv(1024)
                    self.clients[name].append(nachricht)
                    self._empfunk(nachricht,eval(addr2),name)
            except socket.timeout:
                pass
                #print self.name,":  timeout recv"
            except socket.error:
                self._interrupted("interrupted",eval(addr2),name)
                break
#            except:
#                schreibe(self.name,":  error - empangen von:",name)
    def connect(self,addr):
        if addr in [self.server_connection[k].getpeername() for k in self.server_connection]:#nicht 2x connect
            return 
        s=socket.socket(2,1)
        schreibe(self.name,"connect to:",addrtest(addr))
        str_addr=str(addr)
        self.wait_accept[str_addr]=None
        s.connect(addrtest(addr))
        s.send(self.name+split+str(addrtest(self.get_addr())))
        while self.wait_accept[str_addr]==None:
            schreibe("wait",self.name,":",self.wait_accept)
#            time.sleep(1)
        self.server_connection[self.wait_accept[str_addr]]=s
        return self.wait_accept[str_addr]
    def _connect(self,name,addr):
        s=socket.socket(2,1)
        s.connect(addrtest(addr))
        s.send(self.name+split+str(addrtest(addr))+split+str(addrtest(self.get_addr()))+split+"accepted")
        self.server_connection[name]=s
    def send(self,name,nachricht):
        self.server_connection[name].send(nachricht)
    def send_all(self,nachricht):
        """sendet die nachricht an alle verbundenen objekte"""
        for name in self.server_connection:
            self.send(name,nachricht)

    def get_clients(self):
        """=> liste der namen der clients"""
        return self.clients.keys()
    def get_servers(self):
        """=> liste der namen der server"""
        return self.server_connection.keys()

    def bind_emp(self,funk=None,*arg):
        """
        funk==None:
            alle funktionen loeschen
        arg:
            nachricht
            com
            addr
            name
        """
        if funk == None:
            self.empfunk=[]
        else:
            self.empfunk.append((funk,arg))
    def bind_interrupt(self,funk=None,*arg):
        """ausgeloest, wenn sockets voneinander nicht ordnungsgemaess getrennt
        sonst wie bind_emp, nur nachricht=="connection interrupted".
        """
        if funk == None:
            self.intfunk=[]
        else:
            self.intfunk.append((funk,arg))
    bind_int=bind_interrupt
    def _interrupted(self,nachricht,addr,name):
        d={"nachricht":nachricht,"addr":addr,"com":self,"name":name}
        for f in self.intfunk:
            f[0](*[d[arg] for arg in f[1]])
    def _empfunk(self,nachricht,addr,name):
        d={"nachricht":nachricht,"addr":addr,"com":self,"name":name}
        for f in self.empfunk:
            f[0](*[d[arg] for arg in f[1]])
    def testname(self,name):
        """=> (abgewandelter) name """
        while name in self.server_connection.keys()+self.clients.keys():
            name+=" "
        return name

class com2(com):
    def __init__(self,name="random"):
        """
        erzeugt ein objekt der klasse com2,
            dass zur kommunikation in netzwerken (TCP/IP)
            genutzt werden kann.
        name gibt den namen an,
            wenn er nicht angegeben ist,
            wird er zufaellig gewaehlt.
        die ressource "block_connect" ist die einzige,
            die sie veraendern sollten.
            block_connect - gibt die zu blockenden adressen an:
                [ip] => port (geblockte adressen auslesen) 
                [ip] = port => alle anfragen gleicher ip werden geblockt
                block_connect wird automatisch erweitert,
                    wenn jemand eine anfrage stellt,
                    die nicht die form einer der com2 objekte hat.
                    es werden ip und port vermerkt
                    und koennen zurueck verfolgt werden.
        """
        com.__init__(self,name)
        self.empf=[]
        self.conf=[]
        self.disf=[]
        com.bind_emp(self,self._empfangen,"nachricht","addr","name")
        self.bind_int(self._empfangen,"nachricht","addr","name")
    
    def bind(self,sequence,funk=None,*arg):
        """
        sequence:
            connect
            empfangen
            disconnect
        funk==None:
            alle funktionen loeschen
        arg:
            nachricht
            com
            addr
            name
        ruft die funktion funk
        mit den in arg angegebenen parametern
        wenn eine nachricht empfangen wurde ("empfangen")
        wenn sich ein anderes socket verbunden hat ("connect")
        wenn sich ein anderes socket getrennt hat ("disconnect")
        """
        f={"connect":self.conf,"empfangen":self.empf,"disconnect":self.disf}
        if funk == None:
            f[sequence].list()
        else:
            f[sequence].append((funk,arg))

    def bind_emp(self,funk=None,*arg):
        """
        funk==None:
            alle funktionen loeschen
        arg:
            nachricht
            com
            addr
            name
        ruft die funktion funk
        mit den in arg angegebenen parametern
        wenn eine nachricht empfangen wurde
        """
        if funk == None:
            self.empf.list()
        else:
            self.empf.append((funk,arg))
    def connect(self,addr):
        """
        verbindet das objekt mit einem anderen com2 objekt
            mit der addresse addr.
        wird es mit einem bereits mit ihm selbst verbundenenobjekt verbunden,
            so wird die verbindung zuerst getrennt,
            um sie danach wieder neu auf zu bauen.
        sollten zwei objekte den selben namen besitzen,
            so wird das zuletzt verbundene mit leerzeichen aufgefuellt,
            bis einen einzigartigen namen besitzt.
        """
        if addr in [self.server_connection[k].getpeername() for k in self.server_connection]:#nicht 2x connect
            self.disconnect(addr=addr,wait=True)
        name=com.connect(self,addr)
        if name!=None:self._send(name,"connect"+split)
        return name
    def disconnect(self,name=None,addr=None,wait=False):
        """
        trennt die verbindung zu einem objekt.
        name gibt den namen an - 
            ausserdem kann auch die netzwerkadresse addr genutzt werden,
            der name geht aber vor.
        wait gibt an, ob sofort zurueckgekehrt werden soll
            oder erst dann wenn die verbindung wirklich beendet wurde.
        tipp:
            sie koennen in wait eine gefuellte liste plazieren,
            die sie leeren, wenn sie dringend zurueckkehren wollen.
        """
        if name==None:
            if addr==None:
                return
            name=self.addr_name(addr)            
        self._send(name,"disconnect"+split)
        self.clients[name].append("disconnect")
        if wait:
            while name in self.clients:
                schreibe(self.name,"wait disconnect")

    def send(self,name,nachricht=None):
        """
        sendet die nachricht an das objekt mit dem namen
        sollte keine nachricht angegeben sein, so wird verfahren,
            alsob sie im namen stehen wuerde - name wird an alle gesendet.
        """
        if nachricht==None:
            self.send_all(name)
            return
        self._send(name,"empfangen"+split+nachricht)
    _send=com.send
    
    def _empfangen(self,nachricht,addr,name):
        if nachricht=="" and self.clients[name][-2:]==["disconnect",""]:
            self.clients.pop(name)
            self.server_connection.pop(name)
            return
        elif nachricht=="interrupted":
            self.clients.pop(name)
            self.server_connection.pop(name)
            nachricht+=split
        if nachricht=="":
            schreibe("error: nachricht an",self.name,"von",name,": keine nachricht")
            return
        i=nachricht.index(split)
        nachricht=[nachricht[:i],nachricht[i+len(split):]]
        d={"nachricht":nachricht[1],"addr":addr,"com":self,"name":name}
        f={"connect":self.conf,"empfangen":self.empf,"disconnect":self.disf,"interrupted":self.disf}
        for funk in f[nachricht[0]]:
            funk[0](*[d[arg] for arg in funk[1]])
        if nachricht[0]=="disconnect":
            self.clients.pop(name)
            self.server_connection.pop(name)

    def __getitem__(self,name):
        """__getitem__(self,name) <==> self[name]
        gibt die hinterlassenen nachrichten von name zurueck.
        sollte das objekt die anfrage zum verbindungsaufbau erhalten haben,
            so ist der erste string leer.
        """
        return [nachricht[nachricht.index(split)+len(split):] for nachricht in self.clients[name]]
    def __setitem__(self,name,n):
        """__setitem__(self,name,n) <==> self[name]=n
        entfernt die ersten n nachrichten
        """
        self.clients[name]=self.clients[name][n:]
    def name_addr(self,name):
        """name => addr"""
        return self.serverconnection[name].getpeername()
    def addr_name(self,addr):
        """addr => name"""
        if addr==self.get_addr():
            return self.name
        for i in self.server_connection.items():
            if addr==i[1].getpeername():
                return i[0]

if not "idlelib" in dir() and __name__=="__main__":
#if 1:
    schreiben=True
    c=com2("c")
    v=com2("v")
    def f(*arg):
        if not "idlelib" in dir():
            schreibe(arg)
    v.bind_emp(f,"nachricht","com","addr")
    schreibe("v:",v.get_addr())
    schreibe("c:",c.get_addr())
    i=c.connect(v.get_addr())
    schreibe("succesfully connected to:",i)
    c.send_all("c - sendet")
    if not "idlelib" in dir():
        while 1:exec raw_input()
