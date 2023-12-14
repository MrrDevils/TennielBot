import asyncio
from thefuzz import process, fuzz
import datetime
try:
    from .file_reader import getArcsong
except ImportError:
    from file_reader import getArcsong
    
class InvalidConstantError(ValueError):
    pass

class DiffNotFoundError(ValueError):
    pass

class ChartNotFoundError(ValueError):
    pass

class AprilFoolsChartException(Exception):
    pass

past = ["pst", "past"]
present = ["prs", "present"]
future = ["ftr", "future"]
beyond = ["byd", "beyond"]
special = [
    "resurrection", "green", "overdead", "afterburn", "moment", "rityvvvip"
]
AF = [
    "ignotusafterburn", "singularityvvvip", "redandblueandgreen",
    "mistemperedmalignance", "oxeoeiccull", "overdead"
]
diff_mapping = {
    "Past": 0,
    "Present": 1,
    "Future": 2,
    "Beyond": 3,
    "All": 4
}


async def getTime(time_second):
    if time_second % 60 < 10:
        time = f"{int(time_second / 60)}:0{int(time_second % 60)}"
    else:
        time = f"{int(time_second / 60)}:{int(time_second % 60)}"
    return time

async def detectTime(jacket):
    current_time = datetime.datetime.now()
    current_hour = current_time.hour
    if 6 <= current_hour < 20:
        return f"{jacket}"
    else:
        return f"{jacket}_NIGHT"

async def getSongId(query):
    arcsong = getArcsong()
    found_songs = []
    highest_confidence = 0
    top_song = None
    
    for song in arcsong['songs']:
        compare = process.extractOne(query, song['alias'])
        if compare[1] > 80:
            found_songs.append((song, compare[1]))
            if compare[1] > highest_confidence:
                highest_confidence = compare[1]
                top_song = song
    if top_song is None:
        raise ChartNotFoundError('No charts found.')
    return top_song

async def diffFormat(diff):
    if diff % 2 == 0:
        return f'{int(float(diff / 2))}'
    elif diff == -1:
        return '?'
    else: 
        return f'{int(float((diff - 1) / 2))}+'
    
async def ratingFormat(rating):
    if rating == -1:
        return '?.?'
    elif rating == 0:
        return '0.0'
    else:
        return rating / 10

async def diffToString(diff):
    if diff == 0:
        return "Past"
    elif diff == 1:
        return "Present"
    elif diff == 2:
        return "Future"
    elif diff == 3:
        return "Beyond"
    else:
        return 4
    

async def search(query, diff_name):

    diff = diff_mapping.get(diff_name, None)
    try:
        cc = float(query)
        if cc < 1.0 or cc > 12.0:
            raise InvalidConstantError()
        output = await searchConstant(cc)
        return 2, output
    except InvalidConstantError as e:
        raise InvalidConstantError(e)
    except ValueError:
        pass

    query = query.split(' ')
    chart = ""
    
    
    override = False
    difficulty = 4

    try:
        for words in query:
            if process.extractOne(words, beyond)[1] > 90:
                difficulty = 3
                override = True
                break
            elif process.extractOne(words, future)[1] > 90:
                difficulty = 2
                override = True
                break
            elif process.extractOne(words, present)[1] > 90:
                difficulty = 1
                override = True
                break
            elif process.extractOne(words, past)[1] > 90:
                difficulty = 0
                override = True
                break
            elif process.extractOne(words, special)[1] >= 90:
                difficulty = 3
                chart += words
                override = True
            elif fuzz.ratio(words, "eternity") > 95:
                difficulty = 3
                chart = "lasteternity"
                override = True
                break
            elif fuzz.ratio(words.lower(), "misdeed") > 90:
                chart = "misdeed"
                override = False
                break
            else:
                chart = chart + words
    except Exception as e:
        print(e)
        raise DiffNotFoundError("Could not identify the chart's difficulty.")
    if override:
        diff = difficulty

    if diff == 4:
        try:
            output = await searchChart(chart)
        except AprilFoolsChartException:
            output = await searchDiff(chart, 2, True)
            return 1, output, 2
        return 0, output
    else:
        output = await searchDiff(chart, diff)
        return 1, output, diff
        
async def searchConstant(constant):
    """
    Asynchronously searches for songs with a specific constant.

    Args:
        constant (float): The constant value to search for.

    Returns:
        list: A list of dictionaries containing the song information matching the constant.

    Raises:
        InvalidConstantError: If no charts are found with the specified constant.
    """
    arcsong = getArcsong()
    found_song = []
    minSearch = 0
    if constant >= 10.0:
        minSearch = 2
    
    for song in arcsong['songs']:
        for index, difficulty in enumerate(song['difficulties']):
            if index < minSearch:
                continue
            cc = difficulty['rating'] / 10
            if cc == constant:
                song_index = {
                    "name_en": difficulty['name_en'],
                    "difficulty_name": await diffToString(index),
                }
                found_song.append(song_index)
    if found_song == []:
        raise InvalidConstantError(f"No charts found with the constant: {constant}")
    return found_song
        
async def searchChart(query):
    """
    Retrieves information about a song based on a search query.

    Parameters:
        query (str): The search query to retrieve the song information.
        
    Returns:
        dict: A dictionary containing information about the song, including the song ID, name (in English and Japanese), artist, jacket designer, BPM, side, pack, time, and difficulties. The difficulties are represented as a list of dictionaries, each containing the difficulty level, rating, and difficulty name. The jacket path is also included in the dictionary.
        
    Raises:
        AprilFoolsChartException: If the song ID is found in the April Fools chart and cannot be retrieved.
    """
    chart = await getSongId(query)
    if chart['song_id'] in AF:
        raise AprilFoolsChartException
    
    song_id = chart["song_id"]
    song_name = chart["difficulties"][2]["name_en"]
    song_name_jp = chart["difficulties"][2]["name_jp"]
    song_artist = chart["difficulties"][2]["artist"]
    illustrator = chart["difficulties"][2]["jacket_designer"]
    bpm = chart["difficulties"][2]["bpm"]
    side = chart["difficulties"][2]["side"]
    pack = chart["difficulties"][2]["set_friendly"]
    time_second = chart['difficulties'][2]['time']
    time = await getTime(time_second)
    
    difficulties = []
    for index, difficulty_info in enumerate(chart["difficulties"]):
        difficulty = await diffFormat(difficulty_info["difficulty"])
        cc = await ratingFormat(difficulty_info["rating"])
        difficulty_name = await diffToString(index)
        difficulties_index = {
            "difficulty": difficulty,
            "rating": cc,
            "difficulty_name": difficulty_name
        }
        difficulties.append(difficulties_index)
        
    if song_id == 'melodyoflove':
        jacket_path = f"Assets/Jackets/{await detectTime(song_id)}.jpg"
    else:
        jacket_path = f"Assets/Jackets/{song_id}.jpg"
    
    try:
        with open(jacket_path, "rb") as f:
            f.close()
    except FileNotFoundError:
        jacket_path = 'Assets/Jackets/base.jpg'
    
    song = {
        "song_id": song_id,
        "name_en": song_name,
        "name_jp": song_name_jp,
        "artist": song_artist,
        "jacket_designer": illustrator,
        "side": side,
        "bpm": bpm,
        "set_friendly": pack,
        "jacket_path": jacket_path,
        "difficulties": difficulties,
        "time": time,
    }
    return song

async def searchDiff(query, diff, skip = False):
    """
    Asynchronously searches for a song with the given query and difficulty and returns information about the song's difficulty.

    Args:
        query (str): The query used to search for the song.
        diff (int): The difficulty level of the song.
        skip (bool, optional): Whether to skip the search and use the provided query directly. Defaults to False.

    Raises:
        DiffNotFoundError: If the specified difficulty level is invalid.

    Returns:
        dict: A dictionary containing information about the song, including its ID, name, artist, difficulty, rating, side, BPM, set, chart designer, jacket path, note count, and duration.
    """
    if not skip:
        chart = await getSongId(query)
        if chart['song_id'] in AF:
            diff = 2
    else:
        chart = query
        
    song_id = chart["song_id"]
    try:
        song_name = chart["difficulties"][diff]["name_en"]
    except IndexError:
        raise DiffNotFoundError("Invalid Difficulty.")
    song_name_jp = chart["difficulties"][diff]["name_jp"]
    song_artist = chart["difficulties"][diff]["artist"]
    illustrator = chart["difficulties"][diff]["jacket_designer"]
    bpm = chart["difficulties"][diff]["bpm"]
    side = chart["difficulties"][diff]["side"]
    pack = chart["difficulties"][diff]["set_friendly"]
    time_second = chart['difficulties'][diff]['time']
    time = await getTime(time_second)
    chart_design = chart["difficulties"][diff]["chart_designer"]
    note = chart["difficulties"][diff]["note"]
    jacket_override = chart["difficulties"][diff]["jacket_override"]
    difficulty = await diffFormat(chart["difficulties"][diff]["difficulty"])
    cc = await ratingFormat(chart["difficulties"][diff]["rating"])
    
    if song_id == "melodyoflove":
        jacket_path = f"Assets/Jackets/{detectTime(song_id)}.jpg"
    elif jacket_override == False:
        jacket_path = f"Assets/Jackets/{song_id}.jpg"
    elif diff == 3:
        jacket_path = f"Assets/Jackets/{song_id}_BYD.jpg"
    elif diff == 1:
        jacket_path = f"Assets/Jackets/{song_id}_PRS.jpg"
    else:
        jacket_path = f"Assets/Jackets/{song_id}_PST.jpg"
    try:
        with open(jacket_path, "rb") as f:
            f.close()
    except FileNotFoundError:
        jacket_path = 'Assets/Jackets/base.jpg'
    
    song = {
        "song_id": song_id,
        "name_en": song_name,
        "name_jp": song_name_jp,
        "artist": song_artist,
        "jacket_designer": illustrator,
        "difficulty": difficulty,
        "difficulty_name": await diffToString(diff),
        "rating": cc,
        "side": side,
        "bpm": bpm,
        "set_friendly": pack,
        "chart_designer": chart_design,
        "jacket_path": jacket_path,
        "note": note,
        "time": time,
    }
    return song


if __name__ == "__main__":

    try:
        print(asyncio.run(search('grievous')))
    except Exception as e:
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {e.args[0]}")
        print(f"__cause__: {e.__cause__}")
        print(f"__context__: {e.__context__}")
        print(f"__traceback__: {e.__traceback__}")