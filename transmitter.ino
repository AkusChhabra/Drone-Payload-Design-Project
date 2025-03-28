#include <RH_ASK.h>
#ifdef RH_HAVE_HARDWARE_SPI
#include <SPI.h> // Not actually used but needed to compile
#endif
// (speed, receive pin, transmit pin, push-to-talk)
RH_ASK driver(1000, 4, 2, 0);
void setup()
{
Serial.begin(115200);
if (!driver.init())
Serial.println("init failed");

}
void loop()
{
driver.send((uint8_t *)msg, strlen(msg));
driver.waitPacketSent();
delay(200);
Serial.println("Sending Message");
Serial.println(driver.waitPacketSent());
}