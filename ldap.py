# 2017.06.19
# LDAP.py
# Generate users, groups, memberships in Active Directory
# anton.bezkrovnyy@gmail.com
 
 
# for work with Active Directry
from ldap3 import Server, Connection, ALL, NTLM
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups as addUsersInGroups
# data generator
from elizabeth import Personal, Address,Text
import random
  
# define constans
  
serverName='lsd-dc1.stand.lsd'
connUser="stand.lsd\\Администратор"
connUserPwd="" # enter pwd here
usersOU = 'ou=test-ou,dc=stand,dc=lsd' # ou for generated users
groupsOU = 'ou=test-groups,dc=stand,dc=lsd'# ou for generated groups
address = Address('en') # generate data for OU name
person = Personal('en') # generate data for users
  
usersDnList = [] # global list DN of generated users
groupsDnList = [] # global list DN of generated groups
 
 
# let's connect
server = Server(serverName, get_info=ALL)
conn = Connection(server, user=connUser, password=connUserPwd, authentication=NTLM)
conn.bind() #must be TRUE if OK
  
conn.add(usersOU, 'organizationalUnit') # add test-ou for users
conn.add(groupsOU, 'organizationalUnit') # add test-ou for groups
 
# generate groups
data = Text('en')
for _ in range(0,10):
    currentGroup = 'cn='+data.word()+',ou=test-groups,dc=stand,dc=lsd'
    conn.add(currentGroup, 'group')
    groupsDnList.append(currentGroup) # add gnerated group to global list
     
for _ in range(0,10):
    address_country = address.country() # generate OU name
    conn.add('ou='+address_country+',ou=test-ou,dc=stand,dc=lsd', 'organizationalUnit') #create OU
    for _ in range (0,10):
        name = person.name(gender='male')
        surname = person.surname(gender='male')
        currentUser = 'cn='+name+'.'+surname+','+'ou='+address_country+',ou=test-ou,dc=stand,dc=lsd'
        usersDnList.append(currentUser) # add generated user in global list
        conn.add(currentUser, 'User', # add user in OU
        {'givenName': name,
        'sn': surname,
        'departmentNumber': 'DEV',
        'telephoneNumber': 1111})
  
for _ in range(0,300):
    rndUser = random.choice(usersDnList) # random user from list
    rndGroup = random.choice(groupsDnList) # random group from list
    addUsersInGroups(conn, rndUser, rndGroup) # add user to group
