import sys,time
print sys.argv
s=time.asctime(time.localtime())
print s
file("last modified.txt","w").write(s)
time.sleep(5)
