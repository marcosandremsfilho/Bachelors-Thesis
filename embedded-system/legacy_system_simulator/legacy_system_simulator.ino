const int RASP_DATA_PIN = 5; // This is the D1 pin but his respective GPIO is the 5
const int RASP_DATA_OUT = 0; // This is the D3 pin but his respective GPIO is the 0
const int IR_SENSOR = 4; // This is the D2 pin but his respective GPIO is the 4
const int PNEUMATIC_ACTUATOR = 2; // This is the D4 but his respective GPIO is the 2

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(RASP_DATA_PIN, INPUT);
  pinMode(IR_SENSOR, INPUT);
  pinMode(RASP_DATA_OUT, OUTPUT);
  pinMode(PNEUMATIC_ACTUATOR, OUTPUT);

  digitalWrite(LED_BUILTIN, LOW);

  Serial.begin(9600);
}

bool read_ir_sensor(){
  /*
    This function is used to invert the read data from the IR sensor. This sensor returns 0 if something is blocking
    otherwise return 1, to make easier to understand, this function invert this logic, turning 1 if something is blocking
  */
  int sensor_state = digitalRead(IR_SENSOR);

  if (sensor_state == LOW){
      return LOW;
  }
  return HIGH;
}

void system(){
  int state = digitalRead(RASP_DATA_PIN) ;
  
  if (state == HIGH){
    bool ir_sensor_state = read_ir_sensor();
    Serial.println(ir_sensor_state);
     if(read_ir_sensor()) {
        digitalWrite(RASP_DATA_OUT, HIGH);
        digitalWrite(PNEUMATIC_ACTUATOR, HIGH);
        digitalWrite(LED_BUILTIN, HIGH);
     } else {
        digitalWrite(RASP_DATA_OUT, LOW);
        digitalWrite(PNEUMATIC_ACTUATOR, LOW);
        digitalWrite(LED_BUILTIN, LOW);
     }
  }
}

void send_ir_sensor_status_to_rasp(){
  bool ir_sensor = read_ir_sensor();
  digitalWrite(RASP_DATA_OUT, ir_sensor);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  system();
}
