#include <OneWire.h>
#include <DallasTemperature.h>


#define ONE_WIRE_BUS A0

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);

uint8_t ** addresses;
uint8_t nAddresses;
DeviceAddress target;
float temperature;

void setupSensors(void)
{
  nAddresses = sensors.getDeviceCount();
  addresses = (uint8_t**)malloc(sizeof(uint8_t *) * nAddresses);
  for(uint8_t i = 0; i < nAddresses; i++)
  {
    addresses[i] = (uint8_t*)malloc(sizeof(DeviceAddress));
    sensors.getAddress(addresses[i], i);
  }

}

void setup(void)
{
  // start serial port
  Serial.begin(9600);

  // Start up the library
  sensors.begin();
  setupSensors();
}

union{
  byte asBytes[4];
  float asFloat;
} FloatBytes;

void setTemperature()
{
  for(int8_t i = 0; i < 4; ++i)
  {
    while((FloatBytes.asBytes[i] = Serial.read()) == -1);
  }
  temperature = FloatBytes.asFloat;
  Serial.println(temperature);
}

void setTarget()
{
  for(int8_t i = 0; i < 8; ++i)
  {
    while((target[i] = Serial.read()) == -1);
  }
  for(uint8_t j = 0; j<8; j++)
  {
    Serial.print("0x");
    Serial.print(target[j], HEX);
    Serial.print(" ");
  }
  Serial.println();
}

void printTemps()
{
  sensors.requestTemperatures(); // Send the command to get temperatures
  Serial.println(nAddresses);
  for(uint8_t i = 0; i < nAddresses; i++)
  {
    for(uint8_t j = 0; j<8; j++)
    {
      Serial.print("0x");
      Serial.print(addresses[i][j], HEX);
      Serial.print(" ");
    }
    Serial.println();
    Serial.println(sensors.getTempC(addresses[i]));
  }
  Serial.flush();
}


void loop(void)
{ 
  switch(Serial.read())
  {
    case 1:
      printTemps();
      break;
    case 2:
      setTemperature();
      break;
    case 3:
      setTarget();
    break;
    case -1:
       delay(500);
       break;
  }
}
