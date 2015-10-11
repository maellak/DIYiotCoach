// these constants describe the pins. They won't change:
const int xpinA = A0;                  // x-axis of the accelerometer
const int ypinA= A1;                  // y-axis
const int zpinA = A2;                  // z-axis (only on 3-axis models)

const int xpinB = A3;                  // x-axis of the accelerometer
const int ypinB = A4;                  // y-axis
const int zpinB = A5;                  // z-axis (only on 3-axis models)


//
int sampleDelay = 500;   //number of milliseconds between readings
void setup()
{
 // initialize the serial communications:
 Serial.begin(9600);
 //
 //
 //for Arduino Uno
 //analogReference(EXTERNAL);
 
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
 //add a small delay between pin readings.  I read that you should
 //do this but haven't tested the importance
   delay(1); 
 //
 int yA = analogRead(ypinA);
 int yB = analogRead(ypinB);
 //
 //add a small delay between pin readings.  I read that you should
 //do this but haven't tested the importance
   delay(1); 
 //
 int zA = analogRead(zpinA);
 int zB = analogRead(zpinB);
 //
 //zero_G is the reading we expect from the sensor when it detects
 //no acceleration.  Subtract this value from the sensor reading to
 //get a shifted sensor reading.
 float zero_G =512; 
 //
 //scale is the number of units we expect the sensor reading to
 //change when the acceleration along an axis changes by 1G.
 //Divide the shifted sensor reading by scale to get acceleration in Gs.
 float scale =102.3;
 //
 Serial.print("@:A:");
 Serial.print(((float)xA - zero_G)/scale);
 Serial.print(":");
 Serial.print(((float)yA - zero_G)/scale);
 Serial.print(":");
 Serial.print(((float)zA - zero_G)/scale);
 Serial.print("B:");
 Serial.print(((float)xB - zero_G)/scale);
 Serial.print(":");
 Serial.print(((float)yB - zero_G)/scale);
 Serial.print(":");
 Serial.print(((float)zB - zero_G)/scale);
 Serial.print(":");
 Serial.println("#");
 //
 // delay before next reading:
 delay(sampleDelay);
}
