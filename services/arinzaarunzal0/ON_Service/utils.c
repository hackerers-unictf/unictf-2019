#include "utils.h"

void hawk_todos()
{
	static const char admpath[] = "arinzaadm";
  	FILE *adm_todo = fopen (admpath, "r");
  	if (adm_todo != NULL)
  	{
    	char line [58];
    	while (fgets(line, sizeof line, adm_todo) != NULL)
    	{
    		fputs (line, stdout);
    	}
    	fclose (adm_todo);
  	}
  	else
    	puts("Failed Open Hawk Todos");
}