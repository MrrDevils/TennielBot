import random
try:
    from .file_reader import getProfile, getScore, saveProfile, saveScore
except ImportError:
    from file_reader import getProfile, getScore, saveProfile, saveScore


class UserAlreadyRegistered(Exception):
    pass

class UserNotRegistered(Exception):
    pass

async def generate_random_9_digit_number():
    players = getProfile()
    while True:
        code = random.randint(100000000, 999999999)
        code_exists = any(player['code'] == str(code)
                          for player in players['users'])

        if not code_exists:
            break
    return code

async def register(discord_id, username, code):
    users = getProfile()
    for user in users['users']:
        if user['discord_id'] == discord_id:
            raise UserAlreadyRegistered("User already registered.")
    new_code = code
    if code == "":
        new_code = await generate_random_9_digit_number()

    entry = {
        "discord_id": discord_id,
        "username": username,
        "code": new_code
    }
    users['users'].append(entry)
    saveProfile(users)
    
    scores = getScore()
    if code != "":
        for player in scores['players']:
            if player['code'] == code:
                return 0
        
    newplayer = {
        "code": new_code,
        "best30": 0,
        "scores": []
    }
    scores['players'].append(newplayer)
    saveScore(scores)
    return new_code

async def getCode(discord_id):
    profiles = getProfile()
    for profile in profiles['users']:
        if profile['discord_id'] == discord_id:
            return profile['code']
    raise UserNotRegistered("User not registered.")