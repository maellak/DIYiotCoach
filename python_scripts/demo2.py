import sys
import re
import threading
#import time
import pty
#import tty
import os

def moveTennisPlayer(strRelocation):
    try:       
        clearText = re.sub('[@\n\r]', '', strRelocation)
        #print(strRelocation)
        lForItems = clearText.split(':')
        print(lForItems)
        
        i = 0
        while (i < len(lForItems)):
            ID = lForItems[i]
            
            if ID == 'N': #Px an einai to heading kai exei mono ena aistitira!
                x = lForItems[i + 1]
                i +=2 
                print (float(x))            
            else:
                x = lForItems[i + 1]
                y = lForItems[i + 2]
                z = lForItems[i + 3]    
                print (float(x))
                print (float(y))
                print (float(z))
                i += 4
                    
            print(ID)
            
            
            if ID == 'A':  # Deksi_wmos
                print("Move : Deksi_wmos")                
            elif ID == 'B':  # Deksi_agkwnas
                print("Move : Deksi_agkwnas")
            elif ID == 'C':  # Deksi_kapros
                print("Move : Deksi_kapros")
            elif ID == 'D':  # Aristero_wmos
                print("Move : Aristero_wmos")
            elif ID == 'E':  # Aristero_agkwnas
                print("Move : Aristero_agkwnas")
            elif ID == 'F':  # Aristero_karpos
                print("Move : Aristero_karpos")
            elif ID == 'G':  # Thorakas
                print("Move : Thorakas")
            elif ID == 'H':  # Deksi_gonato
                print("Move : Deksi_gonato")
            elif ID == 'I':  # Deksi_kalami
                print("Move : Deksi_kalami")
            elif ID == 'J':  # Aristero_gonato
                print("Move : Aristero_gonato")
            elif ID == 'K':  # Aristero_kalami
                print("Move : Aristero_kalami")
            else:
                print("Nothing")
    except Exception:
        return False
    return True


f = open('/home/ellak/Desktop/Mike/realData/remoteTest.txt', 'w')
print("Demo!")
for line in sys.stdin:    
	print(line)
	f.write(line)		
f.close()

'''
age = raw_input("Push any Button: ")
from subprocess import Popen, PIPE, STDOUT
cmd = 'socat - tcp-listen:1234,fork'
master, slave = pty.openpty()
p = Popen(cmd, shell=True, stdin=PIPE, stdout=slave, stderr=slave, close_fds=True)
stdout = os.fdopen(master)
#print (stderdout.readline())
print (stdout.readline())
'''