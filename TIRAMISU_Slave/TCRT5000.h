#define ReflectionPin A0
#define TrapLimit 800
float Reflect = 100;
bool OnBlackTile = false;

void TCRT5000Initialize() {
	pinMode(ReflectionPin, INPUT);
}

void ReadReflection() {
  	Reflect = (analogRead(ReflectionBPin) * 0.5) + (Reflect * 0.5);
	OnBlackTile = false;
	if (Reflect >= TrapLimit) {
		OnBlackTile = true;
	}
}
