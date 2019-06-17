import datetime, paramiko

def put_flag(host, service, flag):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys() # Save my life

    ssh.connect(host[ 'ipaddress_{}bit'.format(service['arch']) ], username=host['username'])

    stdin, stdout, stderr = ssh.exec_command("echo -n {} > {}".format(flag, service['flagpath']))

def get_flag(host, service):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()

    ssh.connect(host[ 'ipaddress_{}bit'.format(service['arch']) ], username=host['username'])

    stdin, stdout, stderr = ssh.exec_command("cat {}".format(service['flagpath']))
    flag = stdout.readline()
    return flag

def get_team_byname(teams, name):
    for team in teams:
        if team['name'] == name:
            return team
    return None

def get_team_byaddress(teams, ipaddress):
    for team in teams:
        for arch in [ "32", "64" ]:
            if team['host']['ipaddress_{}bit'.format(arch)] == ipaddress:
                return team
    return None

def append_to_history(mongodb, _id, message):
    mongodb.ctfgame.update_one({
        "_id": _id,
    },
        { "$push": { "history": "{} - {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  , message) } }
    )