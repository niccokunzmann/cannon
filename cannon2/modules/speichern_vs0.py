__version__=("speichern",0)
__doc__="""
in daten befindet sich der pfad zu der speichervariablen.
 {speicherpfad:ladepfad}
 in speicherpfad kann sich ein string oder eine funktion,
  die einen string zurueck gibt, befinden.
 in ladepfad befindet sich eine funktion,
  die mit den ladewerten ausgefuehrt wird oder
  ein string wird hinein geschrieben
"""
trenn="\n"
import main
daten={}

def pfad_int(pfad):
    s="1234567890qwertzuiopasdfghjklyxcvbnm_QWERTZUIOPASDFGHJKLYXCVBNM/"
    z=0
    for i in pfad:
        if i=="\\":
            i="/"
        z=z<<6
        z+=s.index(i)#error: ungueltiger pfad!
    return z

def int_pfad(z):
    s="1234567890qwertzuiopasdfghjklyxcvbnm_QWERTZUIOPASDFGHJKLYXCVBNM/"
    r=""
    while z:
        r=s[z%64]+r
        z/=64
    return r

def save(daten=daten,pfad="save"):
    s=""
    files.str_file(pfad,s)
def load(pfad="save"):
    pass
        
