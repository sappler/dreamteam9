#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <wiringPi.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>

#include <errno.h>
#include "time.h"

int main(){
	int time, alarm, manual;
	int state, brightness;
	printf("%s\n", __TIME__);
	//Parse_Parameters( time, alarm, manual);
	printf("Total_time: %d\n",Parse_InputTime());
	printf("Alarm: %d\n",Parse_Alarm());
	printf("Manual: %d\n",Parse_Manual());
}
