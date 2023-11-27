import json
from PIL import Image

arcsong_cache = None
profile_cache = None
score_cache = None
# template_cache = None
image_cache = {}

def getJacket(path, enhanced = False):
    key = path + str(enhanced)
    if key in image_cache:
        return image_cache[key]
    else:
        try:
            image = Image.open(path)
        except FileNotFoundError:
            image = Image.open('Assets/Jackets/base.jpg')
        if enhanced:
            return #TODO later
        image_cache[key] = image
        return image

def getArcsong():
    global arcsong_cache
    if arcsong_cache is None:
        with open ('Assets/arcsong.json', 'r', encoding='utf-8') as json_file:
                arcsong_cache = json.load(json_file)
    return arcsong_cache

def saveArcsong(data):
    with open ('Assets/arcsong.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        global arcsong_cache
        arcsong_cache = data
    return

def getProfile():
    global profile_cache
    if profile_cache is None:
        with open ('Assets/profile.json', 'r', encoding='utf-8') as json_file:
                profile_cache = json.load(json_file)
    return profile_cache

def saveProfile(data):
    with open ('Assets/profile.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        global profile_cache
        profile_cache = data
    return

def getScore():
    global score_cache
    if score_cache is None:
        with open ('Assets/score.json', 'r', encoding='utf-8') as json_file:
                score_cache = json.load(json_file)
    return score_cache

def saveScore(data):
    with open ('Assets/score.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        global score_cache
        score_cache = data
    return

# def getTemplate():
#     global template_cache
#     if template_cache is None:
#         with open ('Assets/template.txt', 'r', encoding='utf-8') as file:
#                 template_cache = file.read()
#     return template_cache
    
async def reload():
    global arcsong_cache
    global profile_cache
    global score_cache
    global image_cache
    arcsong_cache = None
    profile_cache = None
    score_cache = None
    image_cache = {}
    return