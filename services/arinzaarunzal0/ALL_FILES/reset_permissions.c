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


int main(int argc, char **argv, char **environ)
{
    uid_t scorebot_uid = get_uid("scorebot");
    uid_t user_uid = get_uid("user");
    uid_t guest_uid = get_uid("guest");
    uid_t root_uid = 0;
    char *endptr;
    
    gid_t scorebot_gid = get_gid("scorebot");
    gid_t user_gid = get_gid("user");
    gid_t guest_gid = get_gid("guest");

    chown("arinzaadm", scorebot_uid, scorebot_gid);
    chown("utils.h", scorebot_uid, scorebot_gid); 
    chown("utils.o", scorebot_uid, scorebot_gid);
    chown("arinzaarunzal0", guest_uid, guest_gid);
    chown("todos", guest_uid, guest_gid);
    chown("arinzaarunzal0.c", scorebot_uid, user_gid);
    chown("recompile", root_uid, root_uid);

    chmod("arinzaadm", S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH); 
    chmod("arinzaarunzal0", S_ISUID|S_ISGID|S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH|S_IXOTH); 
    chmod("recompile", S_ISUID|S_ISGID|S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH|S_IXOTH);
    chmod("arinzaarunzal0.c", S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP);
    chmod("utils.h", S_IRUSR|S_IWUSR|S_IRGRP);
    chmod("utils.o", S_IRUSR|S_IWUSR|S_IRGRP);
    return 0;
}