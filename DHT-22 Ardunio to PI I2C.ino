#include <Wire.h>
#include <dht.h>
#define SLAVE_ADDRESS 0x08
#define DHTdataPin 3 
byte number = 0;
dht DHT; // Creats a DHT object
void flash_data(int loops)
{ 
   for (int i = 0; i < loops; i++)
   {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(50);
      digitalWrite(LED_BUILTIN, LOW);
      delay(50);
   }
}

void flash_good(int loops)
{ 
   for (int i = 0; i < loops; i++)
   {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(20);
      digitalWrite(LED_BUILTIN, LOW);
      delay(20);
   }
}

void flash_bad( int loops ) {}

// callback for received data
void receiveData(int byteCount){
    if ( Wire.available() ) {
       number = Wire.read();
       Serial.println(number);
    }
}

void sendData() {
  int readData = DHT.read22(DHTdataPin); // Reads the data from the sensor
  float t = DHT.temperature; // Gets the values of the temperature
  float h = DHT.humidity; // Gets the values of the humidity
  String data1="DHT22:"+String(t)+":"+String(h)+":!!!";
  //String data1="DHT22:T"+String(t)+":H"+String(h)+":!!!";
  String test1="a";
  Serial.println(data1);
  //char string2[1]=test1;
  //char string1[30] = "T"+String(t)+"H"+String(h);
  //char string1[30] = "This is a string";
  //Serial.println(string1);
  //Wire.write(string1);  

  // Define 
String str = "This is my string"; 

// Length (with one extra character for the null terminator)
int str_len = data1.length() + 1; 

// Prepare the character array (the buffer) 
char char_array[str_len];

// Copy it over 
data1.toCharArray(char_array, str_len);
Wire.write(char_array);  






}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Wire.begin(SLAVE_ADDRESS); // an address makes this unit a Slave
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);  
  Serial.begin(9600);
}

void loop() {
  if ( number > 0 ) { // If the RPi is sending a value, flash it.
    flash_data(number);
    number = 0;
  } else {
    flash_good(1);
  }

  int readData = DHT.read22(DHTdataPin); // Reads the data from the sensor
  float t = DHT.temperature; // Gets the values of the temperature
  float h = DHT.humidity; // Gets the values of the humidity

  delay(1000);

}
