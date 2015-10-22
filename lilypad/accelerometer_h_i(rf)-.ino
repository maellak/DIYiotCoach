class error{
public:
double fXg;
double fYg;
double fZg;
float alpha;
double pitch;
double roll;
  error(){
  alpha =0.5;
  fXg = 0;
  fYg = 0;
  fZg = 0;
  };
  void values(double Xg, double Yg, double Zg){
  //double pitch, roll, Xg, Yg, Zg;
  //acc.read(&Xg, &Yg, &Zg);
  
  //Low Pass Filter
  fXg = Xg * alpha + (fXg * (1.0 - alpha));
  fYg = Yg * alpha + (fYg * (1.0 - alpha));
  fZg = Zg * alpha + (fZg * (1.0 - alpha));
  
  //Roll & Pitch Equations
  roll = (atan2(-fYg, fZg)*180.0)/M_PI;
  pitch = (atan2(fXg, sqrt(fYg*fYg + fZg*fZg))*180.0)/M_PI;
  
  };
  double getX(){
    return fXg;
  };
  double getY(){
    return fYg;
  };
  double getZ(){
    return fZg;
  };
};
// these constants describe the pins. They won't change:
const int xpinA = A0; // x-axis of the accelerometer
const int ypinA= A1; // y-axis
const int zpinA = A2; // z-axis (only on 3-axis models)

const int xpinB = A3; // x-axis of the accelerometer
const int ypinB = A4; // y-axis
const int zpinB = A5; // z-axis (only on 3-axis models)


//
int sampleDelay = 3; //number of milliseconds between readings
error *err;
error *err2;
void setup()
{
// initialize the serial communications:
Serial.begin(115200);
Serial.setTimeout(5);
err = new error();
err2 =new error();
//
//Make sure the analog-to-digital converter takes its reference voltage from
// the AREF pin
pinMode(xpinA, INPUT);
pinMode(ypinA, INPUT);
pinMode(zpinA, INPUT);

pinMode(xpinB, INPUT);
pinMode(ypinB, INPUT);
pinMode(zpinB, INPUT);
}

void loop()
{
 
int xA = analogRead(xpinA);
int xB = analogRead(xpinB);
//
//add a small delay between pin readings. I read that you should
//do this but haven't tested the importance
delay(1);
//
int yA = analogRead(ypinA);
int yB = analogRead(ypinB);
//
//add a small delay between pin readings. I read that you should
//do this but haven't tested the importance
delay(1);
//
int zA = analogRead(zpinA);
int zB = analogRead(zpinB);
//
//zero_G is the reading we expect from the sensor when it detects
//no acceleration. Subtract this value from the sensor reading to
//get a shifted sensor reading.
float zero_G =512;
//
//scale is the number of units we expect the sensor reading to
//change when the acceleration along an axis changes by 1G.
//Divide the shifted sensor reading by scale to get acceleration in Gs.
float scale =102.3;
//

err->values(xA,yA,zA); 
err2->values(xB,yB,zB);
Serial.print("@H:");
Serial.print(((float)err->getX() - zero_G)/scale);
Serial.print(":");
Serial.print(((float)err->getY() - zero_G)/scale);
Serial.print(":");
Serial.print(((float)err->getZ() - zero_G)/scale);
Serial.print(":");
Serial.print("I:");
Serial.print(((float)err2->getX() - zero_G)/scale);
Serial.print(":");
Serial.print(((float)err2->getY() - zero_G)/scale);
Serial.print(":");
Serial.print(((float)err2->getZ() - zero_G)/scale);
Serial.println("#");

//
// delay before next reading:
delay(sampleDelay);
}
