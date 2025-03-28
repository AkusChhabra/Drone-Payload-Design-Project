#include <RH_ASK.h>
#ifdef RH_HAVE_HARDWARE_SPI
#include <SPI.h> // Not actually used but needed to compile
#endif
//#include <ServoTimer2.h>
//#include <PWMServo.h>
//#include <Servo.h>
//Servo servo1;
//PWMServo servo1;
//ServoTimer2 servo1;
int servoPin = 3;
// (speed, receive pin, transmit pin, push-to-talk)
RH_ASK driver(1000, 2, 4, 0);

void setup() {
Serial.begin(115200);
//servo1.attach(servoPin);
if (!driver.init())
Serial.println("init failed");
analogWrite(servoPin, 0);
pinMode(servoPin, OUTPUT);
// servo1.write(0);
}
void loop() {
uint8_t buf[RH_ASK_MAX_MESSAGE_LEN];
uint8_t buflen = sizeof(buf);

if (driver.recv(buf, &buflen)) {
driver.printBuffer("Got:", buf, buflen); // Message with a good
checksum received, dump it.
String rcv;
for (int i = 0; i < buflen; i++) {
rcv += (char)buf[i];
}
Serial.println(rcv);
if (rcv == "DROP") {
Serial.println("Inside loop Receiver");
analogWrite(servoPin, 50);
delay(1000);
analogWrite(servoPin, 200);
delay(1000);
//analogWrite(servoPin, 230);
//delay(1000);
}
}
}