def get_team_byname(teams, name):
    for team in teams:
        if team['name'] == name:
            return team

def get_team_byaddress(teams, ipaddress):
    for team in teams:
        if team['host']['ipaddress'] == ipaddress:
            return team