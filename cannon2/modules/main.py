__doc__="""
Dieses Modul importiert alle Cannondateien
es sollte immer erst main importiert werden
 bevor irgendein anderes programm im ordner modules importiert wird
da beim importieren vom main noch nicht alle module geladen sein koennen,
 wird emfohlen eine parameterlose funktion in main.onload zu schreiben,
 die nach dem laden ausgefuert wird.
 das modul kann auch die funktion laden besitzen, fuer die das selbe zutrifft.
"""
if __name__=="__main__":
    import main
else:
    import os,sys,version
    var= vars()
    modul=name=None
    __all__=[]
    onload=[]
    for f in os.listdir(""):
        if not ".py" in f:continue
        name=f[:f.index(".py")]
        modul=__import__(name)
        if hasattr(modul,"__version__"):
            if ((modul.__version__[0] not in var) or version.vergleiche(modul,var[modul.__version__[0]])==1):
                var[modul.__version__[0]]=modul
                __all__.append(modul.__version__[0])
        else:
            var[name]=modul
            __all__.append(name)
    for modul in __all__:
        if hasattr(modul,"laden"):
            modul.laden()
    for f in main.onload:
        f()
    del var,modul,f,name
