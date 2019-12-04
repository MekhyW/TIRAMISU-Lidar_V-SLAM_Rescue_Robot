//TIRAMISU Robot - Slave
//Version: 1.0
#include <Wire.h>
#include <string>
#include "OpenMVH7.h"
#include "MLX90614.h"
#include "TCRT5000.h"
#include "Actuators.h"
String Command;
String LastCommand;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  ActuatorsInitialize();
  MLX90614Initialize();
  OpenMVSerialInitialize();
  TCRT5000Initialize();
  pinMode(SwitchPin, INPUT_PULLUP);
}

void loop() {
  ReadReflection();
  ReadTemperature();
  ReadCams();
  if(OnBlackTile==true){
    Serial.println("BLACKTILE");
    while(OnBlackTile==true){
      Move(-200, -200);
      ReadReflection();  
    }
  } else if(Victim==true){
    Serial.println(VictimType);
  } else if(digitalRead(23)==LOW){
    MotorsStop();
    while(digitalRead(23)==LOW){
      Serial.println("STANDBY");
      MotorsRelease(); 
    }
  } else {
    Serial.println("RUNNING");
  }
  if(Serial.available()){
    while(Serial.available()){
      Command = Serial.readString(); 
    }
    if(Command != LastCommand){
      if(Command=="STOP"){
        MotorsStop();
      } else if(Command=="DEPLOYTWOKITS"){
        DeployKit();
        DeployKit();
      } else if(Command=="DEPLOYKIT"){
        DeployKit();
      } else if(Command=="AVOIDLEFT"){
        AvoidLeft();
      } else if(Command=="AVOIDRIGHT"){
        AvoidRight();
      } else if(OnBlackTile==false){
        if(Command==0){
          SpeedLeft = 0;
          SpeedRight = 0;
        } else if(Command>0 && Command<=255){
          SpeedLeft = Command; 
        } else if(Command>255 && Command<=510){
          SpeedRight = Command-255;
        }
        Move(SpeedLeft, SpeedRight);
      }
    }
    LastCommand = Command;
  }
}
