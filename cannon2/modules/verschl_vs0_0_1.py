import os,sys
from main import files
__version__=("verschl",0,0,1)
__doc__="""
dieses modul dient der verschluesselung.
mit encrypt wird ver- mit decrypt entschluesselt.
"""

if not "randsch" in os.listdir(""):
    schl=os.urandom(51200)
    files.str_file("randsch",schl)
else:
    schl=files.file_str("randsch")

def faku(n):
    if n==0 or n==1:return 1
    return faku(n-1)*n

def perm(it="",n=0):
    it=list(it)
    r=""
    for i in xrange(len(it),0,-1):
        b=it[n%i]
        r+=b
        it.remove(b)
        n/=i
    return r

def encrypt(txt,schl=schl):
    """verschluesselt den text.
    es ist empfehlenswert den text mit
        zeichen zu ergaenzen, bis seine laenge
        ein vielfaches von 8 ergibt.
    das programm macht das automatisch mit "\x88"
    """;test=[]
    i=0
    txt+="\x88"*(-len(txt)%8)
    lentxt=len(txt)
    lenschl=len(schl)
    lall=[]
    index=[0]
    schluessel=iterator(schl,index)
    ##########################################################
    #boxliste erzeugen [[[] x 8], ...]
    for n in txt:
        if i%8==0:
            lbox=[]
            lall.append(lbox)
        t=int_tuple(ord(n)^ord(schluessel.next()))
        lbox.append(t)
        i+=1
    #auf laenge | 8 bringen
    lenlall=len(lall)
    test.append(lall)
    ##########################################################
    # boxen shiften
    itlistboshift=[]
    i=1
    while i<lentxt:
        itlistboshift.append(i)
        i=i<<8
    ##########################################################
    for runde in range(10):
        ##########################################################
        #boxen shiften
        i=lenlall
        lallklon=lall[:]
        while i:
            i-=1
            lall[i]=zip(*shiftbox(lallklon[i]\
                    ,int_octtuple(schluessel.next()\
                    +schluessel.next()+schluessel.next())))
        test.append(lall)
        ##########################################################
        #boxliste shiften
        t=()
        for i in range(8):
            #shifttuple erstellen
            k=0
            for j in itlistboshift:k+=ord(schluessel.next())*j
            t+=(k,)
        l=[]#liste fuer bitreihen aus lall
        for i in lall:l+=i
        bitlist=zip(*shiftbox(zip(*l),t))#lall-bitreihen shiften, in byte-tuple fassen
        test.append(bitlist)
        #ausgangsposition herstellen
        lall=[]
        i=0
        while i<lentxt:
            if i%8==0:
                lbox=[]
                lall.append(lbox)
            lbox.append(bitlist[i])
            i+=1
        test.append(lall)
    ##########################################################
    r=""
    for b in lall:
        rt=""
        for t in b:
            rt+=chr(tuple_int(t))
        r+=rt
    return files.int_string(index[0],("\x00",))+"\x00"+r#,schl,test

def decrypt(txt,schl=schl,):# test=[]):
    """
    entschluesslt den text in txt mit dem schluessel in schl
    es kann vorkommen, das letzte zeichen fehlen, wenn diese lauteten:"\x88"
    """
    i=txt.index("\x00")
    index=[files.string_int(txt[:i],("\x00",))]
    schluessel=iterator(schl,index,-1)
    lentxt=len(txt)-i-1
    lall=[]
    n=0
    ##########################################################getestet
    #lall erzeugen
    for i in txt[i+1:]:
        if n%8==0:
            lbox=[]
            lall.append(lbox)
        lbox.append(int_tuple(ord(i)))
        n+=1
#    print test[-1]==lall
    ##########################################################getestet
    # boxen shiften
    itlistboshift=[]
    i=1
    while i<lentxt:
        itlistboshift.append(i)
        i=i<<8
    itlistboshift.reverse()
    ##########################################################
    lenlall=len(lall)
    for runde in range(10):
        ##########################################################
        #boxliste shiften - 
        t=[]
        for i in range(8):
            #shifttuple erstellen
            k=0
            for j in itlistboshift:k-=ord(schluessel.next())*j
            t.append(k)
        l=[]#liste fuer bitreihen aus lall
        for i in lall:l+=i
        t.reverse()
        bitlist=zip(*shiftbox(zip(*l),t))#lall-bitreihen shiften, in byte-tuple fassen
#        print test[-2]==bitlist
        #ausgangsposition herstellen
        lall=[]
        i=0
        while i<lentxt:
            if i%8==0:
                lbox=[]
                lall.append(lbox)
            lbox.append(bitlist[i])
            i+=1
#        print test[-3]==lall
        ##########################################################
        #boxen shiften
        i=0
        lallklon=lall[:]
        while i<lenlall:
            lall[i]=shiftbox(zip(*lallklon[i])\
                    ,int_negocttuple(schluessel.next()\
                    +schluessel.next()+schluessel.next()))
            i+=1
#        print test[-4]==lall
    ##########################################################
    r=""
    lall.reverse()
    for b in lall:
        rt=""
        b.reverse()
        for t in b:
            rt=chr(tuple_int(t)^ord(schluessel.next()))+rt
        r=rt+r
    i=0
    while r[i-1]=="\x88":i-=1
#    print index # kontrolle: wenn [0]:alles ok
    if i ==0:
        return r
    else:return r[:i]
    
def int_octtuple(c3):
    z=ord(c3[0])+ord(c3[1])*256+ord(c3[2])*65536
    r=()
    for i in range(8):
        r2=divmod(z,8)
        r+=r2[1:]
        z=r2[0]
    return r
def int_negocttuple(c3):
    z=(ord(c3[2])+ord(c3[1])*256+ord(c3[0])*65536)
    r=()
    for i in range(8):
        r2=divmod(z,8)
        r+=(-r2[1],)
        z=r2[0]
    return r

def int_tuple(c):
    """nur fur ord(c)"""
    l=()
    i=128
    while i>0:
        l+=(c/i,)
        c%=i
        i/=2
    return l

def tuple_int(t):
    l=0
    i=128
    while i:
        l+=t[0]*i
        t=t[1:]
        i/=2
    return l

def shifttuple(t,n):
    return t[n:]+t[:n]
def shiftbox(b,t):
    return [shifttuple(b[i],t[i]) for i in range(len(b))]

def iterator(s,l=None,step=1):
    """l ist eine liste, die immer den index enthaelt (ab l[0] wird gestartet)
    """
    if not l:
        l=len(s)
        i=0
        while 1:
            yield s[i%l]
            i+=step
    li=l
    l=len(s)
    while 1:
        yield s[li[0]%l]
        li[0]+=step
        
##von toni##
# Bitshift <- (Byte)
def lshift(x, n):
   return (x << n) % 256 | (x >> 8 - n)
 

# Bitshift -> (Byte)
def rshift(x, n):
   return (x >> n) | (x << 8 - n) % 256
##        ##
