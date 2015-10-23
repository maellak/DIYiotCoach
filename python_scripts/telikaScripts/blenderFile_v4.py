#Ta sxolia einai se latinikous xaraktikes gia na min yparxei problima kodikopoihsis se opoiodipote systima!
import re
import bpy
import math
from queue import LifoQueue
'''
ManageSensor = Klasi gia na diaxeirizetai tis times apo toys diaforoys aistitires .
To x,y,z pairnei ti mso oro ton 5 teleytaion timon gia megaliteri akrivia .
Episis poly eykola , deinontas apla x,y,z mporoyme na paroyme to trexon pitch & roll(aktinia kai moires),epitaxinseis(xyz)xoris bari kai metatopisesi sto xoro(xyz)
Oi metatopiseis den einai exakrivomeno oti doylevoun sosta - Einai dokimastika ...
'''
class ManageSensor:
	#Static variables :
	alpha = 0.1
	beta =  0.2
	theta = 0.3
	R = [
	[math.cos(alpha)*math.cos(beta),math.cos(alpha)*math.sin(beta)*math.sin(theta) - math.sin(alpha)*math.cos(theta),math.cos(alpha)*math.sin(beta)*math.cos(theta) + math.sin(alpha)*math.sin(theta)]
	,[math.sin(alpha)*math.cos(beta),math.sin(alpha)*math.sin(beta)*math.sin(theta)+math.cos(alpha)*math.cos(theta),math.sin(alpha)*math.sin(beta)*math.cos(theta) - math.cos(alpha)*math.sin(theta)]
	,[-1* math.sin(beta),math.cos(beta) * math.sin(theta),math.cos(beta) * math.cos(theta)]
	]
	dt = 0.1
	#Variables :
	nameSensor = ""
	x = 0.0
	y = 0.0
	z = 0.0
	curPitch = 0.0
	curRoll = 0.0
	curPitchDEG = 0.0
	curRollDEG = 0.0
	rG = [0,0,0]
	rA = [0,0,0]
	mA = [0,0,0]
	cm = [0,0,0]
	typeSensor = -1 # 0 => Acc,1 => gyr,2 => magn

	qFx = LifoQueue(5)
	qFsumX = 0.0
	qFy = LifoQueue(5)
	qFsumY = 0.0  
	qFz = LifoQueue(5)
	qFsumZ = 0.0  

	#Con :
	def __init__(self,ts,ns):
		typeSensor = ts
		nameSensor = ns
	#Methods :
	def newValues(self,nX,nY,nZ):           
		self.qFsumX += nX
		if self.qFx.full():
			self.qFsumX -= self.qFx.get()
		self.qFx.put(nX)
		self.qFsumY += nY
		if self.qFy.full():
			self.qFsumY -=self.qFy.get()
		self.qFy.put(nY)

		self.qFsumZ += nZ
		if self.qFz.full():
			self.qFsumZ -=self.qFz.get()
		self.qFz.put(nZ)        

		x = self.qFsumX / self.qFx.qsize()
		y = self.qFsumY / self.qFy.qsize()
		z = self.qFsumZ / self.qFz.qsize()

		#Calc pitch and roll :
		self.curPitch = math.atan2(x, math.sqrt(y * y) + (z * z))
		self.curRoll = math.atan2(y, math.sqrt(x * x) + (z * z))
		self.curPitchDEG = self.curPitch * 180.0 / math.pi
		self.curRollDEG = self.curRoll * 180.0 / math.pi

		accel = [x,y,z]
		gravity = [0.0,0.0,0.0]     

		gravity[0]= math.sin(self.curPitch)
		gravity[1]= math.sin(self.curRoll) 
		gravity[2]= math.sqrt(math.fabs(1-gravity[1]*gravity[1]+gravity[0]*gravity[0]))

		self.rG[0]= gravity[0]*ManageSensor.R[0][0] + gravity[1]*ManageSensor.R[0][1] + gravity[2]*ManageSensor.R[0][2] 
		self.rG[1]= gravity[0]*ManageSensor.R[1][0] + gravity[1]*ManageSensor.R[1][1] + gravity[2]*ManageSensor.R[1][2] 
		self.rG[2]= gravity[0]*ManageSensor.R[2][0] + gravity[1]*ManageSensor.R[2][1] + gravity[2]*ManageSensor.R[2][2] 

		self.rA[0]= accel[0]*ManageSensor.R[0][0] + accel[1]*ManageSensor.R[0][1] + accel[2]*ManageSensor.R[0][2] 
		self.rA[1]= accel[0]*ManageSensor.R[1][0] + accel[1]*ManageSensor.R[1][1] + accel[2]*ManageSensor.R[1][2] 
		self.rA[2]= accel[0]*ManageSensor.R[2][0] + accel[1]*ManageSensor.R[2][1] + accel[2]*ManageSensor.R[2][2] 

		self.mA[0]=self.rA[0]-self.rG[0]
		self.mA[1]=self.rA[1]-self.rG[1]
		self.mA[2]=self.rA[2]-self.rG[2]

		self.rA[0]= self.mA[0]*ManageSensor.R[0][0] + self.mA[1]*ManageSensor.R[1][0] + self.mA[2]*ManageSensor.R[2][0] 
		self.rA[1]= self.mA[0]*ManageSensor.R[0][1] + self.mA[1]*ManageSensor.R[1][1] + self.mA[2]*ManageSensor.R[2][1] 
		self.rA[2]= self.mA[0]*ManageSensor.R[0][2] + self.mA[1]*ManageSensor.R[1][2] + self.mA[2]*ManageSensor.R[2][2] 

		#metro = math.sqrt(rA[0]*rA[0]+rA[1]*rA[1]+rA[2]*rA[2])
		self.cm[0] = self.rA[0]*9.81*(ManageSensor.dt/1)*(ManageSensor.dt/1)*1 
		self.cm[1] = self.rA[1]*9.81*(ManageSensor.dt/1)*(ManageSensor.dt/1)*1 
		self.cm[2] = self.rA[2]*9.81*(ManageSensor.dt/1)*(ManageSensor.dt/1)*1

	def getPitch(self,Reg = True):
		if Reg:
			return self.curPitchDEG
		else:
			return self.curPitch
	def getRoll(self,Reg = True):
		if Reg:
			return self.curRollDEG
		else:
			return self.curRoll
	def getAccelerations(self):
		return self.rA
	def getSumAccelerations(self):
		return [self.qFsumX,self.qFsumY,self.qFsumZ]
	def getRelocations(self):
		return self.cm

sA = ManageSensor(0,"A") # Deinoyme typo aistitira kai onoma (Gia pithanon mellontiki xrisi)
counter = 0 # Yparxei gia na kanei kiniseis to montelo mas ana  5 deigmata opos fainetai pio kato sto if counter == 5
def moveTennisPlayer(line): 
	#Dilononte global gia na mporei na vlepei i synartisi aytes tis 2 katholikes metavlites .
	global counter
	global sA	
	clearText = re.sub('[@\n\r]', '', line)
	lForItems = clearText.split(':')
	i = 0 # Einai o deiktis gia ta kommatia tis listas - gramis poy exoyme diabasei ..
	while (i+3 < len(lForItems)):
		ID = lForItems[i] 
		x = float(lForItems[i + 1])
		y = float(lForItems[i + 2])
		z = float(lForItems[i + 3])
		i+=4 # Ayxanetai kata 4 gia na paroyme to epomeno ID me ta 3 x,y,z toy
		counter +=1
		if counter == 5: 
			counter = 0			
		if ID ==  'F':  # Aristeros astragalos (gia dokimes) *** Ypirxe palia to 'A': #Aristeri palami
			sA.newValues(x,y,z)	
			if counter == 0: #An einai 0 o counter tote metakinoume to montelo mas (anthropino omoiwma)
				bpy.ops.object.select_pattern(pattern="shin.fk.L")				
				bpy.ops.transform.rotate(value=sA.getRoll(), axis=(1,0,0))							
				#bpy.ops.transform.rotate(value=sA.getPitch(), axis=(0,1,0))
				#accelerations = sA.getAccelerations()
				#bpy.ops.transform.translate(value=(accelerations[0], accelerations[1], accelerations[2]))	
				
				#Ginetai elenhos gia na min xepernaei i timi toy axona x to limit min kai max poy exei ..(Den einai sigouro oti paizei sosta)
				if bpy.context.object.pose.bones["shin.fk.L"].constraints["Limit Rotation"].min_x > bpy.context.object.pose.bones["shin.fk.L"].rotation_quaternion[1]:
					bpy.context.object.pose.bones["shin.fk.L"].rotation_quaternion[1] = bpy.context.object.pose.bones["shin.fk.L"].constraints["Limit Rotation"].min_x
				if bpy.context.object.pose.bones["shin.fk.L"].constraints["Limit Rotation"].max_x < bpy.context.object.pose.bones["shin.fk.L"].rotation_quaternion[1]:
					bpy.context.object.pose.bones["shin.fk.L"].rotation_quaternion[1] = bpy.context.object.pose.bones["shin.fk.L"].constraints["Limit Rotation"].max_x
			a = 1	#Gia otan xreiastei na min kanei tipota If, na exei periexomeno ...
		'''
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
			bpy.ops.object.select_pattern(pattern="hand.fk.R")
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
		'''
		if counter == 0:
			bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=0.005)

f = open('C:\\realData\\Podia\\LegAstragalosLeft\\LegLeftBendKnee.txt', 'r')
for line in f.read().split('#'): 
	moveTennisPlayer(line)	


