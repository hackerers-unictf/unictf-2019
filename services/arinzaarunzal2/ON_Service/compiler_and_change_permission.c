#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <pwd.h>
#include <string.h>
uid_t get_uid(char *str_uid)
{
    uid_t uid;
    char *endptr;
    struct passwd *pwd;
    uid = strtol(str_uid, &endptr, 10);  /* Allow a numeric string */
    if (*endptr != '\0') {         /* Was not pure numeric string */
        pwd = getpwnam(str_uid);   /* Try getting UID for username */
        if (pwd == NULL) {
            perror("getpwnam");
            return -1;
        }
        uid = pwd->pw_uid;
    }
    return uid;
}

uid_t get_gid(char *str_gid)
{
    uid_t gid;
    char *endptr;
    struct passwd *pwd;
    gid = strtol(str_gid, &endptr, 10);  /* Allow a numeric string */
    if (*endptr != '\0') {         /* Was not pure numeric string */
        pwd = getpwnam(str_gid);   /* Try getting GID for username */
        if (pwd == NULL) {
            perror("getpwnam");
            return -1;
        }
        gid = pwd->pw_gid;
    }
    return gid;
}

int main(int argc, char **argv, char **environ){
pid_t childPid;  // the child process that the execution will soon run inside of. 
childPid = fork();
if(childPid == 0)  // fork succeeded 
{   
   char *cc = "cc";
	char *o = "-o";
	char *w = "-w";
	char *out_file = "arinzaarunzal2";
	char *stk = "-fno-stack-protector";
	char *in_file = "arinzaarunzal2.c";
	char *params[7] = {cc, o, out_file,w, stk, in_file, NULL};
	if (execve("/usr/bin/cc", params, environ) == -1)
	{
		int i = 0;
		puts("execve error");
		for(i = 0; i < 6; i++)
		{
			printf("%s ", params[i]);
		}
		printf("\n");
	}
	exit(0);
}
else if(childPid < 0)  // fork failed 
{    
   printf("error");
  exit(-1);
}
else  // Main (parent) process after fork succeeds 
{    
    int returnStatus;    
    waitpid(childPid, &returnStatus, 0);  // Parent process waits here for child to terminate.

    if (returnStatus == 0)  // Verify child process terminated without error.  
    {
  	
    uid_t scorebot_uid = get_uid("scorebot");
    uid_t user_uid = get_uid("user");
    uid_t guest_uid = get_uid("guest");
    uid_t root_uid = 0;
    char *endptr;
    
    gid_t scorebot_gid = get_gid("scorebot");
    gid_t user_gid = get_gid("user");
    gid_t guest_gid = get_gid("guest");
    
    chown("address", scorebot_uid, scorebot_gid);
    chown("arinzaarunzal2", guest_uid, guest_gid);
    chown("arinzaarunzal2.c", scorebot_uid, user_gid);
    chown("recompile", root_uid, root_uid);
    chown("start_service.sh",scorebot_uid,user_gid);
    chmod("start_service.sh",S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IXGRP);
    chmod("address", S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP|S_IROTH);
    chmod("arinzaarunzal2",S_IXUSR|S_IXGRP|S_ISUID|S_ISGID|S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH|S_IXOTH);
    chmod("recompile", S_ISUID|S_ISGID|S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IXGRP|S_IROTH|S_IXOTH);
    chmod("arinzaarunzal2.c", S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP);
    }
}
return  0;
}
