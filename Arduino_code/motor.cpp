

void motorMovement(int pinOne, int pinTwo, int pinThree, int pinFour){
    int frequency = 375000; //WE NEED TO CALCULATE THE PROPER FREQUENCY

    analogWrite(pinOne, frequency);
    analogWrite(pinTwo, frequency);
    analogWrite(pinThree, frequency);
    analogWrite(pinFour, frequency);

}