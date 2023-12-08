from file_reader import getArcsong

def get_set_info():
    """
    Retrieves the set information for each song in the arcsong.

    Returns:
        set_info (dict): A dictionary containing the set information for each song in the arcsong.
            The keys are the set IDs and the values are the corresponding set names.
    """
    arcsong = getArcsong()
    set_info = {}
    for song in arcsong["songs"]:
        difficulty = song["difficulties"][2]
        set_info[difficulty["set"]] = difficulty["set_friendly"]
    return set_info

print(get_set_info())