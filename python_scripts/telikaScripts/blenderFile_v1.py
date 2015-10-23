import re
import bpy

def moveTennisPlayer(line):    
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
			bpy.ops.object.select_pattern(pattern="forearm.L")
			bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			a = 1
		elif ID == 'B':  # Aristeros omos
			bpy.ops.object.select_pattern(pattern="deltoid.L")
			bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			a = 1
		elif ID == 'C':  # Dexi palami
			bpy.ops.object.select_pattern(pattern="forearm.R")
			bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			a = 1			
		elif ID == 'D':  # Dexis omos
			bpy.ops.object.select_pattern(pattern="deltoid.R")
			bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			a = 1			
		elif ID == 'E':  # Aristero mpouti
			bpy.ops.object.select_pattern(pattern="thigh.L")
			bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			a = 1			
		elif ID == 'F':  # Aristero astragalos
			bpy.ops.object.select_pattern(pattern="shin.L")
			bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			a = 1			
		elif ID == 'G':  # Nothing - Den xrisimopoihte
			a = 1			
		elif ID == 'H':  # Deksi mpouti
			bpy.ops.object.select_pattern(pattern="thigh.R")
			bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
			a = 1			
		elif ID == 'I':  # Deksi astragalos
			bpy.ops.object.select_pattern(pattern="shin.R")
			bpy.ops.transform.translate(value=(float(x), float(y), float(z)))
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

f = open('/home/ellak/Desktop/Mike/realData/remoteTest.txt', 'r')
for line in f.read().split('#'): 
	moveTennisPlayer(line)	

	
		#object = bpy.data.objects['Desktop:forearm.R']
		#object.select = True
	

