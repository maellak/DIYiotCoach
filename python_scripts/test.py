import re


#DV einai i metaboli taxutitas (v=speed)
#DX einai i metaboli tis thesis 
#DXtot einai i sunoliki metatopisi
#acc einai i timi tis epitaxunsis 
#Vo einai i timi tis taxutitas


def calc_DX(state):
  #prevState[acc,DX,Vo]
  acc = state[0]
  DX = state[1]
  Vo = state[2]
  DV = acc*Dt
  DX = Vo*Dt + (1/2)*acc*Dt*Dt
  state[2] = Vo + DV/Dt
  state[1] = DX
  return state
  
Dt=0.005 #xronos se second tis deigmatolipsias 
file = open('test.txt', 'r')

#prevState[acc,DX,Vo]
state = [-1,-1,-1]
DXtot = 0


#calc_DXtotal
for i in range(0,10):
  str = file.readline()
  str = re.sub('[\n@#]', '', str)
  str = str.split(':')
  state[0] = float(str[2])
  
  state = calc_DX(state)
  DXtot = DXtot + state[1]
  print "Current State : %s" , state
  print "DX total : %s" , DXtot
  #print type (acc)












