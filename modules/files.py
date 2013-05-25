def list_string(l,zeichen=()):
    """liste => string
    !!!nur interger!!!"""
    trenn=int_char(0,zeichen)
    string=""
    for i in l:
        string+=trenn+int_string(i,zeichen+(trenn,))
    return string[1:]

def string_list(string,zeichen=()):
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

def canvaselement_indent(canvas,nr):
    c=canvas.itemconfigure(nr)
    d={'text': 'text', 'image': 'image', 'bitmap': 'bitmap', 'window': 'window', 'style': 'arc', 'arrow': 'line'}
    for i in d:
        if i in c:
            return d[i]
    if 'smooth' in c:
        return 'polygon'
    return "rectangle or oval"


