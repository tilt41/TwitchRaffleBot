import socket,threading,random,os

# Only change these settings
channelname = 'channel here' #Set the channel name here (No need for # that is done on for you)
nick = 'botaccountname'  # create an account for your bot on twitch then set you bot name here
password = 'Your oauth here' #get your bots oath from http://www.twitchapps.com/tmi/
# Do Not change anything below unless you know wht your doing

queue = 13 
channel = '#'+channelname
server = 'irc.twitch.tv'
irc = socket.socket()
irc.connect((server, 6667)) 
irc.send('PASS ' + password + '\r\n')
irc.send('NICK ' + nick + '\r\n')
irc.send('JOIN ' + channel + '\r\n')
rafflelist = []
beginraffle = "Entries for the raffle have started. Type !raffle  to join now!!"
print beginraffle
irc.send('PRIVMSG ' + channel + ' :' + beginraffle + '\r\n')
def rafflesave():
    rafflelist.append(user)
def run_raffle():
    print rafflelist
    winner = random.choice(rafflelist)
    rafflewinner = winner + " is the winner!! :)"
    irc.send('PRIVMSG ' + channel + ' :' + rafflewinner + '\r\n')
    print winner + ' won the raffle!!!'
    os._exit(0)
def message(msg):
    global queue
    queue = 5
    if queue < 20: 
        irc.send('PRIVMSG ' + channel + ' :' + msg + '\r\n')
    else:
        print 'Message deleted'
def queuetimer(): 
    global queue
    queue = 0
    threading.Timer(30,queuetimer).start()
queuetimer()
while True:
    tilthack = irc.recv(1204)
    user = tilthack.split(':')[1]
    user = user.split('!')[0] 
    if tilthack.find('PING') != -1:
        irc.send(tilthack.replace('PING', 'PONG')) 
    if tilthack.find('!raffle') != -1: 
            if any(word in user for word in rafflelist):
                message(user + ' has already entered :)')
            else:
                rafflesave()
                message(user + ' has been added to the raffle :)')
                print rafflelist
    if tilthack.find('!runraffle') != -1:
        run_raffle()
