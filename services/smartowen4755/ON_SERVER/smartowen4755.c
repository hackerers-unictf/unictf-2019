#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>

static const char* PASSWORD = "47ThIsIsNotATr0ll55";
static const char* USERNAME = "THIS_IS_THE_USERNAME";
char* PREMENU = "\
       ________ ___      ___      __       _______ ___________            ______   __   __  ___  _______ _____  ___          ___  ___ _________   ________ ________  \n\
      /^       )^  \\    /^  |    /^^\\     /^      (^     _   ^)          /    ^ \\ |^  |/  \\|  ^|/^     ^(\\^   \\|^  \\        (: ^||_  (^       ^\\ /^      ^)^      ^) \n\
     (:   \\___/ \\   \\  //   |   /    \\   |:        )__/  \\__/          // ____  \\|'  /    \\:  (: ______).\\   \\    |       |  (__) :|\\___/   :/(:   //\\_(:   //\\_/  \n\
      \\___  \\   /\\  \\/.    |  /' /\\  \\  |_____/   )  \\_ /            /  /    ) :): /'        |\\/    | |: \\.   \\  |        \\____  ||   /   //  \\___ \\   \\___ \\     \n\
       __/  \\ |: \\.        | //  __'  \\  //      /   |.  |           (: (____/ // \\//  /\'    |// ___)_|.  \\    \\. |            _\\ '| __\\  ./   __ | \\  __ | \\    \n\
      /^ \\   :)|.  \\    /:  |/   /  \\  \\|:  __   \\   \\:  |            \\        /  /   /  \\\\   (:      ^|    \\    \\ |           /^ \\_|(:  \\_/ \\ /^ \\/  :)/^ \\/  :)   \n\
     (_______/ |___|\\__/|___(___/    \\___)__|  \\___)   \\__|             \\^_____/  |___/    \\___|\\_______)\\___|\\____\\)          (_______)_______|_______/(_______/    \n\
                                                                                                                                                                     \n\
\n\n\
Welcome Guest, TheHawk gives the opportunity to use\n\
this fantastic SmartOwen4755 producted by uniCTf in collaboration\n\
with CUTTER!! Your food won't ever been ready so fast!\n";

char* MENU = "\
0) Exit\n\
1) Open/Close The Door\n\
2) Insert food\n\
3) Set temperature\n\
4) Set fan On/OFF\n\
5) Set Power\n\
6) Set seconds\n\
7) Start\n\
8) Remove Food\n\
9) Print State\n\
>";

int autentication = 0;

struct state {
	int door; //BOOLEAN
	int food; //BOOLEAN
	char food_type[64];
	int temperature; //MAX 255
	int fan; //BOOLEAN
	int power; //0 = nothing 1 = min 2 = med 3 = max
	long time; //time(0) when started
	int seconds;
	int started; //boolean
}; typedef struct state state;

void print_state(state a)
{
	puts("State of the Owen:");
	if(a.door == 0)
		puts("Door Closed");
	else
		puts("Door Open");
	
	if(a.food == 1)
		printf("Food Inside: %s", a.food_type);
	else
		puts("No Food inside");
	
	printf("Temperature setted on: %d\n", a.temperature);
	
	if(a.fan == 0)
		puts("Fan Disabled");
	else
		puts("Fan Enabled");
	
	if(a.power == 0)
		puts("Power OFF");
	else if(a.power == 1)
		puts("Power: Low");
	else if(a.power == 2)
		puts("Power: Medium");
	else
		puts("Power: Max");

	if(a.started == 0 || a.seconds == 0)
		puts("Stopped");

	if(a.seconds != 0)
		printf("Setted for: %d", a.seconds);
}

int check_autentication(char* username, char* password)
{
	int x = 43;
	int y = 23;
	int c = 768;
	int u = 12;
	char *fuffa = "mYG0dThiSiSmYPasswd";
	int result = 0;
	if(x == 43)
	{
		if(strcmp(fuffa, "mYG0dThiSiSmYPasswd") == 0)
		{
			u += 10;
			u += 21;
			x += u;
			u = 12;
			if((char)x == (char)x)
			{
				x << 1;
				y += 325;
				y = u + 11;
				if(c * 12 == u * 768)
				{	if(u == y - 11)
					{
						if(strcmp(password, PASSWORD) == 0) //I CONTROLLI DI SOPRA SONO TUTTI FUFFA
						{
							result += 1;
							if(strcmp(username, USERNAME) == 0)
							{
								result += 1;
								if(u == u)
									if(x*y == y*x)
										return 1; //USERNAME E PW GIUSTI
									else
										result = -1;
								else
									result = -2;
							}
							else
								return 0; //USERNAME ERRATO
						}
						else
							return 2; //PASSWORD ERRATA
					}
					else
						result = -4;
				}
				else
					result = -5;
			}
			else
				result = -6;
		}
		else
			result = -7;
	}
	if (result < 0)
	{
		if(strcmp(password, PASSWORD) == 0)
			if(strcmp(username, USERNAME) == 0)
				return 1;
	}
	return result;
}

void smartOwen()
{
	char admpath[5]; 
	admpath[0] = 0x48;
	admpath[1] = 0x61;
	admpath[2] = 0x77; 
	admpath[3] = 0x6b;
	admpath[4] = 0x00;
  	FILE *adm_todo = fopen(admpath, "r");
  	if (adm_todo != NULL)
  	{
    	char line [58];
    	while (fgets(line, sizeof line, adm_todo) != NULL)
    		fputs (line, stdout);
    	fclose (adm_todo);
  	}
  	else
    	puts("Failed");
}

int autenticate()
{
	char username[64];
	char password[64];
	puts("Insert your username");
	fflush(stdout);
	fgets(username, 64, stdin);
	int ch;
	//if(!strchr(username, '\n'))
		//while((ch = getchar()) != EOF && ch != '\n') {}
	username[strlen(username)-1] = '\0';
	puts("Insert your password");
	fflush(stdout);
	fgets(password, 64, stdin);
	//if(!strchr(password, '\n'))
	//	while((ch = getchar()) != EOF && ch != '\n') {}
	password[strlen(password)-1] = '\0';
	return autentication = check_autentication(username, password);
}

void switch_door(state *a)
{
	if(a->door == 0)
	{
		a->door = 1;
		puts("Door Opened");
	}
	else
	{
		a->door = 0;
		puts("Door Closed");
	}
}

void insert_food(state *a)
{
	if(a->door == 0)
	{
		puts("Damn, the door is closed");
		return;
	}
	puts("Give me the food");
	fflush(stdout);
	fgets(a->food_type, 64, stdin);
	int ch;
	//if(!strchr(a->food_type, '\n'))
	//	while((ch = getchar()) != EOF && ch != '\n') {}
	a->food = 1;
}

void remove_food(state *a)
{
	a->food = 0;
	memset(a->food_type, 0, 64);
}


void set_temperature(state *a)
{
	puts("Give me the temperature 0-255 Celsius");
	fflush(stdout);
	char buf[8];
	fgets(buf, 8, stdin);
	int ch;
	//if(!strchr(buf, '\n'))
	//	while((ch = getchar()) != EOF && ch != '\n') {}
	a->temperature = atoi(buf);
	if(a->temperature > 255)
		a->temperature = 255;
	else if(a->temperature < 0)
		a->temperature = 0;
}

void switch_fan(state *a)
{
	if(a->fan == 0)
	{
		a->fan = 1;
		puts("Fan Started");
	}
	else
	{
		a->fan = 0;
		puts("Fan Stopped");
	}
}

void set_power(state *a)
{
	puts("Choose\n0) Shutdown\n1) Low\n2) Med\n3) Max");
	fflush(stdout);
	char buf[8];
	fgets(buf, 8, stdin);
	int ch;
	//if(!strchr(buf, '\n'))
	//	while((ch = getchar()) != EOF && ch != '\n') {}
	while(atoi(buf) < 0 || atoi(buf) > 3)
	{
		puts("Choose Better");
		fflush(stdout);
		fgets(buf, 8, stdin);
		//if(!strchr(buf, '\n'))
		//	while((ch = getchar()) != EOF && ch != '\n') {}
	}
	if(atoi(buf) == 3)
	{
		puts("Oh, For this you've to autenticate yourself");
		fflush(stdout);
		autenticate();
		if(autentication == 1)
		{
			puts("Success");
			a->power = atoi(buf);
		}
		else if (autentication < 0)
		{
			puts("It's wrong man, setted power to medium");
			a->power = 2;
			puts("A patcher done a bad work");
		}
		else
		{
			puts("It's wrong man, setted power to medium");
			a->power = 2;
		}
	}
	else
		a->power = atoi(buf);
}

void set_seconds(state *a)
{
	puts("Give me the seconds: 0-10");
	fflush(stdout);
	char buf[8];
	fgets(buf, 8, stdin);
	int ch;
	//if(!strchr(buf, '\n'))
	//	while((ch = getchar()) != EOF && ch != '\n') {}
	a->seconds = atoi(buf);
	if(a->seconds > 10)
	{
		puts("Too Much seconds, setted to 10");
		a->seconds = 10;
	}
	if(a->seconds < 0)
		a->seconds = 0;
}

void start(state *a)
{
	if(a->started != 0)
	{
		puts("Its started yet");
		return;
	}
	if(a->door == 0 && a->temperature > 0 && a->power > 0 && a->seconds > 0)
	{
		a->started = 1;
		puts("Started");
		a->time = time(0);
		while(a->time+a->seconds > time(0))
		{
			sleep(1);
			printf("Remaining: %ld\n", a->time+a->seconds-time(0));
		}
		puts("Finished");
		a->started = 0;
		a->power = 0;
		a->seconds = 0;
		if(autentication == 1)
			smartOwen();
	}
	else
		puts("Something goes wrong man");
	print_state(*a);
}


int main(int argc, char **argv)
{
	int choose = 9;
	char buf[8] = "";
	state a;
	a.door = 0;
	a.food = 0;
	a.food_type[0] = '\0';
	a.temperature = 0;
	a.fan = 0;
	a.power = 0;
	a.time = 0;
	a.seconds = 0;
	a.started = 0;

	puts(PREMENU);
	while(choose != 0)
	{
		puts(MENU);
		fflush(stdout);
		fgets(buf, 8, stdin);
		choose = atoi(buf);
		
		switch(choose)
		{
			case 0:
				return 0;
			case 1:
				switch_door(&a);
				break;
			case 2:
				insert_food(&a);
				break;
			case 3:
				set_temperature(&a);
				break;
			case 4:
				switch_fan(&a);
				break;
			case 5:
				set_power(&a);
				break;
			case 6:
				set_seconds(&a);
				break;
			case 7:
				start(&a);
				break;
			case 8:
				remove_food(&a);
				break;
			case 9:
				print_state(a);
				break;
			default:
				break;
		}
	}
	return 1;
}
