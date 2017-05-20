#include <Wire.h>

//DHT-------
#include <DHT.h>;
#define DHTPIN 13   
#define DHTPIN2 12  
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino
DHT dht2(DHTPIN2, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino
//DHT-------


#define pump 7
long previousMillis = 0;
long interval = 60000;   // This is how often to send data to raspberry PI to log in milliseconds



void writeI2CRegister8bit(int addr, int value) {
  Wire.beginTransmission(addr);
  Wire.write(value);
  Wire.endTransmission();
}

unsigned int readI2CRegistepump6bit(int addr, int reg) {
  Wire.beginTransmission(addr);
  Wire.write(reg);
  Wire.endTransmission();
  delay(1100);
  Wire.requestFrom(addr, 2);
  unsigned int t = Wire.read() << 8;
  t = t | Wire.read();
  return t;
}


//DHT-------
int chk;
float hum;
float temp;
float hum2; 
float temp2; 
float hum3;  
float temp3; 
int hum4;
int temp4;
int hum5;
//DHT-------

void setup() {
  //DHT-------
    dht.begin();
  dht2.begin();
  //DHT-------
  Wire.begin();
  Serial.begin(9600);
  pinMode(pump, INPUT_PULLUP);
  pinMode(pump, OUTPUT);
  digitalWrite(pump,HIGH);

  pinMode(2, OUTPUT);
  digitalWrite(2, LOW); //Reset the Chirp
  delay(1); //maybe allow some time for chirp to reset
  digitalWrite(2, HIGH); //Go out from reset
  writeI2CRegister8bit(0x20, 3); //send something on the I2C bus
  delay(1000); //allow chirp to boot
}

void loop() {
    unsigned long currentMillis = millis();
  if(currentMillis - previousMillis > interval) {

    previousMillis = currentMillis;   
    
        //Read data and store it to variables hum and temp
    hum = dht.readHumidity();
    temp= dht.readTemperature();
        //Read data and store it to variables hum and temp
    hum2 = dht2.readHumidity();
    temp2= dht2.readTemperature();

    hum3= hum + hum2;
    
    temp3=temp + temp2;
    
    hum4= round(hum3);
    temp4 = round(temp3);
    
    hum5 = hum4 + 200;
  

  Serial.println(readI2CRegistepump6bit(0x20, 0)); //read capacitance register
 
    Serial.println(hum5 / 2);

    Serial.println(temp4 / 2);



  }
delay(1000);
int watering = 0;
if (20 < readI2CRegistepump6bit(0x20, 0)  && readI2CRegistepump6bit(0x20, 0)  < 350) {


   
 digitalWrite(pump,LOW);

delay(400000);

digitalWrite(pump,HIGH);

delay(1000);

 }
if (readI2CRegistepump6bit(0x20, 0) > 1500){


    Serial.println("799");
   delay (5000);





 }

}



