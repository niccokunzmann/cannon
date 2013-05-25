__doc__="""
ein versionstupel sollte so aussehen:
    (name,v1,v2,v3,...)
name ist der name, als welcher dieses document von main importiert wird
v1,v2,v3,... sind die einzelnen versionsnummern, in der rangliste ihrer indexe.
so ist ( version(("c",1,2,3,4))<version(("c",2,1,2)) )==True

jedes so importierte modul sollte __version__ aufweisen
die kleinste version ist version (0,[0,0,...])
"""
__version__=("version",0)

def vergleiche(modul1,modul2):
    """1 => modul1 > modul2
    0 => modul1 == modul2
    -1 => modul1 < modul2
    """
    if hasattr(modul1,"__version__") and hasattr(modul2,"__version__"):
        v1,v2=modul1.__version__[1:],modul2.__version__[1:]
        l1,l2=len(v1),len(v2)
        if l1>=l2:
            v1,v2=v2,v1
            l1,l2=l2,l1
            m=-1
        else:
            m=1
        for i in range(l1):
            e=cmp(v1[i],v2[i])
            if e!=0:
                return m*e
        for i in v2[l1:]:
            if i:
                return -m
        return 0
    else:
        return 0
