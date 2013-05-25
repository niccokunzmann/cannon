(j,n)=1,0
h=input("Hilfe? (j/n) ")
if h:
    print """Das kleinste Zeichen ist 1, das groesste 65536.
    Es wird ausgegeben:
    Zeichen - hexadezimale Nummer - dezimale Nummer
    Um das Zeichen im Cannon Mapeditor zu benutzen: >u'\u hexadezimale Nummer'< engeben. 
    """
    ##schach 2654,2714,nr-278a
a=input("Unicodebeginn:")
e=input("Unicodeende:")
from Tkinter import *
import thread
h=Tk()
s=Scrollbar(h)
s.pack(side=RIGHT,fill=Y)
l=Listbox(h,yscrollcommand=s.set)
def wer(s):
    d="0"*(4-len(s))+s
    return d
def g(a,e):
    for i in range(a,e):
        exec("l.insert(END, u'\\u"+wer(str(hex(i))[2:])+" - "+wer(str(hex(i))[2:])+" - "+str(i)+"')")
thread.start_new(g,(a,e))
l.pack(side=LEFT,fill=X)
s.config(command=l.yview)
h.mainloop()
