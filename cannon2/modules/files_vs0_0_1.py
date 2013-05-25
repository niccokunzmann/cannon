__version__=("files",0,0,1)
def str_string(s,zeichen=()):
    """string => string ohne zeichen
    """
    

def _list_string(l,zeichen=()):
    """liste => string
    !!!nur interger!!!"""
    trenn=int_char(0,zeichen)
    string=""
    for i in l:
        string+=trenn+int_string(i,zeichen+(trenn,))
    return string[1:]

def _string_list(string,zeichen=()):
    """string => liste"""
    trenn=int_char(0,zeichen)
    s=string.split(trenn)
    l=[]
    for i in s:
        l.append(string_int(i,zeichen+(trenn,)))
    return l

def string_int(string,zeichen=()):
    """string => int
    in zeichen befinden sich die zeichen,
    die nicht enthalten sind."""
#    if len(zeichen)==1 and type(zeichen[0])==type(tuple()):zeichen=zeichen[0]
    k=256-len(zeichen)
    z=0
    if char_int(string[0],zeichen)==k-1:
        vz=-1
        string=string[1:]
    elif char_int(string[0],zeichen)==0:
        vz=1
        string=string[1:]
    for i in range(len(string)):
        z+=char_int(string[i],zeichen)*k**i
    return z*vz#error: kein vorzeichen

def int_string(i,zeichen=()):
    """int => string
    in zeichen befinden sich die zeichen,
    die nicht enthalten sind."""
#    if len(zeichen)==1 and type(zeichen[0])==type(tuple()):zeichen=zeichen[0]
    k=256-len(zeichen)
    if i<0:
        string=int_char(k-1,zeichen)
        i*=-1
    else:string=int_char(0,zeichen)
    while i>0:
        string+=int_char(i%k,zeichen)
        i/=k
    return string
    
def char_int(char,zeichen=()):
    """c-1 zeichen,
    in zeichen befinden sich die zeichen,
    die nicht enthalten sind.
    """
    c=ord(char)
    zeichen=list(zeichen)
    zeichen.sort()
    zeichen.reverse()
    for i in zeichen:
        if c >= ord(i): c-=1
    return c

def int_char(z,zeichen=()):
    """c-1 zeichen,
    in zeichen befinden sich die zeichen,
    die nicht enthalten sind.
    """
    if z+len(zeichen)>255:raise ValueError,"kann int nicht zu zeichen machen: int zu gross"
    zeichen=list(zeichen)
    zeichen.sort()
    for i in zeichen:
        if z >= ord(i): z+=1
    return chr(z)

def str_file(datei,string):
    f=file(datei,"w")
    z255,z26=(chr(255),chr(26))
    z2552=z255*2
    z262=z255+chr(254)
    s26=string.split(z26)
    for s in s26:
        s255=s.split(z255)
        f.writelines([z262+s255[0]]+[z2552+i for i in s255[1:]])
        f.flush()
    f.close()

def file_str(datei):
    f=file(datei,"r")
    z255,z26=(chr(255),chr(26))
    z2552=z255*2
    z262=z255+chr(254)
    l26=f.read().split(z262)[1:]
    string=z26x=""
    for l in l26:
        l255=l.split(z2552)
        s=z26x+l255[0]
        for i in l255[1:]:
            s+=z255+i
        string+=s
        z26x=z26
    f.close()
    return string
