#include <OneWire.h>
#include <DallasTemperature.h>
#include "SSR.h"

#define ONE_WIRE_BUS A0

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);

uint8_t ** addresses;
uint8_t nAddresses;
DeviceAddress target;
float temperature = -1000000.00;

void setupSensors(void)
{
  nAddresses = sensors.getDeviceCount();
  addresses = (uint8_t**)malloc(sizeof(uint8_t *) * nAddresses);
  for(uint8_t i = 0; i < nAddresses; i++)
  {
    addresses[i] = (uint8_t*)malloc(sizeof(DeviceAddress));
    sensors.getAddress(addresses[i], i);
  }
  for(uint8_t j = 0; j < nAddresses; j++)
  {
    target[j] = 0x00;
  }

}

void setup(void)
{
  SSRInit();

  // Start up the library
  sensors.begin();
  setupSensors();
  
  // start serial port
  Serial.begin(9600);
}

union{
  byte asBytes[4];
  float asFloat;
} FloatBytes;

void setTemperature()
{
  while(Serial.available()<4) delay(50);  
  for(int8_t i = 0; i < 4; ++i)
  {
    FloatBytes.asBytes[i] = Serial.read();
  }
  temperature = FloatBytes.asFloat;
  Serial.println(temperature);
}

void setTarget()
{
  while(Serial.available()<8) delay(50);  
  for(int8_t i = 0; i < 8; ++i)
  {
    target[i] = Serial.read();
  }
  for(uint8_t j = 0; j<8; ++j)
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

void cycle()
{
  
  if(sensors.validAddress(target))
  {
    float diff = temperature - sensors.getTempC(target);
    if(diff > 0.0f)
    {
      //SSROn();
      SSRPhase(diff);
    } else {
      SSROff(); 
    }
  } else {
    SSROff(); 
  }
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
    case 4:
      PumpOn();
    break;
    case 5:
      PumpOff();
    break;
    case -1:
       delay(500);
       break;
  }
  cycle();
}
