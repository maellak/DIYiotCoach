
// these constants describe the pins that the two accelerometers are conected. They won't change:
                                      //accelerometer1
const int xpin = A0;                  // x-axis 
const int ypin = A1;                  // y-axis
const int zpin = A2;                  // z-axis (only on 3-axis models)

                                  
                                       
const int xpin2 = A3;                  // x-axis  
const int ypin2 = A4;                  // y-axis
const int zpin2 = A5;                  // z-axis (only on 3-axis models)
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
 pinMode(xpin2, INPUT);
 pinMode(ypin2, INPUT);
 pinMode(zpin2, INPUT);
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
  int x2 = analogRead(xpin2);
 //
 //add a small delay between pin readings.  I read that you should
 //do this but haven't tested the importance
   delay(1); 
 //
 int y2 = analogRead(ypin2);
 //
 //add a small delay between pin readings.  I read that you should
 //do this but haven't tested the importance
   delay(1); 
 //
 int z2 = analogRead(zpin2);
 //
 //zero_G2 is the reading we expect from the sensor when it detects
 //no acceleration.  Subtract this value from the sensor reading to
 //get a shifted sensor reading.
 float zero_G2 =512; 
 //
 //scale2 is the number of units we expect the sensor reading to
 //change when the acceleration along an axis changes by 1G.
 //Divide the shifted sensor reading by scale to get acceleration in Gs.
 float scale2 =102.3;
 //
 Serial.print("@C:");
 Serial.print(((float)x - zero_G)/scale);
 Serial.print(":");


 Serial.print(((float)y - zero_G)/scale);
  Serial.print(":");


 
 Serial.print(((float)z - zero_G)/scale);
  Serial.print(":");
 



Serial.print("D:");

  Serial.print(((float)x2 - zero_G2)/scale2);
   Serial.print(":");
 
 


Serial.print(((float)y2 - zero_G2)/scale2);
 Serial.print(":");




Serial.print(((float)z2 - zero_G2)/scale2);
 Serial.print("#");
 Serial.print("\n");


 // delay before next reading:
 delay(sampleDelay);

}

