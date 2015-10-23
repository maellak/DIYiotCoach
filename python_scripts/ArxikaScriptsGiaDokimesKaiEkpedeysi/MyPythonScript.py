import re
Dt=0.005 #xronos se msec metaksu eggrafwn
 
file = open('test.txt', 'r')
str = file.readline()
str=re.sub('[\n@#]', '', str)
str = str.split(':')

accx=str[1]
accy=str[2]
accz=str[3]

Dux=accx*Dt
Duy=accy*Dt
Duz=accz*Dt