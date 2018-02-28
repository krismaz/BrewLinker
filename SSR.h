#ifndef SSR_h
#define SSR_h

#define SSR_PINa 49
#define SSR_PINb 51
#define SSR_PINc 53

#define LED_PINa 22
#define LED_PINb 24
#define LED_PINc 26
#define LED_PINd 28
#define LED_PINe 30


#define PUMP_PIN 11

inline void SSRInit()
{
  pinMode(SSR_PINa, OUTPUT);
  pinMode(SSR_PINb, OUTPUT);
  pinMode(SSR_PINc, OUTPUT);

  pinMode(LED_PINa, OUTPUT);
  pinMode(LED_PINb, OUTPUT);
  pinMode(LED_PINc, OUTPUT);
  pinMode(LED_PINd, OUTPUT);
  pinMode(LED_PINe, OUTPUT);

  digitalWrite(SSR_PINa, LOW);
  digitalWrite(SSR_PINb, LOW);
  digitalWrite(SSR_PINc, LOW);
}

inline void SSROn()
{ 
  digitalWrite(SSR_PINa, HIGH);
  digitalWrite(SSR_PINb, HIGH);
  digitalWrite(SSR_PINc, HIGH);  

  digitalWrite(LED_PINa, HIGH);
  digitalWrite(LED_PINb, HIGH);
  digitalWrite(LED_PINc, HIGH);
  digitalWrite(LED_PINd, HIGH);
  digitalWrite(LED_PINe, HIGH);
}

inline void SSROff()
{
  digitalWrite(SSR_PINa, LOW);
  digitalWrite(SSR_PINb, LOW);
  digitalWrite(SSR_PINc, LOW);

  digitalWrite(LED_PINa, LOW);
  digitalWrite(LED_PINb, LOW);
  digitalWrite(LED_PINc, LOW);
  digitalWrite(LED_PINd, LOW);
  digitalWrite(LED_PINe, LOW);

}

inline void SSRPhase(float diff)
{ 
  SSROff();
  if(diff > 2.0f)
  {
    digitalWrite(SSR_PINa, HIGH);
    digitalWrite(SSR_PINb, HIGH);
    digitalWrite(SSR_PINc, HIGH); 
    digitalWrite(LED_PINa, HIGH);
  } else if (diff > 1.5f){
    digitalWrite(SSR_PINb, HIGH);
    digitalWrite(SSR_PINc, HIGH);
    digitalWrite(LED_PINb, HIGH);
  } else if (diff > 1.0f){
    digitalWrite(SSR_PINa, HIGH);
    digitalWrite(SSR_PINb, HIGH);
    digitalWrite(LED_PINc, HIGH);
  } else if (diff > 0.5f){
    digitalWrite(SSR_PINc, HIGH);
    digitalWrite(LED_PINd, HIGH);
  } else {
    digitalWrite(SSR_PINb, HIGH);
    digitalWrite(LED_PINe, HIGH);
  }
}


inline void PumpOn()
{
  digitalWrite(PUMP_PIN, HIGH);
}

inline void PumpOff()
{
  digitalWrite(PUMP_PIN, LOW);
}

#endif
