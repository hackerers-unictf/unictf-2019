import sqlite3
import random
import sys
import random
import string

def randomString(stringLength=8):
    letters= string.ascii_lowercase
    return ''.join(random.sample(letters,stringLength))


BANNER = """
 ______   __     __         __    __        _____     ______    
/\  ___\ /\ \   /\ \       /\ "-./  \      /\  __-.  /\  == \   
\ \  __\ \ \ \  \ \ \____  \ \ \-./\ \     \ \ \/\ \ \ \  __<   
 \ \_\    \ \_\  \ \_____\  \ \_\ \ \_\     \ \____-  \ \_____\ 
  \/_/     \/_/   \/_____/   \/_/  \/_/      \/____/   \/_____/ 
                                                                
                                                                """
MENU = """
1) add film
2) search filmmaker
3) search film
4) search kind
5) shuffle filmmaker
6) exit\n"""


flag = open('maker_token').read()

c = sqlite3.connect(':memory:').cursor()
nc=randomString(8)
nt=randomString(8)
c.execute("CREATE TABLE films (title text, filmmaker text, kind text)")
c.execute("CREATE TABLE "+nt+"("+nc+" text)")
c.execute("INSERT INTO "+nt+" VALUES ('{}')".format(flag))

def db_list(query):
    print('\n>> film list <<\n')
    for i, res in enumerate(c.execute(query).fetchall()):
        print('{}: "{}" by "{}" | "{}"\n'.format(i+1, res[0], res[1], res[2]))

print(BANNER)

while True:
    print(MENU)
    sys.stdout.write('> ')
    sys.stdout.flush()
    choice = raw_input()
    if choice not in ['1', '2', '3', '4', '5', '6']:
        print('invalid input')
        continue
    if choice == '1':
        print('filmmaker?')
        filmmaker = raw_input().replace('"', "")
        print('film title?')
        title = raw_input().replace('"', "")
        print('kind of film?')
        kind = raw_input().replace('"', "")
        c.execute("""INSERT INTO films VALUES ("{}", "{}", "{}")""".format(title, filmmaker, kind))
    elif choice == '2':
        print('filmmaker?')
        filmmaker = raw_input().replace('"', "")
        db_list("SELECT title, filmmaker, kind FROM films WHERE filmmaker = '{}'".format(filmmaker))
    elif choice == '3':
        print('film title?')
        title = raw_input().replace('"', "")
        db_list("SELECT title, filmmaker, kind FROM films WHERE title = '{}'".format(title))
    elif choice == '4':
        print('kind?')
        kind = raw_input().replace('"', "")
        db_list("SELECT title, filmmaker, kind FROM films WHERE kind = '{}'".format(kind))
    elif choice == '5':
        try:
            filmmaker = random.choice(list(c.execute("SELECT DISTINCT filmmaker FROM films")))[0]
            print('choosing films from random filmmaker: {}'.format(filmmaker))
            db_list("SELECT title, filmmaker, kind FROM films WHERE filmmaker = '{}'".format(filmmaker))
        except IndexError:
            print('the list is empty, add something to use this function')
            continue

    else:
        print('bye bye')
        exit(0)
