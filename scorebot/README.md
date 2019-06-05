# 🎯 unictf - scorebot

## setup

**Requirements**:
- python3
- mongodb

**Setup**:
1) Create virtualenv: `virtualenv -p python3 env`
2) Activate the env: `source env/bin/activate`
3) Install all requirements:
   - `pip install -r requirements.txt`
   - `pip install git+https://github.com/arthaud/python3-pwntools.git`

## services
- **CONFIG** Copy _services.json.dist_ to _services.json_ and populate it. It is a simple json where the key is the name of the service (lowercase) with the attribute _port_ and _flagpath_ (absolute)
- All the services must be up and usable for get a defense point. Each service need to have a **is_up** method that return **True** or **False**

## rules
- Team A cannot send the flag of Team A (same team)
- For gain defense point the service must be **UP, USABLE** and the flag must be **INTEGRY**
- All the team must be have ssh service up with restricted permission for write/read flag.
-
-

## setup ssh pub key
1.  ```ssh-keygen -t rsa -b 2048 -v```
2.  ``` ssh-copy-id -i ~/my-certificate.pub username@ip```

## how to submit flag
Just do a **[POST]** request to `http://scorebotaddress:4526/submitflag` with the following args:
```javascript
{
    "flag": "unictf{BC9QHE1n8rwqM2R0....sx8FgryGbt6}", /** Stoled flag **/
    "servicename": "service1", /** Name of the service hacked **/
    "stoledfrom": "192.168.1.x", /** IP-Address of the 'victim' **/
    "teamname": "team1-power" /** Attack team name **/
}
```


## database
```javascript
{
    "_id" : ObjectId("5cebfd9....7945d6d1"),
    "teams" : [
        {
            "name" : "team1-power", /** Lower case suggested for team name**/
            "host" : {
                "ipaddress" : "192.168.x.x",
                "sshkeypath": "../../idrsa.pub
            },
            "points" : {
                "attack" : 10,
                "defense" : 5
            }
        },
        {
            "name" : "team2-strong",
            "host" : {
                "ipaddress" : "192.168.x.x",
                "sshkeypath": "../../idrsa.pub
            },
            "points" : {
                "attack" : 2,
                "defense" : 8
            }
        }
    ],
    "name" : "Competion name - UNICTF 2019!!!",
    "startdate" : ISODate("2019-05-27T17:07:30.762Z"),
    "history" : [ ... ],
    "flags" : { /** This is will be generate/update from scorebot **/
        "team1-power" : {
            "service_name1" : {
                "flag" : { ... }, /** Crypted **/
                "stoled" : false,
                "generate_at" : ISODate("2019-05-29T12:55:41.405Z")
            },
            "service_name2" : {
                "flag" : { ... }, /** Crypted **/
                "stoled" : false,
                "generate_at" : ISODate("2019-05-29T12:55:41.383Z")
            },
            "service_name3" : {
                "flag" : { ... }, /** Crypted **/
                "stoled" : false,
                "generate_at" : ISODate("2019-05-29T12:55:41.368Z")
            }
        },
        "team2-strong" : {
            "service_name1" : {
                "flag" : { ... }, /** Crypted **/
                "stoled" : false,
                "generate_at" : ISODate("2019-05-29T12:55:42.156Z")
            },
            ...
        }
    }
}
```
