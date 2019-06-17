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

    mode_t sguid = S_IXGRP|S_IXUSR|S_ISUID|S_ISGID|S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH|S_IXOTH;
    mode_t rw_r_r = S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH;
    mode_t rw_rw_ = S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP;
    mode_t rw_r_ = S_IRUSR|S_IWUSR|S_IRGRP;

    chown("unictf_graded_list", user_uid, scorebot_gid);
    chown("graded_list", scorebot_uid, scorebot_gid);
    chown("Hawk", scorebot_uid, scorebot_gid);

    chmod("unictf_graded_list", sguid);
    chmod("graded_list", rw_r_);
    chmod("Hawk", rw_r_);

    return 0;
}