#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <pwd.h>
#include <string.h>


int main(int argc, char **argv, char **environ)
{
	char *cc = "cc";
	char *o = "-o";
	char *out_file = "arinzaarunzal0";
	char *stk = "-fno-stack-protector";
	char *std = "-std=c99";
	char *ut = "utils.o";
	char *in_file = "arinzaarunzal0.c";
	char *params[8] = {cc, o, out_file, stk, std, ut, in_file, NULL};
	if (execve("/usr/bin/cc", params, environ) == -1)
	{
		int i = 0;
		puts("execve error");
		for(i = 0; i < 7; i++)
		{
			printf("%s ", params[i]);
		}
		printf("\n");
	}
	return 0;
}
