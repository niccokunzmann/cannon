import os,sys
from main import files
__version__=("verschl",0)

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
def permbit(c="\x00",n=0):
    t=8
    l=()
    c=ord(c)
    i=128
    while i>0:
        l+=(c/i,)
        c%=i
        i/=2
    print l
        #noch laenge auf 8-faches(len(txt) anhaengen?)
def encrypt(txt,schl=schl):
    """verschluesselt den text.
    es ist empfehlenswert den text mit
        zeichen zu ergaenzen, bis seine laenge
        ein vielfaches von 8 ergibt.
    das programm macht das automatisch mit nullzeichen
    """
    i=0
    lentxt=len(txt)
    lenschl=len(schl)
    lall=[]
    index=[0]
    schluessel=iterator(schl,index)
    #boxliste erzeugen [[[] x 8], ...]
    for n in txt:
        if i%8==0:
            lbox=[]
            lall.append(lbox)
        t=int_tuple(ord(n)^ord(schluessel.next()))
        lbox.append(t)
        i+=1
    t=(0,)*8
    lall[-1]+=[t]*(-lentxt%8)
    # boxen shiften
    itlistboshift=[]
    i=1
    while i<lentxt:
        itlistboshift.append(i)
        i*=256
    lenlall=len(lall)
    lentxt=lenlall*8
    for runde in range(10):
        i=lenlall
        lallklon=lall[:]
        while i:
            i-=1
            lall[i]=zip(*shiftbox(lallklon[i]\
                    ,int_octtuple(schluessel.next()\
                    +schluessel.next()+schluessel.next())))
        #boliste shiften
        t=()
        i=8
        while i:
            #shifttuple erstellen
            i-=1
            k=0
            for j in itlistboshift:k+=ord(schluessel.next())*j
            t+=(k,)
        l=[]#liste fuer bitreihen aus lall
        for i in lall:l+=i
        bitlist=zip(*shiftbox(zip(*l),t))#lall-bitreihen shiften, in byte-tuple fassen
        lall=[]
        #ausgangsposition herstellen
        i=0
        while i<lentxt:
            if i%8==0:
                lbox=[]
                lall.append(lbox)
            lbox.append(bitlist[i])
            i+=1
    r=""
    for b in lall:
        rt=""
        for t in b:
            r+=chr(tuple_int(t))
        r+=rt
    return files.int_string(index[0],("\x00",))+"\x00"+r

def decrypt(txt,schl=schl):
    i=txt.index("\x00")
    index=[files.string_int(txt[:i],("\x00",))]
    schluessel=iterator(schl,index,-1)
    lentxt=len(txt)
    lall=[]
    n=0
    for i in txt[i+1:]:
        if n%8==0:
            lbox=[]
            lall.append(lbox)
        lbox.append(int_tuple(ord(i)))
        n+=1
    for runde in range(10):
        pass
    
def int_octtuple(c3):
    z=ord(c3[0])+ord(c3[1])*256+ord(c3[2])*65536
    r=()
    while len(r)<8:
        r2=divmod(z,8)
        r+=r2[1:]
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
