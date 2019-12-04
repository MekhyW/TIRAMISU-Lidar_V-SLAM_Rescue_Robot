#define Decode_H 72
#define Decode_S 83
#define Decode_U 85
#define Decode_Red 82
#define Decode_Yellow 89
#define Decode_Green 71
#define Decode_n 110
int MVLeftChar = 0;
int MVRightChar = 0;
bool Victim = false;
int VictimType = 1; //(1)or(8)=heated, (2)or(9)=H, (3)or(10)=S, (4)or(11)=U, (5)or(12)=Red, (6)or(13)=Yellow, (7)or(14)=Green

void OpenMVSerialInitialize() {
	Serial1.begin(9600);
	Serial3.begin(9600);
}

void ReadCams() {
	while (Serial1.available()) {
		MVLeftChar = Serial1.read();
	}
	while (Serial3.available()) {
		MVRightChar = Serial3.read();
	}
	Victim = false;
	if (MVLeftChar == Decode_H || MVLeftChar == Decode_S || MVLeftChar == Decode_U || MVLeftChar == Decode_Red || MVLeftChar == Decode_Yellow || MVLeftChar == Decode_Green || MVRightChar == Decode_H || MVRightChar == Decode_S || MVRightChar == Decode_U || MVRightChar == Decode_Red || MVRightChar == Decode_Yellow || MVRightChar == Decode_Green) {
		Victim = true;
		if (MVLeftChar == Decode_H) {
			VictimType = 2;
		}
		else if (MVLeftChar == Decode_S) {
			VictimType = 3;
		}
		else if (MVLeftChar == Decode_U) {
			VictimType = 4;
		}
		else if (MVLeftChar == Decode_Red) {
			VictimType = 5;
		}
		else if (MVLeftChar == Decode_Yellow) {
			VictimType = 6;
		}
		else if (MVLeftChar == Decode_Green) {
			VictimType = 7;
		}
		if (MVRightChar == Decode_H) {
			VictimType = 9;
		}
		else if (MVRightChar == Decode_S) {
			VictimType = 10;
		}
		else if (MVRightChar == Decode_U) {
			VictimType = 11;
		}
		else if (MVRightChar == Decode_Red) {
			VictimType = 12;
		}
		else if (MVRightChar == Decode_Yellow) {
			VictimType = 13;
		}
		else if (MVRightChar == Decode_Green) {
			VictimType = 14;
		}
	}
}
