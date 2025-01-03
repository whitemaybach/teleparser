import os
try:
    from telethon.sync import TelegramClient
 
    from colorama import Fore
 
    from telethon.tl.functions.messages import GetDialogsRequest
    from telethon.tl.types import InputPeerEmpty
except ImportError:
    input(f'У вас отсутствуют нужные библиотеки. Установить?')
    os.system('pip install telethon')
    os.system('pip install colorama')
# Получим данные от Telegram Users API.
api_id = 26568341  # ID приложения. Его можно узнать на my.telegram.org
api_hash = '88b246e6b0034d0e7c63de6131f9eb87'  # HASH код приложения. Его можно узнать на my.telegram.org
phone_number = '+9 ' # ваш номер телефона в международном формате.
client = TelegramClient(phone_number, api_id, api_hash)

def phone_require():
    print(f'{Fore.BLUE}Введите номер телефона для продолжения...')
    return input()

def password_require():
    print(f'{Fore.YELLOW}Введите пароль от аккаунта Telegram для продолжения...')
    return input()

client.start(phone_require(), password_require())

banner = f"""{Fore.GREEN}
 _____  _                          _    ____
|  ___|| |  ___   _ __   ___  ___ | |_ |  _ \   __ _  _ __  ___   ___  _ __
| |_   | | / _ \ | '__| / _ \/ __|| __|| |_) | / _` || '__|/ __| / _ \| '__|
|  _|  | || (_) || |   |  __/\__ \| |_ |  __/ | (_| || |   \__ \|  __/| |
|_|    |_| \___/ |_|    \___||___/ \__||_|     \__,_||_|   |___/ \___||_|
"""

print(f'{banner}\n\nПарсер, созданный для людей.')
chats = []
last_date = None
size_chats = 200
groups=[]

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=size_chats,
    hash = 0
    )
)
chats.extend(result.chats)
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
    
print(f'{Fore.YELLOW}Выберите номер группы из перечня:')
i=0
for g in groups:
    print(F'{Fore.GREEN}{str(i)} - {g.title}')
    i+=1
g_index = input("Введите нужную цифру: ")
target_group=groups[int(g_index)]

print(f'{Fore.YELLOW}Узнаём пользователей...')
all_participants = client.get_participants(target_group)

print(f'{Fore.YELLOW}Начинаем парсить {all_participants.total} участников.')

i_ = 1
usernames = []
for user in all_participants:
    if user.username is not None:
        print(f'{Fore.GREEN}Парсинг {i_} участника из {all_participants.total} прошёл успешно.')
        usernames.append(f'@{user.username} - +{user.phone} - {user.first_name}')
        i_+=1
    else:
        usernames.append(f'+{user.phone} - {user.first_name}')
        print(f'{Fore.RED}{user.first_name} не имеет ника. Игнорируем.')
        i_+=1
print(f'{Fore.GREEN}Парсинг был проведен успешно.')
directory = input(f'В какую директорию сохранить `members.txt`?')
print(f'{Fore.YELLOW}Запись ников в `members.txt`...')

with open(f'{directory}/members.txt', 'w') as file:
    file.write('\n'.join(usernames))
    file.close()

print(f'{Fore.GREEN}Ники находятся в файле `members.txt` в папке {directory}.')

client.disconnect()
