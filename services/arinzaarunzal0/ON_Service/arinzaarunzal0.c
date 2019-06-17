#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <err.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <stdbool.h>
#include <ctype.h>
#include <linux/limits.h>
#include "utils.h"

const char BANNER[] = "\
     ▄▄▄       ██▀███   ██▓ ███▄    █ ▒███████▒ ▄▄▄      ▄▄▄       ██▀███   █    ██  ███▄    █ ▒███████▒ ▄▄▄      \n\
    ▒████▄    ▓██ ▒ ██▒▓██▒ ██ ▀█   █ ▒ ▒ ▒ ▄▀░▒████▄   ▒████▄    ▓██ ▒ ██▒ ██  ▓██▒ ██ ▀█   █ ▒ ▒ ▒ ▄▀░▒████▄    \n\
    ▒██  ▀█▄  ▓██ ░▄█ ▒▒██▒▓██  ▀█ ██▒░ ▒ ▄▀▒░ ▒██  ▀█▄ ▒██  ▀█▄  ▓██ ░▄█ ▒▓██  ▒██░▓██  ▀█ ██▒░ ▒ ▄▀▒░ ▒██  ▀█▄  \n\
    ░██▄▄▄▄██ ▒██▀▀█▄  ░██░▓██▒  ▐▌██▒  ▄▀▒   ░░██▄▄▄▄██░██▄▄▄▄██ ▒██▀▀█▄  ▓▓█  ░██░▓██▒  ▐▌██▒  ▄▀▒   ░░██▄▄▄▄██ \n\
     ▓█   ▓██▒░██▓ ▒██▒░██░▒██░   ▓██░▒███████▒ ▓█   ▓██▒▓█   ▓██▒░██▓ ▒██▒▒▒█████▓ ▒██░   ▓██░▒███████▒ ▓█   ▓██▒\n\
     ▒▒   ▓▒█░░ ▒▓ ░▒▓░░▓  ░ ▒░   ▒ ▒ ░▒▒ ▓░▒░▒ ▒▒   ▓▒█░▒▒   ▓▒█░░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒ ░▒▒ ▓░▒░▒ ▒▒   ▓▒█░\n\
      ▒   ▒▒ ░  ░▒ ░ ▒░ ▒ ░░ ░░   ░ ▒░░░▒ ▒ ░ ▒  ▒   ▒▒ ░ ▒   ▒▒ ░  ░▒ ░ ▒░░░▒░ ░ ░ ░ ░░   ░ ▒░░░▒ ▒ ░ ▒  ▒   ▒▒ ░\n\
      ░   ▒     ░░   ░  ▒ ░   ░   ░ ░ ░ ░ ░ ░ ░  ░   ▒    ░   ▒     ░░   ░  ░░░ ░ ░    ░   ░ ░ ░ ░ ░ ░ ░  ░   ▒   \n\
          ░  ░   ░      ░           ░   ░ ░          ░  ░     ░  ░   ░        ░              ░   ░ ░          ░  ░\n\
                                      ░                                                        ░                  \n\
       _                _                  \n\
      | |   _____ _____| |  ______ _ _ ___ \n\
      | |__/ -_) V / -_) | |_ / -_) '_/ _ \\\n\
      |____\\___|\\_/\\___|_| /__\\___|_| \\___/";                                        





const char MENU[] = "\n\
Hi %s, what would you like to do?\n\
1) Print TODO list\n\
2) Print TODO entry\n\
3) Store TODO entry\n\
4) Delete TODO entry\n\
5) Remote Administration\n\
7) Exit\n\
> ";
const char OUT_OF_BOUNDS_MESSAGE[] = "Sorry but this model only supports 128 TODO list entries.\nPlease upgrade to the ArinzaArunza20 for increased capacity.";

#define TODO_COUNT 128
#define TODO_LENGTH 48

int todo_fd;
char username[64];
char todos[TODO_COUNT*TODO_LENGTH];

void init() {
  system("mkdir todos 2>/dev/null");
  setlinebuf(stdout);
}

void read_line(char *buf, size_t buf_sz) {
  if (!fgets(buf, buf_sz, stdin)) {
    err(1, "fgets()");
  }
  size_t read_cnt = strlen(buf);
  if (read_cnt && buf[read_cnt-1] == '\n') {
    buf[read_cnt-1] = 0;
  }
}

bool read_all(int fd, char *buf, size_t read_sz) {
  while (read_sz) {
    ssize_t num_read = read(fd, buf, read_sz);
    if (num_read <= 0) {
      return false;
    }
    read_sz -= num_read;
    buf += num_read;
  }
  return true;
}

void write_all(int fd, char *buf, size_t write_sz) {
  while (write_sz) {
    ssize_t num_written = write(fd, buf, write_sz);
    if (num_written <= 0) {
      err(1, "write");
    }
    write_sz -= num_written;
    buf += num_written;
  }
}

bool string_is_alpha(const char *s) {
  for (; *s; s++) {
    if (!isalpha(*s)) {
      return false;
    }
  }
  return true;
}

bool list_is_empty() {
  for (int i = 0; i < TODO_COUNT; i++) {
    if(todos[i*TODO_LENGTH]) {
      return false;
    }
  }
  return true;
}

void print_list() {
  if (list_is_empty()) {
    puts("Your TODO list is empty. Enjoy your free time!");
    return;
  }
  puts("+=====+=================================================================+");
  for (int i = 0; i < TODO_COUNT; i++) {
    if(todos[i*TODO_LENGTH]) {
      printf("| %3d | %-63s |\n", i, &todos[i*TODO_LENGTH]);
    }
  }
  puts("+=====+=================================================================+");
}

void open_todos() {
  char todos_filename[PATH_MAX] = "todos/";
  strncat(todos_filename, username, sizeof(todos_filename)-strlen(todos_filename) - 1);

  todo_fd = open(todos_filename, O_RDWR);
  if (todo_fd != -1 && read_all(todo_fd, todos, sizeof(todos))) {
    if (!list_is_empty()) {
      print_list();
    }
  } else {
    todo_fd = open(todos_filename, O_RDWR | O_CREAT | O_TRUNC, 0600);
    if (todo_fd == -1) {
      err(1, "Could not create TODO storage file");
    }
  }
}

bool administration_enabled() {
  return false;
}

void authenticate() {
  printf("user: ");
  fflush(stdout);
  read_line(username, sizeof(username));

  if (!string_is_alpha(username)) {
    errx(1, "username can only consist of [a-zA-Z]");
  }
  if(strcmp("root", username) == 0)
  {
    puts("You cannot be root now, username automatically changed to user");
    strcpy(username, "user");
    return;
  }
}

int read_int() {
  char buf[128];
  read_line(buf, sizeof(buf));
  return atoi(buf);
}

void store_todos() {
  write_all(todo_fd, todos, sizeof(todos));
  close(todo_fd);
}

void active_admin() {
  char administration[64];
  char password[64];
  strcpy(administration, "DISABLED");
  printf("Insert the admin index: ");
  fflush(stdout);
  int idx = read_int();
  if (idx > TODO_COUNT || idx < 0 || idx != 23) {
    puts(OUT_OF_BOUNDS_MESSAGE);
    return;
  }
  puts("Ok, Insert the admin password now: ");
  read_line(password, 64);
  if(strcmp(password, "aRinZaArUnZaTrOlL") == 0)
  {
    puts("Ok, Administration Enabled");
    strcpy(administration, "ENABLED");
    return;
  }
  else
    puts("Failed to active Administration");
}

void store_todo() {
  printf("In which slot would you like to store the new entry? ");
  fflush(stdout);
  int idx = read_int();
  if (idx > TODO_COUNT || idx < 0) {
    puts(OUT_OF_BOUNDS_MESSAGE);
    return;
  }
  printf("What's your TODO? ");
  fflush(stdout);
  read_line(&todos[idx*TODO_LENGTH], TODO_LENGTH);
}

void print_Hawk_todos(char *u) { //SO WHAT???
  char user[64];
  strcpy(user, u);
  printf("Username: %s\n", user);
  char password[64];
  puts("Hi Hawk, insert your root password");
  puts(">> ");
  fgets(password, 128, stdin);
  size_t read_cnt = strlen(password);
  if (read_cnt && password[read_cnt-1] == '\n') {
    password[read_cnt-1] = 0;
  }
  if (strcmp("Hi8342DHD34gjsW", password) != 0)
  {
    puts("Wrong Password");
    return;
  }
  else if(strcmp("Hawk",  user) != 0)
  {
    puts("Hey man, you're not Hawk!!! INTRUDEEER!!");
    return;
  }
  hawk_todos();
}

void print_todo() {
  printf("Which entry would you like to read? ");
  fflush(stdout);
  int idx = read_int();
  if (idx > TODO_COUNT || idx < 0) {
    puts(OUT_OF_BOUNDS_MESSAGE);
    return;
  }
  printf("Your TODO: %s\n", &todos[idx*TODO_LENGTH]);
}

void delete_todo() {
  printf("Which TODO number did you finish? ");
  fflush(stdout);
  int idx = read_int();
  if (idx > TODO_COUNT || idx < 0) {
    puts(OUT_OF_BOUNDS_MESSAGE);
    return;
  }
  todos[idx*TODO_LENGTH] = 0;
  if (list_is_empty()) {
    puts("Awesome, you cleared the whole list!");
  } else {
    puts("Nice job, keep it up!");
  }
}

int main(int argc, char *argv[]) {
  init();

  puts(BANNER);

  authenticate();

  open_todos();

  while (true) {
    printf(MENU, username);
    fflush(stdout);
    int choice = read_int();
    char yesno[64];
    puts("");
    switch (choice) {
      case 1:
        print_list();
        break;
      case 2:
        print_todo();
        break;
      case 3:
        store_todo();
        break;
      case 4:
        delete_todo();
        break;
      case 5:
        if(administration_enabled())
          puts("Heeeyyy, Administration is enabled for arinzaarunza");
        else
        {
          puts("Administration is disabled, do you want to active? type y: ");
          read_line(yesno, sizeof(yesno));
          if(strcmp(yesno, "y") == 0)
            active_admin();
          else
            memset((void*)yesno, 0, strlen(yesno));
        }
        break;
      case 6:
        print_Hawk_todos(username);
        break;
      case 7:
        store_todos();
        puts("Your TODO list has been stored. Have a nice day!");
        return 0;
      default:
        printf("unknown option %d\n", choice);
        break;
    }
  }
}
