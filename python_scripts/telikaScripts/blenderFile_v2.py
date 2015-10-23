import re
import bpy
import math

Dt = 0.005
def calc_DX(state):
    #prevState[acc,DX,Vo]
    acc = state[0] * 9.81
    DX = state[1]
    Vo = state[2]
    DV = acc*Dt
    DX = Vo*Dt + (1/2)*acc*Dt*Dt
    state[2] = Vo + DV/Dt
    state[1] = DX
    return state

def findPitch(x,y,z):
	pitch = math.atan2(x, math.sqrt(y * y) + (z * z))	
	pitch = pitch * (180.0 / math.pi)	
	return pitch

def findRoll(x,y,z):	
	roll = math.atan2(y, math.sqrt(x * x) + (z * z))	
	roll = roll * (180.0 / math.pi)
	return roll

lx = ly = lz = 0

def moveTennisPlayer(line): 
	j = 0   
	clearText = re.sub('[@\n\r]', '', line)
	lForItems = clearText.split(':')
	i = 0
	while (i+3 < len(lForItems)):
		ID = lForItems[i]
		x = lForItems[i + 1]
		y = lForItems[i + 2]
		z = lForItems[i + 3]    
		i += 4
		if ID == 'A': #Aristeri palami			
			#bpy.ops.object.select_pattern(pattern="forearm.L")
			bpy.ops.object.select_pattern(pattern="forearm.fk.L")
			#bpy.ops.transform.rotate(value=-1.40891, axis=(findRoll(float(x), float(y), float(z)), findPitch(float(x), float(y), float(z)),-0.458268))
			bpy.ops.transform.rotate(value=findRoll(float(x), float(y), float(z)), axis=(1,0,0))			
			bpy.ops.transform.rotate(value=findPitch(float(x), float(y), float(z)), axis=(0,1,0))
			#bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			a = 1
		elif ID == 'B':  # Aristeros omos
			#bpy.ops.object.select_pattern(pattern="deltoid.L")
			bpy.ops.object.select_pattern(pattern="shoulder.L")
			#bpy.ops.transform.rotate(value=-1.40891, axis=(findRoll(float(x), float(y), float(z)), findPitch(float(x), float(y), float(z)),-0.458268))
			bpy.ops.transform.rotate(value=findRoll(float(x), float(y), float(z)), axis=(1,0,0))			
			bpy.ops.transform.rotate(value=findPitch(float(x), float(y), float(z)), axis=(0,1,0))			
			#bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			a = 1
		elif ID == 'C':  # Dexi palami									
			#bpy.ops.object.select_pattern(pattern="forearm.R")
			bpy.ops.object.select_pattern(pattern="forearm.fk.R")
			bpy.ops.transform.rotate(value=findRoll(float(x), float(y), float(z)), axis=(1,0,0))			
			bpy.ops.transform.rotate(value=findPitch(float(x), float(y), float(z)), axis=(0,1,0))				
			a = 1			
		elif ID == 'D':  # Dexis omos
			#bpy.ops.object.select_pattern(pattern="deltoid.R")			
			bpy.ops.object.select_pattern(pattern="shoulder.R")
			#bpy.ops.transform.rotate(value=-1.40891, axis=(findRoll(float(x), float(y), float(z)), findPitch(float(x), float(y), float(z)),-0.458268))			
			bpy.ops.transform.rotate(value=findRoll(float(x), float(y), float(z)), axis=(1,0,0))			
			bpy.ops.transform.rotate(value=findPitch(float(x), float(y), float(z)), axis=(0,1,0))			
			a = 1					
		elif ID == 'E':  # Aristero mpouti
			#bpy.ops.object.select_pattern(pattern="shin.R")
			#bpy.ops.transform.rotate(value=-1.40891, axis=(findRoll(float(x), float(y), float(z)), findPitch(float(x), float(y), float(z)),-0.458268))
			#bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			bpy.ops.object.select_pattern(pattern="thigh.fk.L")
			bpy.ops.transform.rotate(value=findRoll(float(x), float(y), float(z)), axis=(1,0,0))			
			bpy.ops.transform.rotate(value=findPitch(float(x), float(y), float(z)), axis=(0,1,0))	
			a = 1			
		elif ID == 'F':  # Aristero astragalos
			bpy.ops.object.select_pattern(pattern="foot.ik.L")
			bpy.ops.transform.rotate(value=findRoll(float(x), float(y), float(z)), axis=(1,0,0))			
			bpy.ops.transform.rotate(value=findPitch(float(x), float(y), float(z)), axis=(0,1,0))	
			a = 1			
		elif ID == 'G':  # Nothing - Den xrisimopoihte
			a = 1			
		elif ID == 'H':  # Deksi mpouti
			bpy.ops.object.select_pattern(pattern="thigh.fk.R")
			bpy.ops.transform.rotate(value=findRoll(float(x), float(y), float(z)), axis=(1,0,0))			
			bpy.ops.transform.rotate(value=findPitch(float(x), float(y), float(z)), axis=(0,1,0))	
			a = 1			
		elif ID == 'I':  # Deksi astragalos
			bpy.ops.object.select_pattern(pattern="foot.ik.L")
			bpy.ops.transform.rotate(value=findRoll(float(x), float(y), float(z)), axis=(1,0,0))			
			bpy.ops.transform.rotate(value=findPitch(float(x), float(y), float(z)), axis=(0,1,0))	
			a = 1			
		elif ID == 'J':  # Kati ...
			#bpy.ops.object.select_pattern(pattern="forearm.R")
			#bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			a = 1					
		elif ID == 'K':  # Kati ...
			#bpy.ops.object.select_pattern(pattern="forearm.R")
			#bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			a = 1	
		elif ID == 'L':  # Kati ...
			#bpy.ops.object.select_pattern(pattern="forearm.R")
			#bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			a = 1	
		elif ID == 'M':  # Kati ...
			#bpy.ops.object.select_pattern(pattern="forearm.R")
			#bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			a = 1	
		else:
			a = 1
			#print("Nothing")
		bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=0.005)

f = open('/home/ellak/Desktop/dataBack2.txt', 'r')
for line in f.read().split('#'): 
	moveTennisPlayer(line)	
