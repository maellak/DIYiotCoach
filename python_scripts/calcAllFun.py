import math

alpha = 0.1
beta =  0.2
theta = 0.3

R = [
[math.cos(alpha)*math.cos(beta),math.cos(alpha)*math.sin(beta)*math.sin(theta) - math.sin(alpha)*math.cos(theta),math.cos(alpha)*math.sin(beta)*math.cos(theta) + math.sin(alpha)*math.sin(theta)]
,[math.sin(alpha)*math.cos(beta),math.sin(alpha)*math.sin(beta)*math.sin(theta)+math.cos(alpha)*math.cos(theta),math.sin(alpha)*math.sin(beta)*math.cos(theta) - math.cos(alpha)*math.sin(theta)]
,[-1* math.sin(beta),math.cos(beta) * math.sin(theta),math.cos(beta) * math.cos(theta)]
]
dt = 0.1

def calcAll(x,y,z):
	accel = [x,y,z]
	gravity = [0.0,0.0,0.0]

	pitch = math.atan2(x, math.sqrt(y * y) + (z * z))
	roll = math.atan2(y, math.sqrt(x * x) + (z * z))
	pitchDEG = pitch * 180.0 / math.pi
	rollDEG = roll * 180.0 / math.pi

	gravity[0]= math.sin(pitch)
	gravity[1]= math.sin(roll) 
	gravity[2]= math.sqrt(math.fabs(1-gravity[1]*gravity[1]+gravity[0]*gravity[0]))
	rG = [0,0,0]
	rA = [0,0,0]
	mA = [0,0,0]
	cm = [0,0,0]
	rG[0]= gravity[0]*R[0][0] + gravity[1]*R[0][1] + gravity[2]*R[0][2] 
	rG[1]= gravity[0]*R[1][0] + gravity[1]*R[1][1] + gravity[2]*R[1][2] 
	rG[2]= gravity[0]*R[2][0] + gravity[1]*R[2][1] + gravity[2]*R[2][2] 

	rA[0]= accel[0]*R[0][0] + accel[1]*R[0][1] + accel[2]*R[0][2] 
	rA[1]= accel[0]*R[1][0] + accel[1]*R[1][1] + accel[2]*R[1][2] 
	rA[2]= accel[0]*R[2][0] + accel[1]*R[2][1] + accel[2]*R[2][2] 

	mA[0]=rA[0]-rG[0]
	mA[1]=rA[1]-rG[1]
	mA[2]=rA[2]-rG[2]

	rA[0]= mA[0]*R[0][0] + mA[1]*R[1][0] + mA[2]*R[2][0] 
	rA[1]= mA[0]*R[0][1] + mA[1]*R[1][1] + mA[2]*R[2][1] 
	rA[2]= mA[0]*R[0][2] + mA[1]*R[1][2] + mA[2]*R[2][2] 


	#metro = math.sqrt(rA[0]*rA[0]+rA[1]*rA[1]+rA[2]*rA[2])
	cm[0] = rA[0]*9.81*(dt/1000)*(dt/1000)*100 
	cm[1] = rA[1]*9.81*(dt/1000)*(dt/1000)*100 
	cm[2] = rA[2]*9.81*(dt/1000)*(dt/1000)*100

	result = [pitch,roll,pitchDEG,rollDEG,rA[0],rA[1],rA[2],cm[0],cm[1],cm[2]]
	#pitch,roll(aktinia?),pitch,roll(moires),x,y,z(epitaxinseis xoris bari),x,y,z(metatopiseis stous 3 axones)

	return result

'''
ID = lForItems[i]
x = float(lForItems[i + 1])
y = float(lForItems[i + 2])
z = float(lForItems[i + 3])    
calcResults = calcAll(float(x),float(y),float(z))
nX = calcResults[4]
nY = calcResults[5]
nZ = calcResults[6]
pitch = calcResults[1]
roll = calcResults[2]
'''