#
from django.http import HttpResponse
from django.shortcuts import render
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
import re
import requests
import json

################## DADOS IMPORTANTES PARA ACTIVE DIRECTORY #################################

#Codigos usados verificar se o usuario esta ativo ou nao no AD:
#512=Enabled
#514= Disabled
#66048 = Enabled, password never expires
#66050 = Disabled, password never expires
#66082 = Disabled, Password Doesn’t Expire & Not Required

#Codigo para pegar os dados do usuario

#sAMAccountName --> Nome do usuario ou DSK no AD (Ex.: contoso)
#cn --> Nome do usuario com espaco (Ex.: Contoso)
#userAccountControl --> Verifica o status do usuario no AD (Consultar os codigos acima)

#countryCode: Caso esse valor seja 2 o usuário não é inserido na tabela (Fiz isso para desativar os usuários do sistema. Ex: SQL Administrator, etc)

###########################################################################################

# Esta função verifica se existe uma string ou conjunto de string e retorna true or false
def comparacao_string(comparacao,string):
	re.compile(comparacao)
	if (re.search(comparacao,string)):
		return True
	else:
		return False

#Esta funão faz conexão com o Active Directory e retorna um array contendo: Nome, Telefone, Departamento, E-mail
def list_ramal(request):
    #Define o servidor
    hostname = 'IPServer' #192.168.10.X
    server = Server(hostname, get_info=ALL)

    #Executa a conexão com o servidor LDAP
    username = 'usuario@contoso.local' #nome de usuário do active directory
    password = 'conto@123'  #senha do active directory
    connection = Connection (server, user=username, password=password, auto_bind=True, collect_usage=True) #faz a conexão com o servidor LDAP
    connection.search('dc=contoso,dc=local', '(objectclass=person)', attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES]) #executa uma pesquisa pelo objeto pessoa no AD retornando todos os usuários
    conn_entries = connection.entries
    list = []
    list_test = []
    list_users = []
    list_users_active = []
    for i in conn_entries:
        dict = i
        list.append(dict)
    for x in list:
        list_test.append(x)

	#Este loop remove todos os objetos que tem DSK, NTB, remove da tabela.
    for y in list_test:
        if y['sAMAccountName']:
        	exist_sama = str(y['sAMAccountName'])
        	se_dsk = comparacao_string('DSK',exist_sama)
        	se_ntb = comparacao_string('NTB',exist_sama)
        	se_srv = comparacao_string('SRV',exist_sama)
        	if se_dsk == False and se_ntb == False and se_srv == False:
        		list_users.append(y)

	#Este loop Verifica quais usuários estão desativados no LDAP e remove da tabela.
    for k in list_users:
        control_user = str(k['userAccountControl'])
        remove_user_code = str(k['countryCode'])
        if (control_user == '514' or control_user == '66082' or control_user == '66050') or (remove_user_code == '2'):
        	pass
        else:
        	list_users_active.append(k)
    print(len(list_users_active))

	#Retorna a lista de array para a página index.html que está em templates
    return render(request, 'index.html', {'list_users_active':list_users_active})
