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
int victim_type = 1; //(1)or(8)=heated, (2)or(9)=H, (3)or(10)=S, (4)or(11)=U, (5)or(12)=Red, (6)or(13)=Yellow, (7)or(14)=Green

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
			victim_type = 2;
		}
		else if (MVLeftChar == Decode_S) {
			victim_type = 3;
		}
		else if (MVLeftChar == Decode_U) {
			victim_type = 4;
		}
		else if (MVLeftChar == Decode_Red) {
			victim_type = 5;
		}
		else if (MVLeftChar == Decode_Yellow) {
			victim_type = 6;
		}
		else if (MVLeftChar == Decode_Green) {
			victim_type = 7;
		}
		if (MVRightChar == Decode_H) {
			victim_type = 9;
		}
		else if (MVRightChar == Decode_S) {
			victim_type = 10;
		}
		else if (MVRightChar == Decode_U) {
			victim_type = 11;
		}
		else if (MVRightChar == Decode_Red) {
			victim_type = 12;
		}
		else if (MVRightChar == Decode_Yellow) {
			victim_type = 13;
		}
		else if (MVRightChar == Decode_Green) {
			victim_type = 14;
		}
	}
}
