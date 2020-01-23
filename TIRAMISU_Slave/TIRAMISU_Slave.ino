//TIRAMISU Robot - SLAVE
#include <Wire.h>
#include <string>
#include "OpenMVH7.h"
#include "MLX90614.h"
#include "TCRT5000.h"
#include "Actuators.h"
int Command;
int LastCommand;
int MoveError = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  ActuatorsInitialize();
  MLX90614Initialize();
  OpenMVSerialInitialize();
  TCRT5000Initialize();
  pinMode(SwitchPin, INPUT_PULLUP);
}

// FOR WRITING: 20=Standby, 21=Running, [1, 14]=Victim, 99=BlackTile
// FOR READING: [0, 180]=AngleError, 200=Stop, 201=AvoidLeft, 202=AvoidRight, 251=DeployKit, 252=DeployTwoKits

void loop() {
  ReadReflection();
  ReadTemperature();
  ReadCams();
  if(digitalRead(23)==LOW){
    MotorsStop();
    while(digitalRead(23)==LOW){
      Serial.println(20);
      MotorsRelease(); 
    }
  } else if(OnBlackTile==true){
    Serial.println(99);
    while(OnBlackTile==true){
      Move(-200, -200);
      ReadReflection();  
    }
  } else if(Victim==true){
    Serial.println(victim_type);
  } else {
    Serial.println(21);
  }
  if(Serial.available()){
    while(Serial.available()){
      Command = Serial.read();
    }
    if(Command != LastCommand){
      if(Command==200){
        MotorsStop();
      } else if(Command==252){
        DeployKit();
        DeployKit();
      } else if(Command==251){
        DeployKit();
      } else if(Command==201){
        AvoidLeft();
      } else if(Command==202){
        AvoidRight();
      } else if(Command>=0 && Command<=180 && OnBlackTile==false){
      	MoveError = ((Command-90)*0.5) + (MoveError*0.5);
      	if(MoveError < (-30)){
      		Move(200, -200)
      	} else if(MoveError > 30){
      		Move(-200, 200)
      	} else {
      		Move(constrain(200-(MoveError*Kp), 0, 200), constrain(200+(MoveError*Kp), 0, 200));
      	}
      }
    }
    LastCommand = Command;
  }
}
