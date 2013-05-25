from Tkinter import *
def ende(k):
    root.destroy()
    root.quit()
def hilfe(k):
    help.pack()
def farbe(k):
    f=entry.get()
    try:
        canvas.config(bg=f)
    except:
        p=1
root=Tk()
text="black"
root.title("Farbendefinieren")
root.iconbitmap("info")
label=Label(root,text="Hier bitte die Farbe definieren:")
entry=Entry(root,textvariable=text)
canvas=Canvas(root,width=200,height=100,cursor="pencil",bg=text)
help=Label(root,text="Hilfe\nman kann Farben wie black,green oder red eingeben.\noder diese abstufen(gray25,red2,blue4)\nHexadezimale Zahlen haben eine Raute am Anfang(#900,#55,88,99,#ABCDEF)\nAuf eine Raute folgt immer der Rotton,darauf der Gruenton und zum Schluss der Blauton.")
root.bind_all("<F1>",hilfe)
canvas.pack()
label.pack()
entry.pack()
root.bind_all("<Any-KeyPress>",farbe)
root.bind_all("Escape",ende)
root.mainloop()
