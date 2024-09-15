#include<Servo.h>

static const int SERIAL_BAUD_RATE = 9600;

static const int TRIGGER_PIN = 2;
static const int ECHO_PIN = 3;
static const int SERVO_CONTROL_PIN = 4;

static const int RADAR_HORIZONTAL_ROTATION_ANGLE = 90;
static const float RADAR_MAX_DETECT_DISTANCE_CM = 200;
static const float SPEED_OF_SOUND = 29.1;

static Servo servo;
static int servoAngle = 0;
static bool servoIsRotatingClockWise = false;

static void rotate_servo()
{
    servoAngle = servoIsRotatingClockWise ? servoAngle + 1 : servoAngle - 1;
    servo.write(servoAngle);

    if(servoIsRotatingClockWise && servoAngle > RADAR_HORIZONTAL_ROTATION_ANGLE)
    {
      servoIsRotatingClockWise = false;
    }

    if(!servoIsRotatingClockWise && servoAngle < 0)
    {
      servoIsRotatingClockWise = true;
    }
}

void setup() 
{
    pinMode(TRIGGER_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    pinMode(SERVO_CONTROL_PIN, OUTPUT);

    servo.attach(SERVO_CONTROL_PIN);
    Serial.begin(SERIAL_BAUD_RATE);
}

void loop() 
{
    digitalWrite(TRIGGER_PIN, LOW);
    delayMicroseconds(5);
    digitalWrite(TRIGGER_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGER_PIN, LOW);

    const float timeout = RADAR_MAX_DETECT_DISTANCE_CM * SPEED_OF_SOUND * 2.0;
    const float duration = pulseIn(ECHO_PIN, HIGH, timeout);
    const float distance = duration > 0.0 ? (duration / 2.0) / 29.1 : RADAR_MAX_DETECT_DISTANCE_CM;

    Serial.print(servoAngle);
    Serial.print(',');
    Serial.print(distance);
    Serial.print("\n");
    Serial.flush();

    rotate_servo();

    delay(15);
}
