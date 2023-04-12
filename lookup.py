import requests
import json
import os
os.system("color 0a")
os.system("title Roblox user lookup")
os.system("cls")
WEBHOOK_URL = "wh-url"
def send_webhook(data):
    payload = {
        "content": data
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)
    if response.status_code == 204:
        print(data)
    else:
        print("Error, Please try again.")
def fetch_user_data(user_id):
    response = requests.get(f'https://users.roblox.com/v1/users/{user_id}')
    if response.status_code != 200:
        print('User not found')
        exit()
    user_data = response.json()
    username = user_data['name']
    bio = user_data['description']
    is_banned = user_data['isBanned']
    is_verified = user_data['hasVerifiedBadge']
    display_name = user_data['displayName']
    created = user_data['created']
    external_app_display_name = user_data['externalAppDisplayName']
    data = f"Username: {username}\nDisplay Name: {display_name}\nBio: {bio}\nBanned: {is_banned}\nVerified Badge: {is_verified}\nCreated: {created}\nExternal App Display Name: {external_app_display_name}"
    return data
while True:
    command = input("Enter command: ")
    if command.startswith("lid"):
        user_id = command.split()[1]
        data = fetch_user_data(user_id)
        send_webhook(data)
