import datetime, paramiko
# from scp import SCPClient

# USERNAME OF SSH MACHINE SHOULD BE AS ARGS OR IN SETTINGS FILE. TODO

def put_flag(host, service, flag):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys() # Save my life

    ssh.connect(host['ipaddress'], username=host["username"])

    # ssh.connect(host['ipaddress'], username=host['username'], password=host['password'])
    stdin, stdout, stderr = ssh.exec_command("echo -n {} > {}".format(flag, service['flagpath']))
    """
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('flag.txt', 'toserver.txt')
    """

def get_flag(host, service):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(host['ipaddress'], username=host["username"])

    # ssh.connect(host['ipaddress'], username=host['username'], password=host['password'])
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
        if team['host']['ipaddress'] == ipaddress:
            return team
    return None

def append_to_history(mongodb, _id, message):
    mongodb.ctfgame.update_one({
        "_id": _id,
    },
        { "$push": { "history": "{} - {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  , message) } }
    )
