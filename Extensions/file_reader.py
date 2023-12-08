import json
from PIL import Image

arcsong_cache = None
profile_cache = None
score_cache = None
# template_cache = None
image_cache = {}

def getJacket(path, enhanced = False):
    """
    Retrieves a jacket image from the specified path.

    Args:
        path (str): The path to the jacket image file.
        enhanced (bool, optional): Whether the jacket image should be enhanced. Defaults to False.

    Returns:
        PIL.Image.Image: The jacket image.

    Raises:
        FileNotFoundError: If the jacket image file is not found.
    """
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
    """
    Retrieves the arcsong from the cache if available, otherwise loads it from the 'Assets/arcsong.json' file.

    Parameters:
        None

    Returns:
        dict: The arcsong data loaded from the cache or the file.
    """
    global arcsong_cache
    if arcsong_cache is None:
        with open ('Assets/arcsong.json', 'r', encoding='utf-8') as json_file:
                arcsong_cache = json.load(json_file)
    return arcsong_cache

def saveArcsong(data):
    """
    Saves the given `data` to the `arcsong.json` file.

    Parameters:
        data (any): The data to be saved.

    Returns:
        None
    """
    with open ('Assets/arcsong.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        global arcsong_cache
        arcsong_cache = data
    return

def getProfile():
    """
    Retrieves the profile from the cache or loads it from the 'profile.json' file if not found.

    Returns:
        The profile data stored in the cache.
    """
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
    """
    Reads the score data from the 'score.json' file and returns it.

    Returns:
        The score data loaded from the file.
    """
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
    
async def reload_data():
    """
    Reloads the data by resetting the global cache variables.
    """
    global arcsong_cache
    global profile_cache
    global score_cache
    global image_cache
    arcsong_cache = None
    profile_cache = None
    score_cache = None
    image_cache = {}
    return