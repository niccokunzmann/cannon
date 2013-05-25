import main
main=vars(main)
__version__=("struktur",0)
def _splitpfad(pfad):
    l1=pfad.split("\\")
    l=[]
    for s in l1:
        l+=s.split("/")
    return l 

def getvar(pfad,environ=main):
    """=> wert
    gibt den wert der variblen spezifisiert in pfad zurueck"""
    return _walk(_splitpfad(pfad),environ)

def _walk(pfadlist,environ=main,*wert):
    """=> wert
    wandert nach pfadlist durch environ.
    wenn wert:
        variable wird gesetzt"""
    for loc in pfadlist:
        if loc == pfadlist[-1]:
            if wert:
                environ[loc]=wert[0]
            else:
                return environ[loc]
        else:
            environ=vars(environ[loc])

def setvar(pfad,wert,environ=main):
    """setvar(pfad=wert)"""
    _walk(_splitpfad(pfad),environ,wert)

class Struktur:
    def getvar(self,pfad):
        """=> wert
        pfad kann relativ sein (er beginnt mit \\ oder /)
        oder sonst absolut
        """
        if pfad[0] in "\\/":
            return getvar(pfad[1:],self.__dict__)
        return gatvar(pfad)
    def setvar(self,pfad,wert):
        """pfad=wert
        pfad kann relativ sein (er beginnt mit \\ oder /)
        oder sonst absolut
        """
        if pfad[0] in "\\/":
            return setvar(self.__dict__,{pfad[1:]:wert})
        return setvar(pfad=wert)
