int pulsePin = 0;                 
int blinkPin = 13;              
int fadePin = 5;               
int fadeRate = 0;                 


volatile int BPM;                   
volatile int Signal;                
volatile int IBI = 600;              
volatile boolean Pulse = false;     
volatile boolean QS = false;        


void setup(){
  pinMode(blinkPin,OUTPUT);         
  pinMode(fadePin,OUTPUT);         
  Serial.begin(9600);             
  interruptSetup();                 
    
}



void loop(){
  //sendDataToProcessing('S', Signal);     
  if (QS == true){                       
        fadeRate = 255;                
        sendDataToProcessing(BPM);   
        QS = false;                   
     }
  
  ledFadeToBeat();
  
  delay(20);                            


void ledFadeToBeat(){
    fadeRate -= 15;                         
    fadeRate = constrain(fadeRate,0,255);   
    analogWrite(fadePin,fadeRate);          
  }


void sendDataToProcessing( int data ){
    //Serial.print(symbol);               
    Serial.println(data);            
  }







