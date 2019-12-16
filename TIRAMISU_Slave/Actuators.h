#include <Servo.h>
#define SwitchPin 0
#define DeployerPin 0
Servo Deployer;
#define motorUR 0
#define motorURdirA 0
#define motorURdirB 0
#define motorLR 0
#define motorLRdirA 0
#define motorLRdirB 0
#define motorUL 0
#define motorULdirA 0
#define motorULdirB 0
#define motorLL 0
#define motorLLdirA 0
#define motorLLdirB 0
#define LDriverSTDBY 0
#define RDriverSTDBY 0
int SpeedLeft=0;
int SpeedRight=0;
#define Kp 4

void MotorsRelease() {
  analogWrite(motorUL, 0);
  analogWrite(motorUR, 0);
  analogWrite(motorLL, 0);
  analogWrite(motorLR, 0);
	digitalWrite(motorULdirA, LOW);
	digitalWrite(motorULdirB, LOW);
	digitalWrite(motorURdirA, LOW);
	digitalWrite(motorURdirB, LOW);
	digitalWrite(motorLLdirA, LOW);
	digitalWrite(motorLLdirB, LOW);
	digitalWrite(motorLRdirA, LOW);
	digitalWrite(motorLRdirB, LOW);
}

void MotorsStop() {
	digitalWrite(motorULdirA, HIGH);
	digitalWrite(motorULdirB, HIGH);
	digitalWrite(motorURdirA, HIGH);
	digitalWrite(motorURdirB, HIGH);
	digitalWrite(motorLLdirA, HIGH);
	digitalWrite(motorLLdirB, HIGH);
	digitalWrite(motorLRdirA, HIGH);
	digitalWrite(motorLRdirB, HIGH);
}

void ActuatorsInitialize() {
	Deployer.attach(DeployerPin);
	Deployer.write(75);
	pinMode(LDriverSTDBY, HIGH);
	pinMode(RDriverSTDBY, HIGH);
	pinMode(motorUL, OUTPUT);
	pinMode(motorULdirA, OUTPUT);
	pinMode(motorULdirB, OUTPUT);
	pinMode(motorLL, OUTPUT);
	pinMode(motorLLdirA, OUTPUT);
	pinMode(motorLLdirB, OUTPUT);
	pinMode(motorUR, OUTPUT);
	pinMode(motorURdirA, OUTPUT);
	pinMode(motorURdirB, OUTPUT);
	pinMode(motorLR, OUTPUT);
	pinMode(motorLRdirA, OUTPUT);
	pinMode(motorLRdirB, OUTPUT);
	MotorsRelease();
}

void URForward() {
	digitalWrite(motorURdirA, HIGH);
	digitalWrite(motorURdirB, LOW);
}

void URBackwards() {
	digitalWrite(motorURdirA, LOW);
	digitalWrite(motorURdirB, HIGH);
}

void ULForward() {
	digitalWrite(motorULdirA, HIGH);
	digitalWrite(motorULdirB, LOW);
}

void ULBackwards() {
	digitalWrite(motorULdirA, LOW);
	digitalWrite(motorULdirB, HIGH);
}

void LRForward() {
	digitalWrite(motorLRdirA, HIGH);
	digitalWrite(motorLRdirB, LOW);
}

void LRBackwards() {
	digitalWrite(motorLRdirA, LOW);
	digitalWrite(motorLRdirB, HIGH);
}

void LLForward() {
	digitalWrite(motorLLdirA, HIGH);
	digitalWrite(motorLLdirB, LOW);
}

void LLBackwards() {
	digitalWrite(motorLLdirA, LOW);
	digitalWrite(motorLLdirB, HIGH);
}


void Move(int pwm_l, int pwm_r) {
	if (pwm_l > 0) {
		ULForward();
		LLForward();
	} else {
		ULBackwards();
		LLBackwards();
	}
	if (pwm_r > 0) {
		URForward();
		LRForward();
	} else {
		URBackwards();
		LRBackwards();
	}
	analogWrite(motorUL, abs(pwm_l));
	analogWrite(motorLL, abs(pwm_l));
	analogWrite(motorUR, abs(pwm_r));
	analogWrite(motorLR, abs(pwm_r));
}

void AvoidLeft() {
  Move(-200, 200);
  delay(50);
  Move(-200, -200);
  delay(50);
  Move(200, -200);
  delay(70);
  Move(200, 200);
  delay(50);
}

void AvoidRight() {
  Move(200, -200);
  delay(50);
  Move(-200, -200);
  delay(50);
  Move(-200, 200);
  delay(70);
  Move(200, 200);
  delay(50);
}

void DeployKit() {
	Deployer.write(145);
	delay(400);
	Deployer.write(60);
	delay(300);
	Deployer.write(75);
	delay(300);
}
