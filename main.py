import telebot as t
import parsermain as par
import sglite
from telebot import types as ty

TOKEN = ''
bot = t.TeleBot(TOKEN)
info = []
inaus = []
sq = sglite.bd()

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, '/reg --- sign up\n'
                                      '/crypto --- bring out information about cryptocurrency\n'
                                      '/log_in --- log in\n'
                                      '/log_out --- log out\n'
                                      '/change --- change information about user')

@bot.message_handler(commands=['reg'])
def register(message):
    msg = bot.send_message(message.chat.id, 'What will your nickname be')
    bot.register_next_step_handler(msg, nextstepreg)

def nextstepreg(message):
    global info
    info = []
    info.append(message.text)
    msg = bot.send_message(message.chat.id, 'What will your password be?')
    bot.register_next_step_handler(msg, nextstepreg2)

def nextstepreg2(message):
    global info
    info.append(message.text)
    msg = bot.send_message(message.chat.id, 'List the short names of cryptocurrencies with a space, the information about which you want to receive'
                                            '(please do not enter a non-existing cryptocurrency, this moment has not yet been calculated)')
    bot.register_next_step_handler(msg, end_step_reg)

def perevir(p):
    kt = len(p)
    kt = kt - 2
    v = True
    for x in range(0, kt):
        if p[x] == False:
            v = False
    return v

def end_step_reg(message):
    global info
    info.append(message.text)
    info.append(message.from_user.id)
    v = sq.add_to_table(info)
    info = []
    if v == 0:
        bot.send_message(message.chat.id, 'You have already logged in')
    else:
        bot.send_message(message.chat.id, 'You have successfully logged in')

@bot.message_handler(commands=['crypto'])
def crypto_func(message):
    global inaus
    id = message.from_user.id
    inaus = sq.info_about_user(id)
    if inaus[-1] == 0:
        print(inaus)
        bot.send_message(message.chat.id, 'Enter your password')
    elif inaus[-1] == None:
        bot.send_message(message.chat.id, 'Sign up')
    else:
        msg = bot.send_message(message.chat.id, 'Enter your nickname')
        bot.register_next_step_handler(msg, cryptovalut)

def cryptovalut(message):
    global inaus
    text = inaus[2]
    cry = text.split()
    crypto = []
    for x in range(0, len(cry)):
        crypto.append(cry[x].upper())
    func = False
    func1 = False
    iter = 0
    cryptovalute = []
    perevirka = []
    n = 1
    for i in range(0, len(crypto)):
        perevirka.append(False)
    perevirka.append(n)
    perevirka.append(iter)
    while func == False:
        cryptov = par.pagenation(n)
        cryptoval = par.beutifullist(cryptov)
        while func1 == False:
            for x in range(0, len(crypto)):
                if crypto[x] == cryptoval[iter]['small_title']:
                    cryptovalute.append(cryptoval[iter])
                    perevirka[x] = True
            if perevir(perevirka) == True:
                func1 = True
                func = True
            elif perevirka[-1] == 49:
                n = n + 1
                perevirka[-2] = n
                perevirka[-1] = 0
                iter = 0
                func1 = True
            else:
                 iter = iter + 1
                 perevirka[-1] = perevirka[-1] + 1
        func1 = False
    for i in range(0, len(cry)):
        bot.send_message(message.chat.id,
                         f'Name: {cryptovalute[i]["title"]}\nShort name: {cryptovalute[i]["small_title"]}\n'
                         f'Place: {cryptovalute[i]["place"]}\nLink: {cryptovalute[i]["link"]}\n'
                         f'Price: {cryptovalute[i]["price"]}\nCapitalization: {cryptovalute[i]["capital"]}\n'
                         f'Growth per hour: {cryptovalute[i]["hour"]}\n')

@bot.message_handler(commands=['log_in'])
def login(message):
    global info
    info = []
    id = message.from_user.id
    p = sq.vhid_in_acc(1, id)
    if p == -1:
        bot.send_message(message.chat.id, 'Enter your nickname')
        bot.register_next_step_handler(message, login2)
    elif p == 0:
        bot.send_message(message.chat.id, 'You have already logged in')

def login2(message):
    global info
    info.append(message.text)
    msg = bot.send_message(message.chat.id, 'Enter your password')
    bot.register_next_step_handler(msg, login3)

def login3(message):
    global info
    info.append(message.text)
    info.append(message.from_user.id)
    info.append(1)
    p = sq.perevirka(info)
    if p == None:
        bot.send_message(message.chat.id, 'You have entered an incorrect nickname')
    elif p == False:
        bot.send_message(message.chat.id, 'You have entered an incorrect password')
    else:
        sq.change_acc(info, info[0], 2)
        bot.send_message(message.chat.id, 'You have successfully logged in')

@bot.message_handler(commands=['log_out'])
def exit(message):
    id = message.from_user.id
    sq.vhid_in_acc(0, id)
    bot.send_message(message.chat.id, 'You have successfully logged out')

@bot.message_handler(commands=['change'])
def change(message):
    global info
    markup = ty.InlineKeyboardMarkup()
    nick = ty.InlineKeyboardButton(text = 'Nickname', callback_data = 'nick')
    password = ty.InlineKeyboardButton(text = 'Password', callback_data = 'password')
    crypto = ty.InlineKeyboardButton(text = 'Cryptocurrency', callback_data = 'crypto')
    markup.add(nick, password, crypto)
    id = message.from_user.id
    info = sq.info_about_user(id)
    if info[-1] == None:
        bot.send_message(message.chat.id, 'Sign up')
    elif info[-1] == 0:
        bot.send_message(message.chat.id, 'Log in')
    else:
        bot.send_message(message.chat.id, 'What are you want to change', reply_markup = markup)

@bot.callback_query_handler(func = lambda call: True)
def change2(call):
    if call.data == 'nick':
        bot.send_message(call.message.chat.id, 'Enter your new nickname')
        bot.register_next_step_handler(call.message, change_nick)
    elif call.data == 'password':
        bot.send_message(call.message.chat.id, 'Enter your new password')
        bot.register_next_step_handler(call.message, change_password)
    elif call.data == 'crypto':
        bot.send_message(call.message.chat.id, 'Enter your new cryptocurrency (including the old one if you still want it\
        get information)')
        bot.register_next_step_handler(call.message, change_crypto)

def change_nick(message):
    global info
    ch = info
    ch[0] = message.text
    sq.change_acc(ch, info[3], 1)
    bot.send_message(message.chat.id, 'Changed')

def change_password(message):
    global info
    ch = info
    ch[1] = message.text
    sq.change_acc(ch, info[0])
    bot.send_message(message.chat.id, 'Changed')

def change_crypto(message):
    global info
    ch = info
    ch[2] = message.text
    sq.change_acc(ch, info[0])
    bot.send_message(message.chat.id, 'Changed')

@bot.message_handler(content = ['text'])
def func(message):
    print(message.chat.id)
    bot.send_message(message.chat.id, 'Все працює')

bot.infinity_polling()
