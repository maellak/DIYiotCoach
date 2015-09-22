// these constants describe the pins. They won't change:
const int xpin = A1;                  // x-axis of the accelerometer
const int ypin = A2;                  // y-axis
const int zpin = A3;                  // z-axis (only on 3-axis models)
//
int sampleDelay = 500;   //number of milliseconds between readings
void setup()
{
 // initialize the serial communications:
 Serial.begin(9600);
 //
 //Make sure the analog-to-digital converter takes its reference voltage from
 // the AREF pin
 pinMode(xpin, INPUT);
 pinMode(ypin, INPUT);
 pinMode(zpin, INPUT);
}
void loop()
{
 int x = analogRead(xpin);
 //
 //add a small delay between pin readings.  I read that you should
 //do this but haven't tested the importance
   delay(1); 
 //
 int y = analogRead(ypin);
 //
 //add a small delay between pin readings.  I read that you should
 //do this but haven't tested the importance
   delay(1); 
 //
 int z = analogRead(zpin);
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
 Serial.print(((float)x - zero_G)/scale);
 Serial.print("\t");
 //
 Serial.print(((float)y - zero_G)/scale);
 Serial.print("\t");
 //
 Serial.print(((float)z - zero_G)/scale);
 Serial.print("\n");
 //
 // delay before next reading:
 delay(sampleDelay);
}

