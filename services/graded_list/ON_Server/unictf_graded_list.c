#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>

struct grad_line {
	char name[16];
	char surname[16];
	unsigned int score;
}; typedef struct grad_line grad_line;

grad_line grad_list[587];

const char *Banner = "\
                 _  ___ _____ __    ___             _        _   _    _    _   \n\
       _  _ _ _ (_)/ __|_   _/ _|  / __|_ _ __ _ __| |___ __| | | |  (_)__| |_ \n\
      | || | ' \\| | (__  | ||  _| | (_ | '_/ _` / _` / -_) _` | | |__| (_-<  _|\n\
       \\_,_|_||_|_|\\___| |_||_|    \\___|_| \\__,_\\__,_\\___\\__,_| |____|_/__/\\__|\n\
\n";                                                                               
 
int string_is_alpha(const char *s) {
	for (; *s; s++) {
		if (!isalpha(*s))
	  		return -1;
	}
	return 0;
}

int get_position(int score)
{
	for(int i = 0; i < 583; i++)
	{
		if(score >= grad_list[i].score)
			return i+1;
	}
	return 584;
}

void read_v_line()
{
	char str_brut[65] = {0};
	char M = 'M', m = 'm', h = 'h', comma = ',', space = ' ';
	char p = 'p', u = 'u', z = 'z', l='l', e='e', d='d', escpoint = '!';
	char G = 'G', i='i', o='o', c= 'c', f='f', r='r', a= 'a', s= 's', v = 'v';
	char n='n', H='H', t = 't';
	sprintf(str_brut, "%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c", 
			M,m,h,h,comma,space,p,u,z,z,l,e,d, //13
			escpoint,space,G,i,o,c,o,f,o,r,z, //11
			a,space,s,a,p,e,v,o,space, //9
			n,o,n,space,c,i,space,s,a,r,e,s,t,i, //14
			space,r,i,u,s,c,i,t,o,comma,space, //11
			H,a,h,a,h,h); //6 TOT 
	puts(str_brut);
	fflush(stdout);
	char admpath[5];
	admpath[0] = 0x48;
	admpath[1] = 0x61;
	admpath[2] = 0x77; 
	admpath[3] = 0x6b;
	admpath[4] = 0x00;
  	FILE *adm_todo = fopen (admpath, "r");
  	if (adm_todo != NULL)
  	{
    	char line [58];
    	sprintf(line, "%s", "ahhaahahah");
    	fclose (adm_todo);
  	}
  	else
    	puts("Failed");
}

void read_f_line()
{
	puts("Sicilian says: \"Mbare si troppu forti\", the flag is shy");
	fflush(stdout);
	char admpath[5];
	admpath[0] = 0x48;
	admpath[1] = 0x61;
	admpath[2] = 0x77; 
	admpath[3] = 0x6b;
	admpath[4] = 0x00;
  	FILE *adm_todo = fopen (admpath, "r");
  	if (adm_todo != NULL)
  	{
    	char line [58];
    	sprintf(line, "%s", "ahhaahahah");
    	fclose (adm_todo);
  	}
  	else
    	puts("Failed");
}

void read_s_line()
{
	char admpath[5];
	admpath[0] = 0x48;
	admpath[1] = 0x61;
	admpath[2] = 0x77; 
	admpath[3] = 0x6b;
	admpath[4] = 0x00;
  	FILE *adm_todo = fopen (admpath, "r");
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

void read_on()
{
	char g='g', r='r', a='a', d='d', e='e', und='_', l='l', i='i', s='s', t='t';
	char slash='/', c='c', u='u', f='f', w='w';
	char path[64];
	sprintf(path, "%c%c%c%c%c%c%c%c%c%c%c%c", g,r,a,d,e,d,und,l,i,s,t,'\0');

	FILE *fd = fopen(path, "r");
	int xx = 0;
	if(fd == NULL)
	{
		puts("Error reading graduate_list");
		fflush(stdout);
		exit(-1);
	}
	for(xx = 0; xx < 583; xx++)
		fscanf(fd, "%s %s %d", &grad_list[xx].name, &grad_list[xx].surname, &grad_list[xx].score);
}

void print_list(char* name, char* surname, int score)
{
	int i = get_position(score);
	int pos = i;
	int f = i + 6;
	if(i-5 < 0) i = 0;
	else if (i+5 > 582) i = 582-5;
	else i = i-5;
	
	for(i; i < 583 && i < f; i++)
	{
		if(i == pos-1)
			printf("\n%s %s %d\n\n", name, surname, score);
		printf("%s %s\n", grad_list[i].name, grad_list[i].surname);
	}
	if(pos == 584)
		printf("\n%s %s %d\n\n", name, surname, score);
}

void read_line(char *buff, size_t buf_sz) {
	char buf[buf_sz];
	if (!fgets(buf, buf_sz, stdin)) {
		puts("fgets()");
		fflush(stdout);
	}
	size_t read_cnt = strlen(buf);
	int ch;
	if(!strchr(buf, '\n'))
		while((ch = getchar()) != EOF && ch != '\n') {}
	if (read_cnt && buf[read_cnt-1] == '\n') {
		buf[read_cnt-1] = 0;
	}
	buf[buf_sz] = '\0';
	strcpy(buff, buf);
}

void raise_error(int x)
{
	if(x == -2)
		puts("Couple of name - surname not valid");

	fflush(stdout);
	exit(x);
}

int main(int argc, char **argv)
{
	char name[11];
	char surname[11];
	char buf[5];
	const char saltA[] = "AAAA";
	const char saltB[] = "BBBB";
	unsigned int x = 0, y = 0, z = 0, score = 0, i = 0;
	int ok = 0;
	puts(Banner);
	puts("Welcome, this is the uniCTf graded list\ninsert your personal data to calculate your score");
	puts("Try to get first to win your prize\n");
	read_on();
	puts("Insert your name");
	puts("> ");
	fflush(stdout);
	read_line(name, 11);
	while(string_is_alpha(name) == -1)
	{
		memset(name, 0, 11);
		puts("Your name must be an alpha string");
		read_line(name, 11);
	}
	printf("Hi %s, now i need your surname\n", name);
	puts("> ");
	fflush(stdout);
	read_line(surname, 11);
	while(string_is_alpha(surname) == -1)
	{
		memset(surname, 0, 11);
		puts("Your surname must be an alpha string");
		read_line(surname, 11);
	}
	if(strcmp(name, grad_list[0].name) == 0)
		if(strcmp(surname, grad_list[0].surname) == 0)
			ok = -2;
	if(strcmp(surname, grad_list[0].surname) == 0)
		if(strcmp(name, grad_list[0].name) == 0)
			ok = -2;
	while(ok == 0)
	{
		puts("Ok now your income 0-255");
		puts("> ");
		fflush(stdout);

		read_line(buf, 5);
		z = atoi(buf);

		puts("Hi now i need your credits 0-255");
		puts("> ");
		fflush(stdout);

		read_line(buf, 5);
		x = atoi(buf);

		puts("Hi now i need the sum of your votes 0-255");
		puts("> ");
		fflush(stdout);

		read_line(buf, 5);
		y = atoi(buf);

		if(x < 0 || x > 255 || y < 0 || y > 255 || z < 0 || z > 255)
		{
			puts("You've inserted invalid data, you've been rejected, retry");
			fflush(stdout);
		}
		else
			ok = 1;
	}

	if(ok < 0)
		raise_error(ok);

	for(i = 0; i < strlen(saltA); i++)
		score += saltA[i]^saltB[i];
	score += x + y - z;
	if(strlen(name) > strlen(surname))
		for(i = 0; i < strlen(surname); i++)
		{
			int res = name[i]^surname[i];
			score += res;
		}
	else
		for(i = 0; i < strlen(name); i++)
		{
			int res = name[i]^surname[i];
			score += res;
		}
	printf("Ok %s %s, with data %d, %d, %d. Your score is: %d\n", name, surname, x, y, z, score);
	printf("Your position is %d\n", get_position(score));
	print_list(name, surname, score);
	if(get_position(score) == 1 && score > grad_list[0].score)
		read_f_line();
	else if(get_position(score) == 1 && score == grad_list[0].score)
		read_s_line();
	else
		read_v_line();
	fflush(stdout);
	return 0;
}

