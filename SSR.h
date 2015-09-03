#ifndef SSR_H
#define SSR_H

#define SSR_PIN 7

void SSRInit()
{
  digitalWrite(SSR_PIN, LOW);
}

void SSROn()
{
  digitalWrite(SSR_PIN, HIGH);
}

void SSROff()
{
  digitalWrite(SSR_PIN, LOW);
}


#endif
