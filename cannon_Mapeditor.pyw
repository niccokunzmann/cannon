from Tkinter import *
import tkMessageBox,thread,time,random,tkFileDialog,winsound
sys.path.append(sys.path[0]+"\\modules")
from files import list_string,string_list
name="Unbenannt.cmap"
width=400
height=400
hintergrundfarbe="gray66"
relief=[]
g=10
ende=0
pinselwidth=2
scrollvar=0
ex=[]
buttonpressed=False
schussart=[ [0,"o",5,"",2,1,["Ball",10,"black"],10,[50,"::Standartschuss"]], \
            [1,"*",10,"",0,-2,["Ball",10,"gray66"],4,[16,u"sch\u00fcttet den Berg auf"]], \
            [2,"+",0,"H",0,0,["",0,"red"],0,[200,u"Erste Hilfe P\u00e4ckchen"]],\
            [3,"-",22,"E",1,1,["Linie",15,"green4"],2,[51,"Hohe Sprengkraft"]],\
            [4,"/\\",7,"E",9,1,["Dreieck",15,"red3"],2,[53,"Viel Schaden"]],\
            [5,"R",14,"E",4,1,["Rakete",15,"gray22"],2,[32,"Normale Rakete"]],\
            [6,"#",8,"K(0,0,15,4,5,5)",1,1,["Rechteck",10,"red4"],0,[123,u"P\u00e4ckchen mit Aufschlagz\u00fcnder"]],\
            [7,"S",0,"S",0,0,["",0,"white"],0,[195,"Schutzschild"]],\
            [8,"<>",8,"K(0,8)",1,1,["Rechteck",5,"blue4"],0,[142,u"rekursives P\u00e4ckchen"]],\
            [9,"%",3,"",3,1,["Schrot",3,"green"],0,[46,"einfacher Schrot"]],\
            [10,"!#!",8,"K(0,4,4,10,6)",1,1,["Rechteck",20,"yellow"],0,[507,u"!!Super P\u00e4ckchen rekursiv!!"]],\
            [11,"!%!",6,"E",4,1,["Schrot",4,"magenta"],0,[69,"!!Superschrot!!"]],\
            [12,"!*!",30,"",0,-2,["Ball",20,"gray66"],0,[33,u"verbessert Bergaufsch\u00fctten"]],\
            [13,"!L!",2,"T(2)K(3,3)",4,1,["Linie",23,"green4"],0,[102,u"Flugsprenger"]],\
            [14,"!R!",28,"E",10,1,["Rakete",25,"gray22"],0,[113,"!!Riesenrakete!!"]],\
            [15,"G",1,"G(15)",3,1,["Rakete",10,"green3"],2,[80,"Gift"]],\
            [16,"F",1,"D(2.4)K("+str([18 for n in range(12)])[1:-1]+")",3,1,["Ball",20,"red3"],0,[703,"Feuerwerk"]],\
            [17,"BB",30,"BB,E",0,0.5,["Rechteck",20,"white"],0,[374,"Bunkerbeamer"]],\
            \
            [18,"",5,"D(1.8)K("+str([5 for n in range(10)])[1:-1]+")",1,1,["Dreieck",6,"blue2"],0,[10,"::Feuerwerk2"]],\
            [19,u"\u06de",37,"st(7,0.5)",17,1,["Stern",20,"blue2"],0,[418,"Starattack"]],\
            ]
m=["Zeichen","Sprengweite","Anmerkung","Schaden","Sprengtiefe","Art","Groesse","Farbe","Startzahl","Preis","Kaufmenutext"]
m2=["[1]","[2]","[3]","[4]","[5]","[6][0]","[6][1]","[6][2]","[7]","[8][0]","[8][1]"]
m3=["eval","eval","","eval","eval","","eval","","eval","eval",""]
#nummer,zeichen,sprengweite,anmerkung,schaden,sprengtiefe,[art,groesse,farbe],anzahl,[Preis,Kaufmenu]
def kartebenennen(name):
    maproot.title(name)
def intlist(l):
    d=[]
    for i in l:
        d.append(int(i))
    return d
list_string=intlist
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
def speichernschuss(*k):
    f=file("schuss.cans","w")
    f.write(str(schussart))
    f.close()
def hilfe(*k):
    maphilfetop=Tk()
    maphilfetop.title("Cannon Mapeditor - Hilfe")
    try:
        f=file("Cannon_Mapeditor - Hilfe.txt","r")
        hilfetext=f.read()
        f.close()
    except:hilfetext="Keine Hilfe moeglich"
    label=Label(maphilfetop,text=hilfetext)
    label.config(justify="left")
    label.pack()
def savemap(*k):
    global g,schussart,relief,width,height,ex
    pfad=tkFileDialog.asksaveasfilename(parent=maproot,title="Cannon - Karte speichern",initialfile="Unbenannt.cmap",filetypes=("Cannonmaps {cmap}",),initialdir="\\maps")
    if pfad=="":return
    if pfad[-5:]!=".cmap":
        pfad+=".cmap"
    f=file(pfad,"w")
    if ex==[]:
        f.write(str((width,height,list_string(relief,(chr(26),)),g)))
    else:
        ex2=[]
        ex2.append(hsdfhsdencrypt(str(ex),(100,2322,33,4,544,20,7,348,9333)))
        f.write(str((width,height,relief,g,ex2)))
    f.close()
def loadmap(*k):
    global g,schussart,relief,width,height,ex,name
    pfad=tkFileDialog.askopenfilename(parent=maproot,title="Cannon - Karte laden",initialfile="Unbenannt.cmap",filetypes=("Cannonmaps {cmap}",),initialdir="\\maps")
    if pfad=="":return
#    if 1:
    try:(width2,height2,relief2,g)=(eval(file(pfad,"r").read()))
    except:
        try:(width2,height2,relief2,g,ex2)=(eval(file(pfad,"r").read()))
        except:
            tkMessageBox.showerror(title="ERROR",message="Die Karte konnte nicht geladen werden",parent=maproot)
            return
        ex=hsdfhsddecrypt(ex2[0],(100,2322,33,4,544,20,7,348,9333))
    width=width2
    height=height2
    schconf()
    mapentryb.delete(0,END)
    mapentryh.delete(0,END)
    mapentryb.insert(0,str(width))
    mapentryh.insert(0,str(height))
    cconf()
    bestueken()
    if type(relief2)==type(""):relief2=string_list(relief2,(chr(26),))
    relief=relief2
    for i in range(width+1):
        mapcanvas.coords(i+1,i,height,i,relief[i])
def erssch(*k):
    global m2,m3,m
    l=[0]
    for i in range(len(m)):
        exec("l.append("+m3[i]+"(entry"+m[i]+".get()))")
    schussart.append([len(schussart),eval("u'"+l[1]+"'"),l[2],l[3],l[4],l[5],[l[6],l[7],l[8]],l[9],[l[10],l[11]]])
    schconf()
def erssch2(*k):
    global m2,m3,m
    l=[0]
    n=eval(schusslistmap.get(schusslistmap.curselection())[:4])
    for i in range(len(m)):
        exec("l.append("+m3[i]+"(entry"+m[i]+".get()))")
    schussart[n]=[n,eval("u'"+l[1]+"'"),l[2],l[3],l[4],l[5],[l[6],l[7],l[8]],l[9],[l[10],l[11]]]
    schconf()
def delsch(*k):
    global schussart
    if schusslistmap.curselection()==():return
    n=eval(schusslistmap.get(schusslistmap.curselection())[:4])
    schussart.remove(schussart[n])
    for i in range(len(schussart)):
        schussart[i][0]=i
    schconf()
def schussconf(k):
    thread.start_new(schussconf2,(k,0))
def schussconf2(k,o):
    global m,schussart,m2
    time.sleep(0.1)
    n=eval(schusslistmap.get(schusslistmap.curselection())[:4])
    for i in range(len(m)):
        try:
            if i==0:
                text=str((schussart[n][1],))[1:-2]
            else:text=str(eval("schussart[n]"+m2[i]))
            exec("entry"+m[i]+".delete(0,END)")
            exec("entry"+m[i]+".insert(0,text)")
        except:pass
    zeichenlabel.config(text=(schussart[n][1]))
def schconf(*k):
    global schussart
    schusslistmap.delete(0,END)
    for i in schussart:
        o=str(i[0])
        o=o.center(4)
        schusslistmap.insert(END,o+" "+i[8][1])
def pwidthconf(*k):
    global pinselwidth
    pinselwidth%=15
    pinselwidth+=1
    pinselbutton.config(font=("Lucida Console",pinselwidth*3,"bold"))
def untergrund(k):
    global width,g,relief
    for i in range(width,-1,-1):
        if abs(relief[i]-relief[(i+1)%(width)])>g/5:
            relief[i]-=(relief[i]-relief[(i+1)%(width)])/(g/5)
            relief[(i+1)%(width)]+=(relief[i]-relief[(i+1)%(width)])/(g/5)
            mapcanvas.coords(i+1,i,height,i,relief[i])
            mapcanvas.coords((i+1)%(width)+1,(i+1)%(width),height,(i+1)%(width),relief[(i+1)%(width)])
    for i in range(0,width+1):
        if abs(relief[i]-relief[(i-1)%(width)])>g/5:
            relief[i]-=(relief[i]-relief[(i-1)%(width)])/(g/5)
            relief[(i-1)%(width)]+=(relief[i]-relief[(i-1)%(width)])/(g/5)
            mapcanvas.coords(i+1,i,height,i,relief[i])
            mapcanvas.coords((i-1)%(width)+1,(i-1)%(width),height,(i-1)%(width),relief[(i-1)%(width)])
def start(k,*eee):
    startbutton.unbind("<1>")
    thread.start_new(start2,(k,1))
def start2(k,*eee):
    global ende
    try:
        while ende==0:
            zeit2=time.time()
            try:untergrund(k)
            except:pass
            while time.time()<zeit2+0.025:
                time.sleep(0.003)
            time.sleep(0.003)
    except: winsound.MessageBeep(48)
    startbutton.bind("<1>",start)
def rel(event):
    global pinselwidth,buttonpressed
    buttonpressed=True
    for i in range(-pinselwidth,pinselwidth,1):
        relief[int(mapcanvas.canvasx(event.x)+i)%(width+1)]=mapcanvas.canvasy(event.y)
        mapcanvas.coords(int(mapcanvas.canvasx(event.x)+i)%(width+1)+1,(mapcanvas.canvasx(event.x)+i)%(width+1),height,(mapcanvas.canvasx(event.x)+i)%(width+1),relief[int(mapcanvas.canvasx(event.x)+i)%(width+1)])
def relr(event):
    global buttonpressed
    buttonpressed=False
def relm(event):
    global buttonpressed
    if buttonpressed:
        rel(event)
def bestueken(*k):
    global width,height,hintergrundfarbe,relief,ende
    relief=[]
    mapcanvas.configure(height=height,width=width,scrollregion="0 0 %i %i"%(width,height))
    for i in range(width+1):
        mapcanvas.create_line(i,height,i,height-2,fill=hintergrundfarbe)
        relief.append(height-2)
    ende=0
def end(*k):
    global ende
    ende=1
    time.sleep(0.1)
    maproot.quit()
    maproot.destroy()
def cconf(*k):
    global width,height,mapcanvas,ende,mapcanvasscrollbar
#    if 1:
    try:
        ende=1
        time.sleep(0.1)
        width=eval(mapentryb.get())
        height=eval(mapentryh.get())
        mapcanvas.pack_forget()
        mapcanvasscrollbar.pack_forget()
        del mapcanvas
        del mapcanvasscrollbar
        mapcanvasscrollbar=Scrollbar(maproot,orient="horizontal")
        mapcanvasscrollbar.pack(side=BOTTOM,fill=X)
        mapcanvas=Canvas(maproot,bg="#DDF",width=width,scrollregion="0 0 %i %i"%(width,height),height=height,xscrollcommand=mapcanvasscrollbar.set)
        mapcanvas.pack(side=TOP,fill=X)
        mapcanvasscrollbar.config(command=mapcanvas.xview)
        mapcanvas.bind("<ButtonPress-1>",rel)
        mapcanvas.bind("<ButtonRelease-1>",relr)
        mapcanvas.bind("<Motion>",relm)
        bestueken()
    except:
        tkMessageBox.showerror(title="ERROR",message=u"Ung\u00fcltige Eingabe",parent=maproot)
def nothing(*m):pass
def mapexecfunk(*k):exec mapexeentry.get();return "break"
maproot=Tk()
maproot.title(name)#"Cannon - Mapeditor")
#canvas
mapcanvasscrollbar=Scrollbar(maproot,orient="horizontal")
mapcanvasscrollbar.pack(side=BOTTOM,fill=X)
mapcanvas=Canvas(maproot,bg="#DDF",width=width,scrollregion="0 0 %i %i"%(width,height),height=height,xscrollcommand=mapcanvasscrollbar.set)
mapcanvas.pack(side=TOP,fill=X)
mapcanvasscrollbar.config(command=mapcanvas.xview)
mapcanvas.bind("<ButtonPress-1>",rel)
#top
maptop=Toplevel(maproot)
mapframecan=Frame(maptop)
mapframecan.grid(row=1,column=1,rowspan=2)
label=Label(mapframecan,text="Hoch").grid(row=1,column=1)
mapentryh=Entry(mapframecan)
mapentryh.grid(row=1,column=2)
mapentryh.insert(0,str(height))
mapentryh.bind("<KeyPress-Return>",cconf)
label=Label(mapframecan,text="Breit").grid(row=2,column=1)
mapentryb=Entry(mapframecan)
mapentryb.grid(row=2,column=2)
mapentryb.insert(0,str(width))
mapentryb.bind("<KeyPress-Return>",cconf)
cconf()
startbutton=Button(maptop,text="Start",width=20)
startbutton.grid(row=1,column=2)
startbutton.bind("<1>",start)
pinselframe=Frame(maptop)
pinselframe.grid(row=1,column=3,rowspan=4)
label=Label(pinselframe,text="Pinseldicke")
label.pack()
pinselbutton=Button(pinselframe,text=u"o",font=("Lucida Console",6,"bold"),width=1)
pinselbutton.pack()
pinselbutton.bind("<1>",pwidthconf)
schtop=Toplevel(maproot)  #sch
schtop.title("Schusseditor")
listschframe=Frame(schtop)
listschframe.grid(row=1,column=1,columnspan=3)
scrmap=Scrollbar(listschframe)
scrmap.pack(fill=Y,side=RIGHT)
schusslistmap=Listbox(listschframe,width=45,relief=RIDGE,yscrollcommand=scrmap.set)
schusslistmap.pack(fill=Y,side=LEFT)
schusslistmap.bind("<Double-ButtonPress-1>",schussconf)
scrmap.config(command=schusslistmap.yview)
#nummer,zeichen,sprengweite,anmerkung,schaden,sprengtiefe,[art,groesse,farbe],anzahl,[Preis,Kaufmenu]
schframe2=Frame(schtop)
for i in range(len(m)):
    label=Label(schframe2,text=m[i])
    label.grid(row=i,column=0)
    exec("entry"+m[i]+"=Entry(schframe2);entry"+m[i]+".grid(row=i,column=1)")
schframe2.grid(row=2,column=1,rowspan=4)
schbuttonframe=Frame(schtop)
schbuttonframe.grid(row=2,column=2,rowspan=5)
zeichenlabel=Label(schbuttonframe)
zeichenlabel.pack()
delbutton=Button(schbuttonframe,text="Loeschen",width=15)
delbutton.pack()
delbutton.bind("<1>",delsch)
ersbutton=Button(schbuttonframe,text="Anfuegen",width=15)
ersbutton.pack()
ersbutton.bind("<1>",erssch)
ersbutton=Button(schbuttonframe,text="Uebernehmen",width=15)
ersbutton.pack()
ersbutton.bind("<1>",erssch2)
ersbutton=Button(schbuttonframe,text="Speichern",width=15)
ersbutton.pack()
ersbutton.bind("<1>",speichernschuss)
savebutton=Button(maptop,text="Speichern")
savebutton.grid(row=3,column=1)
savebutton.bind("<1>",savemap)
loadbutton=Button(maptop,text="Laden")
loadbutton.grid(row=4,column=1)
loadbutton.bind("<1>",loadmap)
maproot.bind("<KeyPress-F1>",hilfe)
maptop.bind("<KeyPress-F1>",hilfe)
schtop.bind("<KeyPress-F1>",hilfe)
maproot.protocol("WM_DELETE_WINDOW",end)
maptop.protocol("WM_DELETE_WINDOW",end)
schtop.protocol("WM_DELETE_WINDOW",end)
#schussladen
try:
    f=file("schuss.cans","r")
    i=f.read()
    f.close()
    i=eval(i)
    schussart=i
except:
    i=tkMessageBox.askquestion(parent=maproot,title="ERROR",message=u"Configurierte Sch\u00fcsse konnten nicht geladen werden.\nDer Schussstandart wird \u00fcbernommen.\n Wollen sie die Standartsch\u00fcsse als default einstellen?")
    if i=="yes":
        f=file("schuss.cans","w")
        f.write(str(schussart))
        f.close()
schconf()
#platzieren
def b():
    schtop.geometry("+0+%s"%(maptop.winfo_geometry().split("+")[0].split("x")[1]))
    maproot.geometry("+%s+%s"%(schtop.winfo_geometry().split("+")[0].split("x")[0],maptop.winfo_geometry().split("+")[0].split("x")[1]))
    maptop.geometry("+0+0")
thread.start_new(b,())
#komandozeile
kommandotop=Toplevel(maproot)
kommandotop.title("Komandozeile")
mapexeentry=Entry(kommandotop,width=100)
mapexeentry.bind("<KeyPress-Return>",mapexecfunk)
mapexeentry.pack()
kommandotop.wm_withdraw()
maproot.bind_all("<Double-Key-F12>",lambda x:kommandotop.wm_deiconify())
maproot.bind_all("<Double-Key-F11>",lambda x:kommandotop.wm_withdraw())
#start
maproot.mainloop()
