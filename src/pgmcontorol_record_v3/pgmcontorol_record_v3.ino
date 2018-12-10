#include <Arduino.h>

// digital out pins for solenoid valves
const int transistorPin1 = 6;
const int transistorPin2 = 8;
const int transistorPin3 = 10;
const int transistorPin4 = 12;

//Interrupt
const int drum_rightinput = 2;
const int drum_leftinput = 3;

static bool drum_rightstate = false;
static bool drum_leftstate = false;
static bool last_drum_rightstate = false;
static bool last_drum_leftstate = false;

static unsigned long last_time_left = 0;
static bool debounse_state_left = false;
static unsigned long last_time_right = 0;
static bool debounse_state_right = false;

bool flag_1 = false;
bool flag_2 = false;
bool flag_3 = false;
bool flag_4 = false;

byte command;

unsigned long starting_time;
unsigned long current_time;
unsigned long tmp_current_time;
const unsigned long period = 1000;

volatile unsigned long left_timing =  0;
volatile unsigned long  left_previous_timing = 0;
volatile unsigned long right_timing =  0;
volatile unsigned long   right_previous_timing = 0;


void setup(){
    Serial.begin(115200);

    //Add the PGM channels and start the control
    pinMode (transistorPin1, OUTPUT);
    pinMode (transistorPin2, OUTPUT);
    pinMode (transistorPin3, OUTPUT);
    pinMode (transistorPin4, OUTPUT);

    pinMode (drum_leftinput, INPUT);
    pinMode (drum_rightinput, INPUT);

    digitalWrite(transistorPin1, LOW);
    digitalWrite(transistorPin2, LOW);
    digitalWrite(transistorPin3, LOW);
    digitalWrite(transistorPin4, LOW);

    attachInterrupt(digitalPinToInterrupt(drum_leftinput), left_isr, RISING);
    attachInterrupt(digitalPinToInterrupt(drum_rightinput), right_isr, RISING);
    Serial.println("started");
}


bool leftFlag = false;
bool rightFlag = false;


void loop(){
    //float val_leftinput = analogRead(drum_leftinput);
    //float val_rightinput = analogRead(drum_rightinput);    

    /*
    if(drum_leftstate != last_drum_leftstate && drum_leftstate == true){
        Serial.println("HIT_LEFT:");
        drum_leftstate != drum_leftstate;
    }
    if(drum_rightstate != last_drum_rightstate && drum_rightstate == true){
        Serial.println("HIT_RIGHT:");  
        drum_rightstate != drum_rightstate;
    }
    */
    
    //last_drum_leftstate = drum_leftstate;
    //last_drum_rightstate = drum_rightstate;

    if(leftFlag){
        leftFlag = false;

            Serial.print("HIT_LEFT:");
            Serial.println(left_timing);
    }

    if(rightFlag){
        rightFlag = false;

            Serial.print("HIT_RIGHT:");
            Serial.println(right_timing);
    }



    if(Serial.available() > 0){
        String command = Serial.readStringUntil('\n');
        Serial.println("\tUSB: received command: " + String(command));
        command.trim();
        switch(command.toInt()){
            case 1: 
                if(flag_1){
                    digitalWrite(transistorPin1, LOW);
                }
                else digitalWrite(transistorPin1, HIGH);
                flag_1 = !flag_1;
                break;
            case 2: 
                if(flag_2){
                    digitalWrite(transistorPin2, LOW);
                }
                else digitalWrite(transistorPin2, HIGH);
                flag_2 = !flag_2;
                break;
            case 3: 
                if(flag_3){
                    digitalWrite(transistorPin3, LOW);
                }
                else digitalWrite(transistorPin3, HIGH);
                flag_3 = !flag_3;
                break;
            case 4: 
                if(flag_4){
                    digitalWrite(transistorPin4, LOW);
                }
                else digitalWrite(transistorPin4, HIGH);
                flag_4 = !flag_4; 
                break;
        }    
    }
    //delay(10);
}

void left_isr() {
    if((millis() - left_previous_timing) > 150){
        left_timing = millis();
        left_previous_timing = left_timing;

        leftFlag = true;

        //Serial.print("left:");
        //Serial.println(left_timing);
    }
}

void right_isr() {
    if((millis() - right_previous_timing) > 150){
        right_timing = millis();
        right_previous_timing = right_timing;

        rightFlag = true;

        //Serial.print("right:");
        //Serial.println(left_timing);
    }
}