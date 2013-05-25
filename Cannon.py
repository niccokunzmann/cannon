from Tkinter import *
from math import *
import time,random,winsound,thread,tkFileDialog,tkMessageBox,sys,os,socket
sys.path.append(sys.path[0]+"\\modules")
from cannoncom import com2,schreiben
schreiben=True

###tkMessageBox - ersetzen
sostiges={}#fuer kartenspeicherung
hintergrundfarbe="#DDF"
untergrundfarbe="gray66"
suddendeath=0
mapartc={"Standard - Doppelberg":"sin(i/100)*width/10+height/10",\
         "Standard - Mittelberg":"sin(i/100-3)*width/10+height/10",\
         "Standard - Das Tal":"abs(i-width/2)",\
         "Standard - Himalaya":"(sin(i/100)*height/7+abs(i/2-width/2))/1.4",\
         "Standard - Flachland":"1",\
         "Standard - Klippen":"i/5",\
         "Standard - Doppeltal":"i%height/2",\
         "Standard - Hochland":"height/5*3",\
         "Standard - Parabeltal":"(i-width/2)**2/350000.0*height"}
mapart="sin(i/100)*100+100"
zeit2=0
(bunkernr,reliefnr,reliefaendernr)=(0,)*3
ende=0
height=700
width=1000
relief=[]
g=10
spanz=0
bupos=[]
bunkerteilanz=7
move=[]
shot=[]
ladekraft=100
gametime=0
reliefg=[]
reliefgnr=0
maxspieleranz=5
maxspieleranz+=1
maxwinkel=90
minwinkel=-90
t2=[{"Left":2,"Right":3,"Up":7,"Down":11,"End":5,"Next":5},\
   {"q":2,"w":11,"e":3,"2":5,"3":7},\
   {"4":2,"5":11,"6":3,"plus":5,"8":7},\
   {"c":2,"v":11,"b":3,"f":5,"g":7},\
   {"i":2,"o":11,"p":3,"0":7,"9":5},\
   {"comma":2,"minus":3,"l":7,"period":11,"space":5},2]#2-links#3-rechts#5-shot#7-hoch  ,  11-runter
t1=[{"Left":2,"Right":3,"Up":7,"Down":11,"End":5,"Next":5},\
   {"q":2,"w":11,"e":3,"2":5,"3":7},\
   {"c":2,"v":11,"b":3,"f":5,"g":7},\
   {"i":2,"o":11,"p":3,"0":7,"9":5},\
   {"comma":2,"minus":3,"l":7,"period":11,"space":5},1]#2-links#3-rechts#5-shot#7-hoch  ,  11-runter
t=t2[:]
schussart=[ [0,"o",5,"",2,1,["Ball",10,"black"],10,[50,"::Standardschuss"]], \
            [1,"*",10,"",0,-2,["Ball",10,untergrundfarbe],4,[16,u"sch\u00fcttet den Berg auf"]], \
            [2,"+",0,"H",0,0,["",0,"red"],0,[200,u"Erste Hilfe P\u00e4ckchen"]],\
            [3,"-",22,"E",1,1,["Linie",15,"green4"],2,[51,"Hohe Sprengkraft"]],\
            [4," /\ ",7,"E",9,1,["Dreieck",15,"red3"],2,[53,"Viel Schaden"]],\
            [5,"R",14,"E",4,1,["Rakete",15,"gray22"],2,[32,"Normale Rakete"]],\
            [6,"#",8,"K(0,0,15,4,5,5)",1,1,["Rechteck",10,"red4"],0,[123,u"P\u00e4ckchen mit Aufschlagz\u00fcnder"]],\
            [7,"S",0,"S",0,0,["",0,"white"],0,[195,"Schutzschild"]],\
            [8,"<>",8,"K(0,8)",1,1,["Rechteck",5,"blue4"],0,[142,u"rekursives P\u00e4ckchen"]],\
            [9,"%",3,"",3,1,["Schrot",3,"green"],0,[46,"einfacher Schrot"]],\
            [10,"!#!",8,"K(0,4,4,10,6)",1,1,["Rechteck",20,"yellow"],0,[507,u"!!Super P\u00e4ckchen rekursiv!!"]],\
            [11,"!%!",6,"E",4,1,["Schrot",4,"magenta"],0,[69,"!!Superschrot!!"]],\
            [12,"!*!",30,"",0,-2,["Ball",20,untergrundfarbe],0,[33,u"verbessert Bergaufsch\u00fctten"]],\
            [13,"!L!",2,"T(2)K(3,3)",4,1,["Linie",23,"green4"],0,[102,"Flugsprenger"]],\
            [14,"!R!",28,"E",10,1,["Rakete",25,"gray22"],0,[113,"!!Riesenrakete!!"]],\
            [15,"G",1,"G(15)",3,1,["Rakete",10,"green3"],2,[80,"Gift"]],\
            [16,"F",1,"D(2.4)K("+str([18 for n in range(12)])[1:-1]+")",3,1,["Ball",20,"red3"],0,[703,"Feuerwerk"]],\
            [17,"BB",30,"BB,E",0,0.5,["Rechteck",20,"white"],0,[374,"Bunkerbeamer"]],\
            \
            [18,"",5,"D(1.8)K("+str([5 for n in range(10)])[1:-1]+")",1,1,["Dreieck",6,"blue2"],0,[10,"::Feuerwerk2"]],\
            [19,u"\u06de",37,"st(7,0.5)",17,1,["Stern",20,"blue2"],0,[418,"Starattack"]],\
            ]
#nummer,zeichen,sprengweite,anmerkung,schaden,sprengtiefe,[art,groesse,farbe],anzahl,[Preis,Kaufmenu]
schussart2={"Ball":("oval",),"Linie":("line",),"Rechteck":("rectangle",),\
            "Rakete":("polygon",),"Luftschiff":("oval","polygon"),"Dreieck":("polygon",),\
            "Schrot":("oval","oval","oval","oval","oval",),"Stern":("polygon",)}
spielersch=0
schutzschild=[]
kaufspieleract=0
timervar={}
optionvar=""
giftvar=[0]*7
listenvar={}
for i in ["geld", "spargeld", "siege", "schussanz", "schaden", "besiegte", "treffer"]:
    listenvar[i]=[0]*7
listenvar["runden"]=0
xyposaex=0
xyposaey=0
clients=[]
sendenvar=""
emp=0
senden=[]
relief2=[]
reliefg2=[]
spielernummer=0
spielerwechselzeit=0
schneevar=[0,0,20]
fallschirmvar=[]
sound=1
fi=[0,80]
default=[]
defaultround=[]
zoom={"height":1,"width":1}
nutzbare_var={}
iconifypause=0
coordspos=(-20,-20,-30,-30)
lanvar={}
#LAN
    #Host
def mehrspielerlan(event):
    event.widget.master.grid_forget()
    lanmenuframe.grid(row=1,column=1)
def lanbeitreten(event):
    event.widget.master.grid_forget()
    beitretenframe.grid(row=1,column=1)
def lanhosten(event):
    event.widget.master.grid_forget()
    hosten1frame.grid(row=1,column=1)
def hostenmenu2(event):
    global lanvar
    if event.widget.get()=="":
        event.widget.bell()
        return
    lanvar["com"]=com2(event.widget.get())
    event.widget.master.grid_forget()
    lanstartbutton.pack()
    hosten2frame.grid(row=1,column=1)
    hostenaddrlabel.config(text="IP:\t"+lanvar["com"].get_addr()[0]+"\nPort:\t"+str(lanvar["com"].get_addr()[1]))
    def connect(name,addr):
        lansplist.insert("end",name.center(15)+" - "+addr[0]+" : "+str(addr[1]))
    lanvar["com"].bind("connect",connect,"name","addr")
    connect(lanvar["com"].name,lanvar["com"].get_addr())


    #client
def client1menu(*k):
    print "connect to host"
    if clientnameentry.get()=="":return
#    try:
    if 1:
        port=int(clientportentry.get())
        ip=clientipentry.get()
        lanvar["client"]=com2(clientnameentry.get())
        lanvar["client"].connect((ip,port))
#    except:pass
    lanstartbutton.pack_forget()
##ende LAN

def showerror(title="",message="",sign="!",cnf={},**kw):
    stop=Toplevel()
    stop.title(title)
    stop.iconbitmap("error")
    stop.protocol("WM_DELETE_WINDOW")
    slabelsign=Label(stop,text="!",font=("Lucida Console",20,"bold"),foreground="red3")
    slabeltext=Label(stop,text=message)
    slabelsign.pack(side="left")
    slabeltext.pack(side="right")
    sbutton=Button(stop,text="ok",command=stop.quit)
    sbutton.pack(side="bottom")
    stop.mainloop()
    stop.destroy()
    return "ok"
 

def canvas_create(kind,*pos,**kw):
    if pos[:]==(pos[0],):pos=pos[0]
    if "cnf" in kw:
        cnf=kw["cnf"]
        kw.pop("cnf")
    else:cnf={}
    cnf.update(kw)
    global coordspos,create_dict
    t=False
    for i in range(100):
        try:
            if kind in ("text","window","image"):
                find_all=create_dict[kind][0](coordspos[0:2])
            else:
                find_all=create_dict[kind][0](coordspos)
##            exec "coords%s"%(k,)
            canvas.itemconfigure(find_all,cnf=cnf)
            canvas_coords(find_all,pos)
            t=True
            break
        except TclError:pass
        except ValueError:pass
    assert t#create, wrong arguments
    return find_all
def canvas_create_rectangle(*pos,**kw):
    return (canvas_create("rectangle",pos,cnf=kw))
def canvas_create_arc(*pos,**kw):
    return (canvas_create("arc",pos,cnf=kw))
def canvas_create_oval(*pos,**kw):
    return (canvas_create("oval",pos,cnf=kw))
def canvas_create_polygon(*pos,**kw):
    return (canvas_create("polygon",pos,cnf=kw))
def canvas_create_line(*pos,**kw):
    return (canvas_create("line",pos,cnf=kw))
def canvas_create_text(*pos,**kw):
    return (canvas_create("text",pos,cnf=kw))
def canvas_create_window(*pos,**kw):
    return (canvas_create("window",pos,cnf=kw))
def canvas_create_image(*pos,**kw):
    return (canvas_create("image",pos,cnf=kw))
def canvas_delete(nr):
    return canvas_try(canvas.delete,nr)
def canvas_insert(nr,pos,text):
    canvas.insert(nr,pos,text)
def canvas_dchars(*arg):
    canvas.dchars(arg[0],arg[1],arg[2:])
def canvas_try(funk,*arg):
    t=0
    if arg[:]==(arg[0],):arg=arg[0]
    for i in range(100):
        try:
            ret=funk(arg)
            t=1
            break
        except TclError:pass
        except ValueError:pass
    assert t#coords, wrong arguments
    return ret

def iconify():
    global iconifypause
    iconifypause=1
    root.overrideredirect(0)
    root.iconify()
def deiconify():
    global iconifypause
    iconifypause=0
    root.deiconify()
    root.overrideredirect(1)
def coordsrelief():
    global reliefnr,relief,height,width,zoom
##    var="canvas.coords("+str(reliefnr)+",0,"+str(height)
##    for i in xrange(width+1):
##        var+=str(i)+","+str(relief[i])
##    var+=","+str(width)+","+str(height)+")"
##    eval(var)
    for i in range(width+1):
        canvas_coords(i+1,i*zoom["width"],zoom["height"]*height,i*zoom["width"],relief[i]*zoom["height"])
##        coords(i+1,i,height,i*,relief[i])
def canvas_coords(*k):
    global zoom,width,heigth,coords
##    n=0
##    f=()
##    for i in k:
##        if n%2==0:#x
##            f+=(i*zoom["width"]*width,)
##        else:
##            f+=(i*zoom["height"]*height,)
##        n+=1
##    var="canvas.coords"+str(f)
    t=0
    if k[1:]==(k[1],):k=(k[0],)+k[1]
    for i in range(100):
        try:
            coords(k[0],k[1:])
##            exec "coords%s"%(k,)
            t=1
            break
        except TclError:pass
        except ValueError:pass
    assert t#coords, wrong arguments
#    eval(var)
def execute_file(path):
    exec file(path,"r").read()
''' KI KI KI KI KI KI KI KI'''
"""
"error0" - zu wenig geld
"error1" - max schussanz erreicht
"error2" - axcess denied
"error3" - wrong keyword
"error4" - wrong value
"complete" - erfolgreich berechnet
"""
def KIset(k,kw,wert):
    global bupos,move#2-links#3-rechts#5-shot#7-hoch  ,  11-runter
    if kw=="winkel":#ereignis,zeit,###,schussart
        if abs(wert)<=90:
            if bupos[k][2]<wert:
                move[k][0]*=2
                while bupos[k][2]<wert:
                    time.sleep(0.05)
                move[k][0]/=2
                bupos[k][2]=wert
            elif bupos[2]>wert:
                move[k][0]*=3
                while bupos[k][2]>wert:
                    time.sleep(0.05)
                move[k][0]/=3
                bupos[k][2]=wert
        else:return "error4"
    elif kw=="schussart":
        if bupos[k][4][wert]>0:
            move[k][0]*=7
            while move[k][3]!=wert:
                time.sleep(0.05)
            move[k][0]/=7
        else:return "error4"
    elif kw=="ladung":# insert=int(time.time()-move[k][1)*ladekraft/4))print KIset(0,"ladung",20)/ thread.start_new(KIset,(0,"ladung",20))
        if wert<=99:#append=(time.time()-move[k][1])*ladekraft
            move[k][0]*=5
            while move[k][1]==0:
                time.sleep(0.05)
            while ((time.time()-move[k][1])*ladekraft/4)<wert:
                time.sleep(0.05)
##            print (time.time()-move[k][1])*ladekraft/4
            move[k][0]/=5
        else:return "error4"
    else:return"error3"
    return "complete"
def KIget(k,*kw):
    global bupos
    r=()
    for i in kw:
        if "pos" == i:r+=((bupos[k][0],bupos[k][1]),)
        elif "winkel" == i:r+=(bupos[k][2],)
        elif "leben" == i:r+=(bupos[k][3],)
        elif "geld" == i:r+=(bupos[k][5],)
        else:r+=("error3",)
    return r
    #x,y,winkel,leben,schussanz,geld,unendlich,ABO
def KIkauf(k,nr):
    if "::" in schussart[nr][8][1]: return "error2"
    if schussart[nr][8][0]>bupos[k][5]:return "error0"
    if bupos[k][4][nr]>9:return "error1"
    bupos[k][5]-=schussart[nr][8][0]
    bupos[k][4][nr]+=1
    return "complete"
def get_cheapest():
    s=get_most_exp()
    for i in schussart:
        if "::" in i[8][1]:continue
        if s[1]>i[8][0]:s=(i[0],i[8][0])
    return s
def get_most_exp(*money):
    s=(0,0)
    money=(0,)+money
    for i in schussart:
        if "::" in i[8][1] or money[-1]!=0 and i[8][0]>money[-1]:continue
        if i[8][0]>s[1]:s=(i[0],i[8][0])
    return s
def max_relief(x1,x2):
    h=relief[x1:x2]
    m=[min(i)]
    for i in range(len(h)):
        if h[i]>m:
            m=i
    return m
def calc_parabel(p1,p2,p3):pass
    ### 
def int_to_string(k):
	string=""
	while k!=0:
		string+=chr(k%256)
		k/=256
	return string
def string_to_int(string):
	k=0L
	for i in range(len(string)):
		k+=256**i*ord(string[i])
	return k
def loadcmap(pfad):
    global relief,g,mapartc,reliefaendernr
    try:(width2,height2,relief2,g2)=(eval(file(pfad,"r").read()))
    except:
        try:(width2,height2,relief2,g2,ex2)=(eval(file(pfad,"r").read()))
        except:
            tkMessageBox.showerror(title="ERROR",message="Die Karte konnte nicht geladen werden",parent=root)
            return
        ex=eval(hsdfhsddecrypt(ex2[0],(100,2322,33,4,544,20,7,348,9333)))
        for i in ex:
            exec (i)
    if g2!=g:default.append("global g;g="+str(g))
    g=g2
    relief=[]
    if type(relief2)==type(""):relief2=string_list(relief2,(chr(26),))
    for i in range(width+1):
        relief.append(relief2[i%width2])
    reliefaendernr=1
def maplistact(*k):
    global mapartc
    for k in ["Standard - ","Eigene - "]:
        for i in mapartc:
            if k == i[:len(k)]:maplist.insert(END,i)
def get_cmaps(*k):
    import os
    try:
        i=os.listdir("maps")
    except:return "Error: kein Automapladen"
    k=[]
    for i in i[:]:
        if i[-5:]==".cmap":k.append(i)
    return k
def autoloadcmap(*k):
    global mapartc
    i=get_cmaps(k)
    if i=="Error: kein Automapladen":return
    for i in i[:]:
        mapartc.update({("Eigene - "+i[:-5]):(r"maps//"+i)})
def find(l,s):
    d=()
    for i in range(len(l)):
        if l[i] is s:
            d+=(i,)
    return d
def get_platz():
    global listenvar,spanz
    l=[]
    for i in range(spanz):
        s=0
        for k in listenvar:
            if k in ("spargeld","runden"):continue
            if max(listenvar[k])==0:continue
            s+=float(listenvar[k][i])/max(listenvar[k])
        l.append(s)
    k=[0]*spanz
    for s in range(spanz):
        for i in range(spanz):
            if l[i]==max(l):
                k[i]=s+1
                l[i]=min(l)-1
                break
    return k
def wertungsframefunk(*k):
    wertungsframeact()
    wertungsframe.grid(row=1,column=1)
def wertungsframefunk2(*k):
    wertungsframe.grid_forget()
    los(1)
def wertungsframeact():
    global listenvar,farben
    c=9
    plazierung=get_platz()
    for i in range(spanz+2):
        if i==0:
            text=u"Spieler".center(c)
            text+=u"Geld".center(c)
            text+=u"Siege".center(c)
            text+=u"Sch\u00fcsse".center(c)
            text+=u"Schaden".center(c)
            text+=u"Besiegte".center(c)
            text+=u"Treffer".center(c)
            text+=u"Platz".center(c)
            fill="black"
        elif i==spanz+1:
            text=">>Zum Spiel<<"
            fill="black"
            exec "wertungslabel"+str(i)+".bind('<1>',wertungsframefunk2)"
        else:
            n=find(plazierung,i)
##            if len(n)!=1:print n
            n=n[0]
            text=("Spieler"+str(n+1)).center(c)
            text+=str(listenvar["geld"][n]).center(c)
            text+=str(listenvar["siege"][n]).center(c)
            text+=str(listenvar["schussanz"][n]).center(c)
            text+=str(listenvar["schaden"][n]).center(c)
            text+=str(listenvar["besiegte"][n]).center(c)
            text+=str(listenvar["treffer"][n]).center(c)
            text+=str(plazierung[n]).center(c)
            fill=farben[n]
        exec "wertungslabel"+str(i)+".grid(row=i,column=0)\nwertungslabel"+str(i)+".config(text=text,foreground=fill)"
def add_player():
    global spanz
    if spanz>=maxspieleranz:return
    spanz+=1
def shotabotest(k,n):
    global bupos
    return bupos[k][6]/2**n%2
def zufallsschuss():
    global schussart
    c=[]
    for i in schussart[:]:
        if not "::" in i[8][1]:
            c.append(i[0])
    return c[int(random.random()*len(c))]
def set_fi(nr):
    global fi
    fi[1]=nr
def fallschirm_test(*k):
    global shot,fallschirmvar
    if not fi[1]:return
    if fi[0]+fi[1]<time.time():
        if  fi[0]!=0:
            global width
            create_fallschirm_at(int(random.random()*(width-6)+3),(zufallsschuss(),int(10-sqrt((random.random()*100)))+1),25)
        fi[0]=time.time()
    dels={}
    dels2={}
    for i in range(len(fallschirmvar[:])):
        fallschirmvar[i][3][1]+=fallschirmvar[i][5]
        coords_fallschirm(fallschirmvar[i][3][0],fallschirmvar[i][3][1],fallschirmvar[i][0],fallschirmvar[i][2])
        for fff in range(len(shot)):
            if abs(shot[fff][5][1]-fallschirmvar[i][3][1])<fallschirmvar[i][2]/2 and abs(shot[fff][5][0]-fallschirmvar[i][3][0])<fallschirmvar[i][2]/2 and schussart[shot[fff][6]][6][1]!=0:
                bupos[shot[fff][8]][4][fallschirmvar[i][1][0]]+=fallschirmvar[i][1][1]
                if bupos[shot[fff][8]][4][fallschirmvar[i][1][0]]>10:bupos[shot[fff][8]][4][fallschirmvar[i][1][0]]=10
                dels[str(fallschirmvar[i])]=1
                dels2[str(shot[fff])]=1
        if relief[int(fallschirmvar[i][3][0])]<fallschirmvar[i][3][1]:
            dels[str(fallschirmvar[i])]=1
    for k in dels:delete_fallschirm(k)
    for k in dels2:delshot(k)
def schusslistact(*k):
    schusslist.delete(0,END)
    for i in schussart:
        if "::" in i[8][1]:continue
        o=str(i[0])
        o=o.center(4)
        schusslist.insert(END,o+" "+i[8][1])
def delete_fallschirm(k):
    global fallschirmvar
    k=eval(k)
    canvas_delete(k[0]-1)
    canvas_delete(k[0])
    fallschirmvar.remove(k)
def create_fallschirm_at(x,ladung,gr,*y):
    global schussart,fallschirmvar
    musik_sound(2)
    if y==():
        y=(0,)
    y=y[0]
    canvas_create_arc(x-gr,y-gr,x+gr,y+gr,extent=90,style="pieslice",start=45,width=3,outline=schussart[ladung[0]][6][2])
    find_all=canvas_create_rectangle(x-gr/2,y,x+gr/2,y+gr/2,fill=schussart[ladung[0]][6][2])
    fallschirmvar.append([find_all,ladung,gr,[x,y],time.time(),1.2])
    #nr,ladung,gr,[pos],zeit,gschw
def coords_fallschirm(x,y,nr,gr):
    canvas_coords(nr-1,x-gr,y-gr,x+gr,y+gr)
    canvas_coords(nr,x-gr/2,y,x+gr/2,y+gr/2)
def create_sun_at(x,y,*gr):
    if gr==():
        gr=(30,)
    gr=gr[0]
    canvas_create_oval(x-gr,y-gr,x+gr,y+gr,width=0,fill="gold")
def create_moon_at(x,y,*gr):
    global hintergrundfarbe
    if gr==():
        gr=(30,)
    gr=gr[0]
    canvas_create_oval(x-gr,y-gr,x+gr,y+gr,width=0,fill="gold")
    canvas_create_oval(x,y-2*gr,x+2*gr,y,width=0,fill=hintergrundfarbe)
def set_schnee(k):
    global schneevar
    if not type(k)==type(1):
        return
    schneevar[1]=k
def schneetest(*k):
    global schneevar
    if schneevar[1]==0:return
    if schneevar[0]<time.time()-1.0/schneevar[1]:
        schnee()
        schneevar[0]=time.time()
def schnee(*k):
    global relief,schneevar
    relief[int(random.random()*width)]-=schneevar[2]
def button1_klick(*k):
    if sound==0:return
    try:
        winsound.PlaySound("sound\\button1.wav",(8192L+131072L+1L+2))
    except:pass
def button3_klick(*k):
    if sound==0:return
    try:
        winsound.PlaySound("sound\\button2.wav",(8192L+131072L+1L+2))
    except:pass
def exblow_sound(*k):
    if sound==0:return
    if k==():
        k=(int(5*random.random())+1,)
    for i in k:
        try:
            winsound.PlaySound("sound\\exblow"+str(i)+".wav",(8192L+131072L+1L+2))
        except:pass
def aufschlag_sound(*k):
    if sound==0:return
    if k==():
        k=(int(5*random.random())+1,)
    for i in k:
        try:
            winsound.PlaySound("sound\\aufschlag"+str(i)+".wav",(8192L+131072L+1L+2))
        except:pass
def schutzsch_sound(*k):
    if sound==0:return
    try:
        winsound.PlaySound("sound\\schutzschild.wav",(8192L+131072L+1L+2))
    except:pass
def gift_sound(*k):
    if sound==0:return
    if k==():
        k=(int(2*random.random())+1,)
    for i in k:
        try:
            winsound.PlaySound("sound\\gift"+str(i)+".wav",(8192L+131072L+1L+2))
        except:pass
def beam_sound(*k):
    if sound==0:return
    if k==():
        k=(int(1*random.random())+1,)
    for i in k:
        try:
            winsound.PlaySound("sound\\beam"+str(i)+".wav",(8192L+131072L+1L+2))
        except:pass
def zischen_sound(*k):
    if sound==0:return
    if k==():
        k=(int(3*random.random())+1,)
    for i in k:
        try:
            winsound.PlaySound("sound\\zischen"+str(i)+".wav",(8192L+131072L+1L+2))
        except:pass
def water_sound(*k):
    if sound==0:return
    if k==():
        k=(int(1*random.random())+1,)
    for i in k:
        try:
            winsound.PlaySound("sound\\water"+str(i)+".wav",(8192L+131072L+1L+2+2+2))
        except:pass
def quitsch_sound(*k):
    if sound==0:return
    if k==():
        k=(int(7*random.random())+1,)
    for i in k:
        try:
            winsound.PlaySound("sound\\quitsch"+str(i)+".wav",(8192L+131072L+1L+2+2))
        except:pass
def musik_sound(*k):
    if sound==0:return
    if k==():
        k=(int(5*random.random())+1,)
    for i in k:
        try:
            winsound.PlaySound("sound\\musik"+str(i)+".wav",(8192L+131072L+1L+2+2))
        except:pass
def heilung_sound(*k):
    if sound==0:return
    try:
        winsound.PlaySound("sound\\heilung.wav",(8192L+131072L+1L+2))
    except:pass
def bell_sound(*k):
    if sound==0:return
    try:
        winsound.PlaySound("sound\\bell.wav",(8192L+131072L+1L+2))
    except:pass
def hsdfhsdencrypt(bb,aa):
    i=0
    text=""
    while i<len(bb):
        kk=0
        for n in range(8):
            kk=ord(bb[(aa[n%len(aa)]+i)%len(bb)])/2**((aa[9%len(aa)]+n)%8)%2*(2**((aa[9%len(aa)]+n)%8))+kk
        i=i+1
        text+=chr(kk)
    return text
def hsdfhsddecrypt(bb,aa):
    i=0
    text=""
    while i<len(bb):
        kk=0
        for n in range(8):
            kk=ord(bb[(-aa[n%len(aa)]+i)%len(bb)])/2**((aa[9%len(aa)]+n)%8)%2*(2**((aa[9%len(aa)]+n)%8))+kk
        i=i+1
        text+=chr(kk)
    return text
def tastenwechsel(*K):
    global t,t2,maxspieleranz
    if t[-1]==1:
        t=t2[:]
    else:
        t=t1[:]
    for i in range(1,7):
        exec("listbox"+str(i)+'.delete(0,END)')
    maxspieleranz=len(t)
    for i in range(1,maxspieleranz):
        for j in t[i-1]:#2-links#3-rechts#5-shot#7-hoch  ,  11-runter
            txt=str(j)
            txt=txt+(7-len(txt))*" "
            txt+="-  "
            txt+=((t[i-1][j]==2)*"links")
            txt+=(t[i-1][j]==3)*"rechts"
            txt+=(t[i-1][j]==5)*"schiessen"
            txt+=(t[i-1][j]==7)*"Schuss wechseln"
            txt+=(t[i-1][j]==11)*"Schuss wechseln"
            exec("listbox"+str(i)+'.insert(0,txt)')
def savegame(*k):
    pfad=tkFileDialog.asksaveasfilename(parent=root,title="Cannon - Speichern",initialfile="Unbenannt.can",filetypes=("Cannongames {can}",))
    if pfad=="":return
    if pfad[-4:]!=".can":pfad+=".can"
    f=file(pfad,"w")
    f.write(str([hsdfhsdencrypt(str((listenvar,bupos,mapart,height,width,relief,g,spanz,reliefg,t,schussart,schussart2,suddendeath,time.time()-gametime)),(100,2322,33,4,544,6,7,348,9333))]))
    f.close()
def loadgame(*k):
    global mapart,height,width,relief,g,spanz,reliefg,t,schussart,schussart2,suddendeath,bupos,gametime,listenvar
    global spielersch,optionvar,reliefgnr,move,maxspieleranz,untergrundfarbe,reliefaendernr
    optionvar+="load"
    pfad=tkFileDialog.askopenfilename(parent=root,title="Cannon - Laden",initialfile="Unbenannt.can",filetypes=("Cannongames {can}",))
    if pfad=="":return
    f=file(pfad,"r")
    try:
        (listenvar,bupos,mapart,height,width,relief,g,spanz,reliefg,t,schussart,schussart2,suddendeath,gametime2)=eval(hsdfhsddecrypt(eval(f.read())[0],(100,2322,33,4,544,6,7,348,9333)))
    except:
        tkMessageBox.showerror(title="ERROR",message="Das Spiel konnte nicht geladen werden",parent=root)
        f.close()
        return
    f.close()
    gametime=time.time()-gametime2
    canvas.config(width=width,height=height)
    spielersch=0
    root.wm_geometry("+%s+%s"%(((root.winfo_screenwidth()-width)/2),((root.winfo_screenheight()-height)/2)))
#    root.wm_geometry("+%s+%s"%(10,100))
    oberflaeche()
    for i in range(spanz):
        buposfconf(i)
    relief
    reliefaendernr=1
    los(1)
def exerr(n):
    exec(exeentry.get())
def xyposae(event):
    global xyposaex,xyposaey
    xyposaex=event.x
    xyposaey=event.y
def F12(k):
    if xyposaex==0==xyposaey:
        exeentry.place_forget()
        return
    exeentry.place(x=xyposaex,y=xyposaey)
def Tastaturbelegung(k):
    hauptmenu.grid_forget()
    Ttop.grid(row=1,column=1)
def Tastaturbelegungende(k):
    Ttop.grid_forget()
    hauptmenu.grid(row=1,column=1)
def giftpos():
    global reliefg,relief,reliefgnr,bupos,giftvar
    for i in range(width,-1,-1):
        if reliefg[i]>0 and -relief[i]+reliefg[i]>-relief[(i+1)%width]+reliefg[(i+1)%width]:
            reliefg[i]-=1
            reliefg[(i+1)%width]+=1
            canvas_coords(reliefgnr+i+1,i,relief[i],i,relief[i]-reliefg[i])
            canvas_coords(reliefgnr+(i+1)%width+1,(i+1)%width,relief[(i+1)%width],(i+1)%width,relief[(i+1)%width]-reliefg[(i+1)%width])
        i=width-i
        if reliefg[i]>0 and -relief[i]+reliefg[i]>-relief[(i-1)%width]+reliefg[(i-1)%width]:
            reliefg[i]-=1
            reliefg[(i-1)%width]+=1
            canvas_coords(reliefgnr+i+1,i,relief[i],i,relief[i]-reliefg[i])
            canvas_coords(reliefgnr+(i-1)%width+1,(i-1)%width,relief[(i-1)%width],(i-1)%width,relief[(i-1)%width]-reliefg[(i-1)%width])
    for k in range(spanz):
        for i in range(bupos[k][0],bupos[k][0]+22):
            i%=width
            if reliefg[i]>1 and (giftvar[0]/2**(k))%2==0 and (bupos[k][1]+29>relief[i]>(bupos[k][1]-11)) and k not in [ee[2] for ee in schutzschild]:
                giftvar[0]+=2**(k)
        if (giftvar[0]/2**(k))%2 and giftvar[k+1]<time.time()-3 and bupos[k][3]>2:
            giftvar[k+1]=time.time()
            bupos[k][3]-=1
            canvas.itemconfigure(width+5+bunkerteilanz*k,fill="green2")
            canvas_coords(width+5+bunkerteilanz*k,bupos[k][0]+5,bupos[k][1]+40-int(bupos[k][3]),bupos[k][0]+5,bupos[k][1]+40)
        elif giftvar[k+1]<time.time()-1.5:canvas.itemconfigure(width+5+bunkerteilanz*k,fill="white"*(k==0 or k==5)+"black"*((k==0 or k==5)^1))
    giftvar[0]=0
def G(n):
    return n
def gift(k,x,y,n):
    global reliefg
    r=eval(k)
    for i in range(int(x-r/2),int(x+r/2)):
        reliefg[int(i%width)]+=int(sqrt(r**2-(i-x)**2))
        canvas_coords(reliefgnr+i%width+1,i%width,relief[i%width],i%width,relief[i%width]-reliefg[i%width])
def Laden(k):
    loadgame()
def T(s):return s
def timer(string,x,y,n,nr):#schussart[i[6]][3],x,y,i[8],i[0]
    global timervar
    zeit=time.time()
#    print (suche(string,"T(",")")[2:-1]),eval(suche(string,"T(",")")[2:-1])
    if not(eval(timervar[str(nr)])<zeit-eval(suche(string,"T(",")")[2:-1])):return
    timervar[str(nr)]=str(zeit)
    if "K(" in string:kasten(suche(string,"K(",")"),x,y,n)#kasten(suche(schussart[i[6]][3],"K(",")"),x,y,i[8])
def suche(string,von,bis):
    for i in range(len(string)-len(von)):
        if string[i:i+len(von)]==von:
            string=string[i:]
            break
    for i in range(len(string)):
        if string[i:i+len(bis)]==bis:
            if not (i==len(string)):
                string=string[0:i+len(bis)]
                break
    return string
def verschwinden(canvasnr):
    try:
        canvas_coords(canvasnr,-20,-20)
    except:
        canvas_coords(canvasnr,-20,-20,-23,-23)
def schusskaufspielerconf(k):
    global kaufspieleract,spielerwechselzeit
    if spielerwechselzeit+1>time.time() and spielerwechselzeit!=0:
        winsound.MessageBeep(0)
        return
    kaufspieleract+=1
    spielerwechselzeit=time.time()
    if kaufspieleract==spanz-1:
        weiterbutton.config(text=">>Zur Wertung>>")
    elif kaufspieleract>=spanz:
        kaufframe.grid_forget()
        spielerwechselzeit=0
        wertungsframefunk(1)
    else:
        weiterbutton.config(text=u">>N\u00e4chster Spieler>>")
    try:
        n=eval(schusslist.get(schusslist.curselection())[:4])
    except:n=0
    spielerlabel.config(text=("Spieler "+str(kaufspieleract+1)))
    zeichenlabel.config(text=eval("u'"+str(bupos[kaufspieleract][4][n])+"'")+u" x  "+\
                        schussart[n][1]+" "+eval("u'"+"\u2714"*shotabotest(kaufspieleract,n)\
                                                 +"'")+" "+abotest(kaufspieleract,n))#4x
    preislabel.config(text=("Preis: "+str(schussart[n][8][0])))
    geldlabel.config(text=("Guthaben: "+str(bupos[kaufspieleract][5])))
def abotest(k,n):
    global bupos
    if bupos[k][7][n]==0:return ""
    else:return eval("u'\u"+str(hex(10121+bupos[k][7][n]))[2:]+"'")
def schussconf(k):
    thread.start_new(schussconf2,(k,0))
def schussconf2(k,o):
    time.sleep(0.1)
    global kaufspieleract,spielernummer
    #zeichenlabelpreislabelgeldlabelkaufbutton
    if len(schusslist.curselection())==0:return
    n=eval(schusslist.get(schusslist.curselection())[:4])
    spielerlabel.config(text=("Spieler "+str(kaufspieleract+1)))
    zeichenlabel.config(text=eval("u'"+str(bupos[kaufspieleract][4][n])+"'")+u" x  "+\
                        schussart[n][1]+" "+eval("u'"+"\u2714"*shotabotest(kaufspieleract,n)\
                                                 +"'")+" "+abotest(kaufspieleract,n))#4x
    preislabel.config(text=("Preis: "+str(schussart[n][8][0])))
    geldlabel.config(text=("Guthaben: "+str(bupos[kaufspieleract][5])))
def kaufenschuss(k):
    global kaufspieleract
    if len(schusslist.curselection())==0:return
    n=eval(schusslist.get(schusslist.curselection())[:4])
    if bupos[kaufspieleract][5]<schussart[n][8][0] or bupos[kaufspieleract][4][n]>9:
        winsound.MessageBeep(0)
        return
    bupos[kaufspieleract][5]-=schussart[n][8][0]
    bupos[kaufspieleract][4][n]+=1
    geldlabel.config(text=("Guthaben: "+str(bupos[kaufspieleract][5])))
    zeichenlabel.config(text=eval("u'"+str(bupos[kaufspieleract][4][n])+"'")+u" x  "+\
                        schussart[n][1]+" "+eval("u'"+"\u2714"*shotabotest(kaufspieleract,n)\
                                                 +"'")+" "+abotest(kaufspieleract,n))#4x
def kaufenabo(k):
    global kaufspieleract
    if len(schusslist.curselection())==0:return
    n=eval(schusslist.get(schusslist.curselection())[:4])
    if bupos[kaufspieleract][5]<schussart[n][8][0]*20 or bupos[kaufspieleract][7][n]>9:
        winsound.MessageBeep(0)
        return
    bupos[kaufspieleract][5]-=schussart[n][8][0]*20
    bupos[kaufspieleract][7][n]+=1
    geldlabel.config(text=("Guthaben: "+str(bupos[kaufspieleract][5])))
    zeichenlabel.config(text=eval("u'"+str(bupos[kaufspieleract][4][n])+"'")+u" x  "+\
                        schussart[n][1]+" "+eval("u'"+"\u2714"*shotabotest(kaufspieleract,n)\
                                                 +"'")+" "+abotest(kaufspieleract,n))#4x
def kaufen(k,o):
    try:
        exec(k+".grid_forget()")
    except:pass
    kaufframe.grid(row=1,column=2)
    global kaufspieleract
    kaufspieleract=-1
    schusslistact()
    schusskaufspielerconf(k)
def aboaddshot():
    global bupos,shot,spanz
    for i in range(spanz):
        for j in range(len(schussart)):
            bupos[i][4][j]+=bupos[i][7][j]#x,y,winkel,leben,schussanz,geld,unendlich,ABO
            if bupos[i][4][j]>10:
                bupos[i][4][j]=10
def Hilfe(k):
    hilfetop=Toplevel(root)
    hilfetop.title("Cannon - Hilfe")
    hilfetop.iconbitmap("info")
    try:
        f=file("Cannon - Hilfe.txt","r")
        hilfetext=f.read()
        f.close()
    except:
        hilfetext="Keine Hilfe Moeglich"
    label=Label(hilfetop,text=hilfetext,justify="left")
    label.pack()
def Hauptmenu(k):
    top.place(relx=0.5,rely=0.5,anchor="center")
    hauptmenu.grid(row=1,column=0)
def multiplayer(k):
    hauptmenu.grid_forget()
    spieleranzahlframef(k)
def Editor(k):
    import os
    os.startfile("cannon_Mapeditor.pyw")
def schutzschposconf():
    global schutzschild,bupos
    for i in schutzschild[:]:
        k=i[2]
        canvas_coords(i[3],bupos[k][0]-6,bupos[k][1]-6,bupos[k][0]+28,bupos[k][1]+28)
def schutzsch():
    global schutzschild,bupos
    for i in schutzschild[:]:
        if time.time()-25>i[0]:
            schutzschild.remove(i)
            canvas_delete(i[3])
def schutz(k):
    global schutzschild
    find_all=canvas_create_arc(bupos[k][0]-6,bupos[k][1]-6,bupos[k][0]+28,bupos[k][1]+28,extent=180,width=3,style=ARC,outline="white")#bogen
    schutzschild.append([time.time(),int(bupos[k][3]),k,find_all])
def kastensch(i,x,y,n,g,ca,kw):
    time.sleep(g/5.0)
    shot.append([ca,kw["winkel"][g%len(kw["winkel"])],100,[x,y],time.time(),[0,0],i,-1,n])
    #canvasnr,winkel,geschw,punkt,zeit,aktuelle pos,art,spielernummer,spielernummerfuergeld
def kasten(k,x,y,n,**kw):
    global shot
    d=eval(k[1:])
    i={"winkel":[int(random.random()*360) for i in range(len(d))]}
    i.update(kw)
    kw=i
    g=0
    for i in d:
        while 1:
            try:
                exec("find_all=canvas.create_"+schussart2[schussart[i][6][0]][0]+"""(
                        int(x+schussart[i][6][1]/2),
                        int(y+schussart[i][6][1]/2),
                        int(x-schussart[i][6][1]/2),
                        int(y-schussart[i][6][1]/2),
                        fill=schussart[i][6][2],
                        width=((i=="Linie")*schussart[i][6][1]/4+1))""")
                break
            except:pass
        thread.start_new(kastensch,(i,x,y,n,g,find_all,kw))
        g+=1
def gewonnen():
    global ende,bupos,spanz,gametime,fi,listenvar,default,g,defaultround
    top.place(relx=0.5,rely=0.5,anchor="center")
    gewonnenlabel.grid(row=1,column=3)
    fi[0]=0
    listenvar["runden"]+=1
    for i in default:
        exec i
##        print i,"\n"
    default=[]
    defaultround=[]
    for i in fallschirmvar:
       delete_fallschirm(str(i))
    if sound:
        winsound.PlaySound("sound\\tada.wav",(8192L+131072L+1+2))
    for k in range(spanz):
        if bupos[k][3]>0:
            bupos[k][5]+=abs(int(gametime-time.time()))*2+400
            listenvar["siege"][k]+=1
        listenvar["geld"][k]+=bupos[k][5]-listenvar["spargeld"][k]
    gewonnenlabel.grid_forget()
    aboaddshot()
    frametop.grid(row=1,column=1)
    schusskaufspielerconf(1)
    ende="gewonnen"
def exblow2(r,b):
    for i in range(int(r/3)+1):
        canvas_delete(b-i)
        time.sleep(0.2)
def exblow(x,y,r):
    ecol=["red2","orange","yellow2","#e41","#f53"]
    for i in range(0,int(r),3):
        zx=int(random.random()*(r-i)-(r-i)/2)
        zy=int(random.random()*(r-i)-(r-i)/2)
        find_all=canvas_create_oval(int(x-zx+i),int(y-zy+i),int(x-i-zx),int(y-i-zy),fill=ecol[int(random.random()*len(ecol))],width=0)
    thread.start_new(exblow2,(r,find_all))
def sig(m):
    if m==0:
        return 0
    return m/abs(m)
def delbunker(k):
    global t,bunkerteilanz,bupos,listenvar,gametime
    t[k]={}
    move[k][0]=1
    for i in range(bunkerteilanz):
        verschwinden(width+i+2+bunkerteilanz*k)
    exblow(bupos[k][0]+5,bupos[k][1],12)
    time.sleep(0.001)
    exblow(bupos[k][0]+5,bupos[k][1]+10,12)
    z=0
    bupos[k][5]+=abs(int(gametime-time.time()))*2
#    print abs(int(gametime-time.time()))
    for i in range(spanz):
        if t[i]=={}:
            z+=1
    if z==spanz-1:
        gewonnen()
def ss2(k):
    if k>height-40:
        return height-40
    else:return k
def delshot(k):
    global shot,spielersch
    k=eval(k)
    if not "E" in schussart[k[6]][3]:
        if "G(" in schussart[k[6]][3]:gift_sound()
        else:aufschlag_sound()
    canvas_delete(k[0])
    shot.remove(k)
    if (spielersch/2**(k[7]+1))%2>0:
        canvas_dchars(width+6+bunkerteilanz*k[7],0,END)
        spielersch-=2**(k[7]+1)
def fliegen():
    global shot,g,width,height,bupos,dels,farben,schussart,reliefg,bunkernr,reliefaendernr
    dels={}
    for zz in range(len(shot)):
        if str(shot[zz]) in dels:continue
        i=shot[zz]
        dels2=0
        zeit=time.time()-i[4]
        gvalue=1
        if "g(" in schussart[i[6]][3]:
            gvalue=eval(suche(schussart[i[6]][3],"g(",")")[1:]) #n fache Gravitation
            if zeit>gvalue[1]:dels2=1
            gvalue=gvalue[0]
        x=-i[2]*cos(pi*(90-i[1])/180)*zeit+i[3][0]
        y=-i[2]*sin(pi*(90-i[1])/180)*zeit+gvalue*250/g*zeit**2+i[3][1]
        x%=width
        if y>height-3:
            y=height-5
        if "nc" in schussart[i[6]][3]:pass
        elif schussart[i[6]][6][0] in ("Ball","Rechteck","Luftschiff","Schrot"):canvas_coords(i[0],x+schussart[i[6]][6][1]/2,y+schussart[i[6]][6][1]/2,x-schussart[i[6]][6][1]/2,y-schussart[i[6]][6][1]/2)
        elif schussart[i[6]][6][0] in ("Linie",):
            a2=shot[zz][5][0]-x
            b2=shot[zz][5][1]-y
            gr=schussart[i[6]][6][1]
            try:
                n=gr/sqrt(a2**2+b2**2)
            except:n=0
            canvas_coords(i[0],x+a2*n,y+b2*n,x,y)
        elif schussart[i[6]][6][0] in ("Dreieck",):
            a2=-shot[zz][5][0]+x
            b2=-shot[zz][5][1]+y
            gr=schussart[i[6]][6][1]
            try:
                n2=gr/sqrt(a2**2+b2**2)
            except:n2=0
            a3=-b2/3
            b3=a2/3
            canvas_coords(i[0],x+a2*n2,y+b2*n2,x-a3*n2,y-b3*n2,x+a3*n2,y+b3*n2)
        elif schussart[i[6]][6][0] in ("Stern",):
            sternr=schussart[i[6]][6][1]
            if not "st(" in schussart[i[6]][3]:sternn=(4,1)
            else:sternn=eval(suche(schussart[i[6]][3],"st(",")")[2:])
            sternstring=""
            sternzeit=time.time()
            for sterni in range(sternn[0]):
                sternw=360/sternn[0]*sterni+(zeit)*360*sternn[1]
                sternstring+=","+str(x+sin(pi*sternw/180)*sternr)+","+str(y+cos(pi*sternw/180)*sternr)
                sternstring+=","+str(x+sin(pi*(sternw+180/sternn[0])/180)*sternr*0.618)+","+str(y+cos(pi*(sternw+180/sternn[0])/180)*sternr*0.618)
            exec("canvas_coords(i[0]"+sternstring+")")
        elif schussart[i[6]][6][0] in ("Rakete",):
            a2=-shot[zz][5][0]+x
            b2=-shot[zz][5][1]+y
            gr=schussart[i[6]][6][1]
            try:
                n2=gr/sqrt(a2**2+b2**2)
            except:n2=0
            a3=-b2/3
            b3=a2/3
            try:
                n3=gr*2.0/3/sqrt(a2**2+b2**2)
            except:n3=0
            n4=n3/2
            canvas_coords(i[0],x+a2*n2,y+b2*n2,\
                          x-a3*n3+a2*n3,y-b3*n3+b2*n3,\
                          x-a3*n4+a2*n4,y-b3*n4+b2*n4,\
                          x-a3*n2,y-b3*n2,\
                          x+a3*n2,y+b3*n2,\
                          x+a3*n4+a2*n4,y+b3*n4+b2*n4,\
                          x+a3*n3+a2*n3,y+b3*n3+b2*n3)
        shot[zz][5]=[x,y,shot[zz][5][0],shot[zz][5][1]]
        if relief[int(x)]<y or y>height-22:
            dels2=1
            bupos[i[8]][5]+=schussart[i[6]][8][0]/10#geld
            if "E" in schussart[i[6]][3]:
                exblow(x,y,schussart[i[6]][2])
                if not "BB" in schussart[i[6]][3]:
                    exblow_sound()
            if "K(" in schussart[i[6]][3]: kasten(suche(schussart[i[6]][3],"K(",")"),x,y,i[8])
            if "G(" in schussart[i[6]][3]:gift(suche(schussart[i[6]][3],"G(",")"),x,y,i[8])
            if "BB" in schussart[i[6]][3]:
                (bupos[i[8]][0],bupos[i[8]][1])=(int(x-11),(int(y)-11))
                beam_sound()
                buposfconf(i[8])
            for z in range(-schussart[i[6]][2],schussart[i[6]][2]+1):
                try:
                    m=schussart[i[6]][5]*sqrt(schussart[i[6]][2]**2-z**2)
                    if relief[int(x)+z]-reliefg[int(x)+z]>y+m and schussart[i[6]][5]>0:continue#drueber
                    elif relief[int(x)+z]<y-m or schussart[i[6]][5]<0:#drunter
                        relief[int(x)+z]+=2*m
                    else:#drin
                        relief[int(x)+z]=y+m
                        if reliefg[int(x)+z]>0 and schussart[i[6]][5]>0:
                            if reliefg[int(x)+z]<m:#drin
                                reliefg[int(x)+z]=0
                            else:reliefg[int(x)+z]-=m#druber
                            canvas_coords(reliefgnr+int(x)+z+1,int(x)+z,relief[int(x)+z],int(x)+z,relief[int(x)+z]-reliefg[int(x)+z])
                    reliefaendernr=1
                except: pass
            for k in range(len(bupos)):
                if abs(x-bupos[k][0]-11)<11+schussart[i[6]][2] and abs(y-bupos[k][1]-14.5)<15+schussart[i[6]][2] and int(bupos[k][3])>=0:
                    if k not in [ee[2] for ee in schutzschild]:
                        bupos[i[8]][5]+=30
                        bupos[k][3]-=schussart[i[6]][4]#schaden
                        listenvar["schaden"][i[8]]+=schussart[i[6]][4]
                        listenvar["treffer"][i[8]]+=1
                        if int(bupos[k][3])<0:
                            bupos[i[8]][5]+=250
                            listenvar["besiegte"][i[8]]+=1
                            delbunker(k)
                        else:
                            if int(bupos[k][3])>29:bupos[k][3]=29
                            canvas_coords(bunkernr+5+bunkerteilanz*k,bupos[k][0]+5,bupos[k][1]+40-int(bupos[k][3]),bupos[k][0]+5,bupos[k][1]+40)
                    dels2=1
        elif "T(" in schussart[i[6]][3]:
            timer(schussart[i[6]][3],x,y,i[8],i[0])
        elif "D(" in schussart[i[6]][3] and eval(suche(schussart[i[6]][3],"D(",")")[1:])<zeit:
            dels2=1
            if "E" in schussart[i[6]][3]: exblow(x,y,schussart[i[6]][2])
            if "K(" in schussart[i[6]][3]: kasten(suche(schussart[i[6]][3],"K(",")"),x,y,i[8])
        for fff in range(len(shot)):
            if abs(shot[fff][5][1]-shot[zz][5][1])<schussart[i[6]][6][1]/2 and abs(shot[fff][5][0]-shot[zz][5][0])<schussart[i[6]][6][1]/2 and fff!=zz and schussart[shot[fff][6]][6][1]!=0:
                dels2=1
                dels[str(shot[fff])]=1
        if dels2==1:dels[str(i)]=1
    for k in dels:delshot(k)
def schuss(k,*eee):
    global bupos,move,shot,farben,height,spielersch,bunkernr
    if int(bupos[k][3])<0:return
    y=bupos[k][1]+11-cos(pi*bupos[k][2]/180)*22
    x=bupos[k][0]+11-22*sin(pi*bupos[k][2]/180)
    sch=0
    switch=-1
#    if 1:
    try:
        for i in range(len(schussart2[schussart[move[k][3]][6][0]])):
            i2=schussart2[schussart[move[k][3]][6][0]][i]
#            print 
            find_all=create_dict[i2][1](x+schussart[move[k][3]][6][1]/2,\
            y+schussart[move[k][3]][6][1]/2,\
            x-schussart[move[k][3]][6][1]/2,\
            y-schussart[move[k][3]][6][1]/2,\
            fill=schussart[move[k][3]][6][2],\
            width=(schussart[move[k][3]][6][0]=="Linie")*schussart[move[k][3]][6][1]/4+1)
            shot.append([find_all,bupos[k][2]-3*i+6*sig(i),(time.time()-move[k][1])*ladekraft,[x,y],time.time()-0.1*i,[0,0],move[k][3],k,k])
            listenvar["schussanz"][k]+=1#canvasnr,winkel,geschw,punkt,zeit,aktuelle pos,art,spielernummer,spielernummerfuergeld
            if "T(" in schussart[move[k][3]][3]:
                timervar[str(find_all)]=str(time.time())
        if schussart[move[k][3]][6][0] is "Rakete":
            zischen_sound()
        spielersch+=2**(k+1)
    except:
        if "H" in schussart[move[k][3]][3]:
            heilung_sound()
            bupos[k][3]=29
            canvas_coords(bunkernr+5+bunkerteilanz*k,bupos[k][0]+5,bupos[k][1]+40-int(bupos[k][3]),bupos[k][0]+5,bupos[k][1]+40)
            switch=0
        elif "S" in schussart[move[k][3]][3]:
            schutzsch_sound()
            schutz(k)
            switch=0
    bupos[k][4][move[k][3]]-=1*(1^shotabotest(k,move[k][3]))
    if bupos[k][4][move[k][3]]<=0 or switch==0:
        move[k][3]=0
        canvas_dchars(width+7+bunkerteilanz*k,0,END)
        canvas_insert(width+7+bunkerteilanz*k,0,schussart[move[k][3]][1])
    canvas_dchars(width+8+bunkerteilanz*k,0,END)
    canvas_insert(width+8+bunkerteilanz*k,0,":"*(bupos[k][4][move[k][3]]/2)+"."*(bupos[k][4][move[k][3]]%2))            
    if move[k][0]==0: move[k][0]=1
def ss(k):
    global minwinkel,maxwinkel
    if abs(minwinkel-maxwinkel)>=360:pass
    elif k<minwinkel:
        return minwinkel
    elif k>maxwinkel:
        return maxwinkel
    return k
def winkel(w):
    global move,spanz,spielersch
    for k in range(spanz):
        if bupos[k][3]<0:continue
        elif move[k][0]%2==0:
            bupos[k][2]=ss(bupos[k][2]+3)
            canvas_coords(bunkernr+4+bunkerteilanz*k,bupos[k][0]+11,bupos[k][1]+11,bupos[k][0]+11-22*sin(pi*bupos[k][2]/180),\
                          bupos[k][1]+11-cos(pi*bupos[k][2]/180)*22)
        elif move[k][0]%3==0:
            bupos[k][2]=ss(bupos[k][2]-3)
            canvas_coords(bunkernr+4+bunkerteilanz*k,bupos[k][0]+11,bupos[k][1]+11,bupos[k][0]+11-22*sin(pi*bupos[k][2]/180),\
                          bupos[k][1]+11-cos(pi*bupos[k][2]/180)*22)
        if move[k][0]%5!=0 and move[k][2]!=move[k][1]:
            schuss(k)#
            move[k][2]=0
            move[k][1]=0.0
        elif move[k][0]%5==0 and move[k][1]==0 and (spielersch/2**(k+1))%2==0:#aufladen
            move[k][1]=time.time()
        elif move[k][1]!=0 and move[k][2]==0:#ladevorgang
            canvas_dchars(width+6+bunkerteilanz*k,0,END)
            canvas_insert(width+6+bunkerteilanz*k,0,str(int((time.time()-move[k][1])*ladekraft/4)))
            if -(move[k][1]-time.time())>4:
                schuss(k)
                canvas_dchars(width+6+bunkerteilanz*k,0,END)
                canvas_insert(width+6+bunkerteilanz*k,0,str(ladekraft-1))
                move[k][2]=0
                move[k][1]=0.0
        elif move[k][0]%7==0:
            while 1:
                move[k][3]=(move[k][3]+1)%len(bupos[k][4])
                if bupos[k][4][move[k][3]]>0:break
            canvas_dchars(width+7+bunkerteilanz*k,0,END)
            canvas_insert(width+7+bunkerteilanz*k,0,schussart[move[k][3]][1])
            canvas_dchars(width+8+bunkerteilanz*k,0,END)
            canvas_insert(width+8+bunkerteilanz*k,0,":"*(bupos[k][4][move[k][3]]/2)+"."*(bupos[k][4][move[k][3]]%2))            
        elif move[k][0]%11==0:
            while 1:
                move[k][3]=(move[k][3]-1)%len(bupos[k][4])
                if bupos[k][4][move[k][3]]>0:break
            canvas_dchars(width+7+bunkerteilanz*k,0,END)
            canvas_insert(width+7+bunkerteilanz*k,0,schussart[move[k][3]][1])
            canvas_dchars(width+8+bunkerteilanz*k,0,END)
            canvas_insert(width+8+bunkerteilanz*k,0,":"*(bupos[k][4][move[k][3]]/2)+"."*(bupos[k][4][move[k][3]]%2))            
def kfunkr(event):
    global move,spanz,t
    for i in range(spanz):
        if event.keysym in t[i]:
            move[i][0]/=t[i][event.keysym]
def kfunkp(event):
    global move,spanz,t
    for i in range(spanz):
        if event.keysym in t[i] and move[i][0]%t[i][event.keysym]!=0:
            move[i][0]*=t[i][event.keysym]
def buposfconf(k):
    if int(bupos[k][3])<0:return
    canvas_coords(bunkernr+2+bunkerteilanz*k,bupos[k][0],bupos[k][1],bupos[k][0]+22,bupos[k][1]+22)
    canvas_coords(bunkernr+3+bunkerteilanz*k,bupos[k][0],bupos[k][1]+11,bupos[k][0]+22,bupos[k][1]+40)
    canvas_coords(bunkernr+4+bunkerteilanz*k,bupos[k][0]+11,bupos[k][1]+11,bupos[k][0]+11-22*sin(pi*bupos[k][2]/180)\
                  ,bupos[k][1]+11-cos(pi*bupos[k][2]/180)*22)
    canvas_coords(bunkernr+5+bunkerteilanz*k,bupos[k][0]+5,bupos[k][1]+40-int(bupos[k][3]),bupos[k][0]+5,bupos[k][1]+40)
    canvas_coords(bunkernr+6+bunkerteilanz*k,bupos[k][0]+15,bupos[k][1]+16)
    canvas_coords(bunkernr+7+bunkerteilanz*k,bupos[k][0]+15,bupos[k][1]+34)
    canvas_coords(bunkernr+8+bunkerteilanz*k,bupos[k][0]+15,bupos[k][1]+25)
    schutzschposconf()
def buposf(k):
    global bupos,relief,bunkerteilanz
    for k in range(spanz):
        if relief[bupos[k][0]+11]>bupos[k][1]+11 or bupos[k][1]>height-40:
            bupos[k][1]=ss2(bupos[k][1]+g/5)
            buposfconf(k)
        if relief[bupos[k][0]+12]>relief[bupos[k][0]+11]+g/5 and relief[bupos[k][0]+11]>=bupos[k][1]:
            bupos[k][0]=(bupos[k][0]+1)%width
            buposfconf(k)
        elif relief[bupos[k][0]+10]>relief[bupos[k][0]+11]+g/5 and relief[bupos[k][0]+11]>=bupos[k][1]:
            bupos[k][0]=(bupos[k][0]-1)%width
            buposfconf(k)
def newbupos(k):
    global spanz,bupos,width
    anz=[]
    anz2=[]
    for i in schussart:
        anz.append(i[7])
        anz2.append(0)
    bupos.append([width/(spanz+1)*(1+k)+15,200,0,29,anz,200,1,anz2]) #x,y,winkel,leben,schussanz,geld,unendlich,ABO
def bunker(k):
    newbupos(k)
    global spanz,farben,farben2,bupos,width
    canvas_create_arc(bupos[k][0],bupos[k][1],bupos[k][0]+22,bupos[k][1]+22,extent=180,fill=farben[k],style=CHORD)#bogen
    canvas_create_rectangle(bupos[k][0],bupos[k][1]+11,bupos[k][0]+22,bupos[k][1]+40,fill=farben2[k])#koerper
    canvas_create_line(bupos[k][0]+11,bupos[k][1]+11,bupos[k][0]+11,bupos[k][1]-11,fill=farben2[k],width=2)#rohr
    canvas_create_line(bupos[k][0]+5,bupos[k][1]+40-int(bupos[k][3]),bupos[k][0]+5,bupos[k][1]+40,width=3,fill="white"*(k==0 or k==5)+"black"*((k==0 or k==5)^1))#leben
    canvas_create_text(bupos[k][0]+14,bupos[k][1]+16,text="",fill="white"*(k==0 or k==5)+"black"*((k==0 or k==5)^1))#ladung
    canvas_create_text(bupos[k][0]+14,bupos[k][1]+34,text="o",fill="white"*(k==0 or k==5)+"black"*((k==0 or k==5)^1),font=("Lucida Console",7,"bold"))#schussart
    canvas_create_text(bupos[k][0]+14,bupos[k][1]+32,text="",fill="white"*(k==0 or k==5)+"black"*((k==0 or k==5)^1))#schussanz    
def oberflaeche(*k):
    global reliefg,reliefgnr,relief,untergrundfarbe,bunkernr,reliefnr
    for i in canvas.find_all():
        canvas_delete(i)
    for i in range(0,width+1):
        relief.append(height-int(random.random()*50))
        canvas_create_line(i,height,i,height-2,fill=untergrundfarbe)
#    canvas.create_polygon(i,height,i,height-2,fill=untergrundfarbe)
    reliefnr=canvas.find_all()[-1]
    bunkernr=reliefnr-1
    for i in range(maxspieleranz):
        bunker(i)
    reliefgnr=canvas.find_all()[-1]
    for i in range(0,width+1):
        reliefg.append(0)
        canvas_create_line(i,height-10,i,height-10,fill="green2")
def entryspanzf(k):                        # # # # # # # # # # # # # # # #
    global spanz,relief,reliefg,reliefgnr,maxspieleranz
    for i in entryspanz.get():
        if i not in [str(m) for m in range(2,maxspieleranz) ] or len(entryspanz.get())>1 or len(entryspanz.get())==0:
            winsound.MessageBeep(0)
            entryspanz.delete(0,END)
            return 
    spanz=eval(entryspanz.get())
    oberflaeche()
    spieleranzahlframe.grid_forget()
    if k!="lan":
        frametop.grid(row=1,column=2)
def los(k):
#    thread.start_new(los2,(1,))
#def los2(*k):
    global kaufspieleract,bupos,t,shot,spielersch,move,reliefg,optionvar,t1,t2,default
##    for i in default:
##        exec i
##    default=[]
    if "load" in optionvar: #ladevorgang
        hauptmenu.grid_forget()
    kaufspieleract=-1
    def los2(i,label):
        if i==4:
            label.grid_forget()
            los3()
            return
        label.config(text=["3","2","1","LOS!"][i])
        i+=1
        root.after(999,los2,i,label)
    def los3():
        global kaufspieleract,bupos,t,shot,spielersch,move,reliefg,optionvar,t1,t2,default
        top.place_forget()
        move=[]
        root.bind_all("<Any-KeyPress>",kfunkp)
        root.bind_all("<Any-KeyRelease>",kfunkr)
        for i in range(maxspieleranz):
            move.append([1,0,0,0])#ereignis,zeit,###,schussart
            k=i
            canvas_dchars(width+6+bunkerteilanz*k,0,END)
            canvas_dchars(width+7+bunkerteilanz*k,0,END)
            canvas_insert(width+7+bunkerteilanz*k,0,schussart[move[k][3]][1])
            canvas_dchars(width+8+bunkerteilanz*k,0,END)
            canvas_insert(width+8+bunkerteilanz*k,0,":"*(bupos[k][4][move[k][3]]/2)+"."*(bupos[k][4][move[k][3]]%2))            
        if "load" in optionvar: #ladevorgang
            for i in range(spanz):
                if bupos[i][3]<0:
                    delbunker(i)
            optionvar=""
            start(1)
            return
        reliefg=[]
        if suddendeath:
            for i in range(width+1):
                reliefg.append(23)
                canvas_coords(reliefgnr+i+1,i,relief[i],i,relief[i]-reliefg[i])
        else:
            for i in range(width+1):
                reliefg.append(0)
                canvas_coords(reliefgnr+i+1,i,relief[i],i,relief[i]-reliefg[i])
        for i in range(spanz):
            bupos[i][3]=29
            bupos[i][2]=0
            bupos[i][1]=height/10*3
            bupos[i][0]=width/(spanz+1)*(1+i)+15
            #x,y,winkel,leben,schussanz,geld
            listenvar["spargeld"][i]=bupos[i][5]
        if t[5]==1:
            t=t1[:]
        else:
            t=t2[:]
        spielersch=0
        for i in shot:
            canvas_delete(i[0])
        shot=[]
        start(k)
    label=Label(top,font=("Arial",20,"bold"),bg="#DDF")
    label.grid(row=1,column=1)
    los2(0,label)
def totalende(k):
    root.destroy()
    root.quit()
def aendernmap(k):
    global ende,mapart,mapartc
    ende="neustart"
    mapart=mapartc[maplist.get(maplist.curselection())]
    kaufen("frametop",0)
def randommap(k):
    global ende,mapart,mapartc
    ende="neustart"
    mapart=mapartc[mapartc.keys()[int(len(mapartc.keys())*random.random())]]
    kaufen("frametop",0)
def loadmap(*k):
    global g,relief,width,height,ende,canvas,mapart
    pfad=tkFileDialog.askopenfilename(parent=root,title="Cannon - Karte laden",initialfile="Unbenannt.cmap",filetypes=("Cannonmaps {cmap}",))
    if pfad=="":return
    loadcmap(pfad)
##    f=file(pfad,"r")
##    try:
##        (width2,height2,relief2,g)=(eval(f.read()))
##    except:
##        tkMessageBox.showerror(title="ERROR",message="Die Karte konnte nicht geladen werden",parent=root)
##        f.close()
##        return
##    f.close()
##    relief=[]
##    for i in range(width+1):
##        relief.append(relief2[i%width2])
##        canvas_coords(i+1,i,height,i,relief[i])
    ende=0
    kaufen("frametop",0)
def spieleranzahlframef(k):
    spieleranzahlframe.grid(row=1,column=1)
    entryspanz.unbind("<KeyPress-Return>")
    entryspanz.bind("<KeyPress-Return>",entryspanzf)
def end(*k):
    global ende
    ende=1
def untergrund(k):
    global width,g,relief,reliefaendernr
    g_5= g/5
    for i in range(width,-1,-1):
        w1= relief[i]-relief[(i+1)%(width)]
        if abs(w1)>g_5:
            relief[i]-=(w1)/(g_5)
            relief[(i+1)%(width)]+=(w1)/(g_5)
            reliefaendernr=1
        i=width-i
        w1= relief[i]-relief[(i-1)%(width)]
        if abs(w1)>g_5:
            relief[i]-=(w1)/(g_5)
            relief[(i-1)%(width)]+=(w1)/(g_5)
            reliefaendernr=1
def start(k,*eee):
#    thread.start_new(start2,(k,eee))
#def start2(k,*eee):
    global ende,relief,width,zeit2,breakvar,gametime,optionvar,defaultround,reliefaendernr,\
           iconifypause
    gametime=time.time()
    for k in range(spanz):
        buposfconf(k)
        canvas_dchars(width+6+bunkerteilanz*k,0,END)
    startschleife(1)
def startschleife(k,*eee):
    global ende,relief,width,zeit2,breakvar,gametime,optionvar,defaultround,reliefaendernr,\
           iconifypause
    if ende==0 or ende=="neustart":
        zeit2=time.time()
        fallschirm_test()
        schneetest()
        untergrund(k)
        if reliefaendernr:
            coordsrelief()
            reliefaendernr=0
        if ende=="neustart":
            try:
                relief2=[]
                for i in range(0,width+1):
                    relief2.append(height-int(random.random()*50)-eval(mapart))
                    relief=relief2[:]
            except:loadcmap(mapart)
            ende=0
        for i in defaultround:
            exec i
        buposf(k)
        winkel(k)
        fliegen()
        schutzsch()
        giftpos()
        while iconifypause:time.sleep(0.5)
        i=1
        if time.time()<zeit2+0.035:
            i=int(1000*(zeit2+0.035-time.time()))
        root.after(i,startschleife,1)
    if ende==1:
        tt=time.time()
        g=tkMessageBox.askquestion(parent=root,title="Beenden",message="Spiel Beenden?")
        if g=="no":
            ende=0
            tt-=time.time()
            global shot,timervar,schutzschild
            for i in range(len(shot)):
                shot[i][4]-=tt
            for i in timervar:
                timervar[i]=str(eval(timervar[i])-tt)
            for i in range(len(schutzschild)):
                schutzschild[i][0]-=tt
            startschleife(1)
        else:
            root.quit()
            root.destroy()
autoloadcmap()#karten laden
root=Tk()
##leader=Tk()
##root=Toplevel(leader)
##leader.iconbitmap("cannon.ico")
##leader.title("Cannon")
##leader.iconname("Cannon")
##root.transient(leader)
#sound
root.bind_all("<1>",button1_klick)
##vollbild
root.overrideredirect(1)
screenheight=height=root.winfo_screenheight()
screenwidth=width=root.winfo_screenwidth()
root.wm_geometry("+%s+%s"%(((root.winfo_screenwidth()-width)/2),((root.winfo_screenheight()-height)/2)))##
##
root.bind_all("<Double-Key-Escape>",totalende)
root.bind_all("<KeyPress-Escape>",end)
root.title("")
root.protocol("WM_DELETE_WINDOW",end)
canvas=Canvas(root,height=height,width=width,bg=hintergrundfarbe,borderwidth=0)
canvas.pack()
##top
top=Frame(root,bg=hintergrundfarbe,relief=RIDGE)
top.place(relx=0.5,rely=0.5,anchor="center")
## map
frametop=Frame(top,bg=hintergrundfarbe)
maplistlabel=Label(frametop,bg=hintergrundfarbe,text=u"W\u00e4hlen sie ihre Map:")
maplistlabel.pack()
frametop2=Frame(frametop,bg=hintergrundfarbe)
frametop2.pack()
scr=Scrollbar(frametop2)
scr.pack(fill=Y,side=RIGHT)
maplist=Listbox(frametop2,width=45,yscrollcommand=scr.set)
maplist.pack(fill=Y,side=LEFT)
maplist.bind("<Double-Button-1>",aendernmap)
scr.config(command=maplist.yview)
randommapbutton=Button(frametop,text="Zufallskarte",width=20)
randommapbutton.bind("<1>",randommap)
randommapbutton.pack()
choosemapbutton=Button(frametop,text="Karte suchen",width=20)
choosemapbutton.bind("<1>",loadmap)
choosemapbutton.pack()
maplistact()
maplist.focus_set()
## spieleranzahl
spieleranzahlframe=Frame(top,bg=hintergrundfarbe)
entryspanz=Entry(spieleranzahlframe)
entryspanz.grid(row=1,column=1)
labelspanz=Label(spieleranzahlframe,text="Anzahl der Spieler:",bg=hintergrundfarbe)
labelspanz.grid(row=0,column=1)
#farbenwahl
farben=("blue1","red","#ffa518","#338533","gold3","black","magenta","cyan","white","green","black")
farben2=("blue2","red2","#ee9408","#559644","gold1","gray33","magenta2","cyan2","gray88","green2")
root.bind_all("<Double-KeyPress-F2>",start)
#menuanfang
hauptmenu=Frame(top,bg=hintergrundfarbe)
menulabel1=Label(hauptmenu,bg=hintergrundfarbe,text="""Cannon\nHauptmenu""",font=("Arial",20,"bold"))
menulabel1.pack()
menubutton1=Button(hauptmenu,text="Mehrspieler",width=30)
menubutton1.pack()
menubutton1.bind("<1>",multiplayer)
menubutton5=Button(hauptmenu,text="Mehrspieler LAN",width=30)
menubutton5.pack()
menubutton5.bind("<1>",mehrspielerlan)
menubutton2=Button(hauptmenu,text="Waffeneditor",width=30)
menubutton2.pack()
menubutton2.bind("<1>",Editor)
menubutton3=Button(hauptmenu,text="Spiel Laden",width=30)
menubutton3.pack()
menubutton3.bind("<1>",Laden)
menubutton3=Button(hauptmenu,text="Tastaturbelegung",width=30)
menubutton3.pack()
menubutton3.bind("<1>",Tastaturbelegung)
menubutton4=Button(hauptmenu,text="Hilfe",width=30)
menubutton4.pack()
menubutton4.bind("<1>",Hilfe)
menubutton4=Button(hauptmenu,text="Beenden (Doppel - ESC)",width=30)
menubutton4.pack()
menubutton4.bind("<1>",totalende)
Hauptmenu(1)
#gewonnen
gewonnenlabel=Label(top,text="!!GEWONNEN!!",bg=hintergrundfarbe,font=("Arial",20,"bold"))
#kaufen
kaufframe=Frame(top,bg=hintergrundfarbe)
    #listkaufframe
listkaufframe=Frame(kaufframe,bg=hintergrundfarbe)
listkaufframe.grid(row=1,column=1,rowspan=9)
scrk=Scrollbar(listkaufframe)
scrk.pack(fill=Y,side=RIGHT)
schusslist=Listbox(listkaufframe,width=45,bg=hintergrundfarbe,relief=RIDGE,yscrollcommand=scrk.set)
schusslist.pack(fill=Y,side=LEFT)
schusslist.bind("<ButtonRelease-1>",schussconf)
scrk.config(command=schusslist.yview)
schusslist.focus_set()
#nummer,zeichen,sprengweite,anmerkung,schaden,sprengtiefe,[art,groesse,farbe],anzahl,[Preis,Kaufmenu]
    #zugehoeriges
spielerlabel=Label(kaufframe,text="Spieler 1",font=("Arial",20,"bold"),width=20,bg=hintergrundfarbe)
spielerlabel.grid(row=1,column=2)
geldlabel=Label(kaufframe,text="",font=("Arial",20,"bold"),width=20,bg=hintergrundfarbe)
geldlabel.grid(row=2,column=2)
zeichenlabel=Label(kaufframe,text="",font=("Arial Unicode",17,"bold"),width=20,bg=hintergrundfarbe)
zeichenlabel.grid(row=3,column=2)
preislabel=Label(kaufframe,text="",font=("Arial",15,"bold"),width=20,bg=hintergrundfarbe)
preislabel.grid(row=4,column=2)
kaufframeforbuttons=Frame(kaufframe,bg=hintergrundfarbe)
kaufbutton=Button(kaufframeforbuttons,text="Kaufen",width=15)
kaufbutton.grid(row=0,column=0)
kaufbutton.bind("<1>",kaufenschuss)
abokaufbutton=Button(kaufframeforbuttons,text="Abo Kaufen",width=15)
abokaufbutton.grid(row=0,column=1)
abokaufbutton.bind("<1>",kaufenabo)
kaufframeforbuttons.grid(row=5,column=2)
weiterbutton=Button(kaufframe,text=u">>N\u00e4chster Spieler>>",width=30)
weiterbutton.grid(row=6,column=2)
weiterbutton.bind("<1>",schusskaufspielerconf)
#tastatubelegung
Ttop=Frame(top,bg=hintergrundfarbe)
label=Label(Ttop,text="Cannon\nTastaturbelegung",font=("Arial",20,"bold"),bg=hintergrundfarbe)
label.grid(row=0,column=1,columnspan=5)
Ttop2=Frame(Ttop,bg=hintergrundfarbe)
Ttop2.grid(row=1,column=2)
for i in range(1,7):
    anz=2
    tframe=Frame(Ttop2,bg=hintergrundfarbe)
    tframe.grid(row=((i-1)/2+1),column=((i-1)%2+1))
    label=Label(tframe,text="Spieler "+str(i),font=("Arial",15,"bold"),bg=hintergrundfarbe)
    label.grid(row=1,column=1)
    exec("listbox"+str(i)+'=Listbox(tframe,font=("Lucida Console",10,"bold"),width=30,height=8)')
    exec("listbox"+str(i)+'.grid(row=2,column=1)')
tastenwechsel()
tbutton=Button(Ttop,text=u"Tastenbelegung \u00e4ndern",width=25)
tbutton.bind("<1>",tastenwechsel)
tbutton.grid(row=10,column=2)
tbutton=Button(Ttop,text="Hauptmenu",width=25)
tbutton.bind("<1>",Tastaturbelegungende)
tbutton.grid(row=11,column=2)
#eigriff
root.bind_all("<KeyPress-F12>",F12)
exeentry=Entry(root,width=50)
exeentry.bind("<KeyPress-Return>",exerr)
root.bind_all("<Control-Button-1>",xyposae)
#save
root.bind_all("<Control-Alt-s>",savegame)
root.bind_all("<Control-Alt-o>",loadgame)
#wertung
wertungsframe=Frame(top,bg=hintergrundfarbe)
for i in range(8):
    exec("wertungslabel"+str(i)+"=Label(wertungsframe,bg=hintergrundfarbe,justify='left',foreground=farben[i%7-1],font=('Lucida Console',12,'bold'))")
#schussladen
try:   
    i=eval(file("schuss.cans","r").read())
    schussart=i
except:
    i=tkMessageBox.askquestion(parent=root,title="ERROR",message=u"Configurierte Sch\u00fcsse konnten nicht geladen werden.\nDer Schussstandard wird \u00fcbernommen.\n Wollen sie die Standardsch\u00fcsse als default einstellen?")
    if i=="yes":
        try:
            f=file("schuss.cans","w").write(str(schussart))
        except:tkMessageBox.showerror(title="ERROR",message="Option nicht durchf\u00fchrbar",parent=root)
schusslistact()
#Einstellungen laden
#if 1:
schneeintervall = 0
fallschirmintervall = 80
try:
    k =("hintergrundfarbe =","suddendeath =","height =","width =","ladekraft =","sound =","schneeintervall =","fallschirmintervall =")
    for i1 in file("cannnon settings.txt","r").readlines():
        for i2 in k:
            if i1[:len(i2)]==i2:
                exec(i1[:i1.find("###")])
except:tkMessageBox.showerror(title="ERROR",message="Benutzerdefinierte Einstellungen konnten nich geladen werden.",parent=root)
schneevar[1]=schneeintervall
fi[1]=fallschirmintervall
try:del i,schneeintervall,fallschirmintervall,screenheight,screenwidth,k,i1,i2
except:pass
#coords,create
coords=canvas.coords#
create_dict={"line":(canvas.create_line,canvas_create_line),"arc":(canvas.create_arc,canvas_create_arc),\
             "rectangle":(canvas.create_rectangle,canvas_create_rectangle),"oval":(canvas.create_oval,canvas_create_oval)\
             ,"polygon":(canvas.create_polygon,canvas_create_polygon),"window":(canvas.create_window,canvas_create_window)\
             ,"text":(canvas.create_text,canvas_create_text)}
#LAN
##hosten/beitreten => spanz => spielerliste => normal map
lanmenuframe=Frame(top,bg=hintergrundfarbe)
label=Label(lanmenuframe,text="Cannon\nMehrspieler LAN (TCP/IP)",bg=hintergrundfarbe,font=("Arial",15,"bold"))
label.pack()
lanhostbutton=Button(lanmenuframe,text="Ein Spiel Hosten",width=25)
lanhostbutton.bind("<1>",lanhosten)
lanhostbutton.pack()
lanclientbutton=Button(lanmenuframe,text="Einem Spiel Beitreten",width=25)
lanclientbutton.bind("<1>",lanbeitreten)
lanclientbutton.pack()
#hosten
    #menu1
hosten1frame=Frame(top,bg=hintergrundfarbe)
hostenaddrlabel=Label(hosten1frame,text="Ihr Nick:",bg=hintergrundfarbe)
hostenaddrlabel.pack()
hostennameentry=Entry(hosten1frame)
hostennameentry.bind("<KeyPress-Return>",hostenmenu2)
hostennameentry.pack()
    #menu2
hosten2frame=Frame(top,bg=hintergrundfarbe)
hostenaddrlabel=Label(hosten2frame,justify="left",bg=hintergrundfarbe)
hostenaddrlabel.pack()
hosten2frame2=Frame(hosten2frame,bg=hintergrundfarbe)
lanspscr=Scrollbar(hosten2frame2)
lanspscr.pack(fill=Y,side=RIGHT)
lansplist=Listbox(hosten2frame2,width=45,yscrollcommand=lanspscr.set)
lansplist.pack(fill=Y,side=LEFT)
lanspscr.config(command=lansplist.yview)
hosten2frame2.pack()
lanstartbutton=Button(hosten2frame,text="LAN starten",width=25)
lanstartbutton.pack()
#beitreten
    #menu1
beitretenframe=Frame(top,bg=hintergrundfarbe)
label=Label(beitretenframe,text="Ihr Nick:",bg=hintergrundfarbe)
label.grid(row=1,column=1)
clientnameentry=Entry(beitretenframe)
clientnameentry.grid(row=1,column=2)
label=Label(beitretenframe,text="Die Host-Ip:",bg=hintergrundfarbe)
label.grid(row=2,column=1)
clientipentry=Entry(beitretenframe)
clientipentry.grid(row=2,column=2)
label=Label(beitretenframe,text="Der Host-Port:",bg=hintergrundfarbe)
label.grid(row=3,column=1)
clientportentry=Entry(beitretenframe)
clientportentry.grid(row=3,column=2)
clientconnectbutton=Button(beitretenframe,text="Beitreten",width=15,command=client1menu)
clientconnectbutton.grid(row=4,column=1,columnspan=2)

#start
x=1
root.mainloop()
if "com" in lanvar:
    c=lanvar["com"]
elif "client" in lanvar:
    c=lanvar["client"]
else:x=0
if x:
    for i in c.get_servers():
        c.disconnect(i)
