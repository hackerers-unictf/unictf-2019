from datetime import datetime
from paramiko import SSHClient
# from scp import SCPClient

def put_flag(host, service, flag):
    ssh = SSHClient()
    ssh.load_system_host_keys()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key_file(host['sshkeypath'])
    ssh.connect(host['ipaddress'], username='edwards', pkey = key)

    # ssh.connect(host['ipaddress'], username=host['username'], password=host['password'])
    stdin, stdout, stderr = ssh.exec_command("echo -n {} > {}".format(flag, service['flagpath']))
    """
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('flag.txt', 'toserver.txt')
    """

def get_flag(host, service, flag):
    ssh = SSHClient()
    ssh.load_system_host_keys()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key_file(host['sshkeypath'])
    ssh.connect(host['ipaddress'], username='edwards', pkey = key)

    # ssh.connect(host['ipaddress'], username=host['username'], password=host['password'])
    stdin, stdout, stderr = ssh.exec_command("cat {}".format(service['flagpath']))
    flag = stdout.readlines()
    return flag

def get_team_byname(teams, name):
    for team in teams:
        if team['name'] == name:
            return team
    return None

def get_team_byaddress(teams, ipaddress):
    for team in teams:
        if team['host']['ipaddress'] == ipaddress:
            return team
    return None

def append_to_history(mongodb, _id, message):
    mongodb.ctfgame.update_one({
        "_id": _id,
    },
        { "$push": { "history": "{} - {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")  , message) } }
    )
