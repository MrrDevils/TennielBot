import asyncio
import time
try:
    from .file_reader import getArcsong, getProfile, getScore, getJacket, saveScore
    from .search import detectTime, getSongId
except ImportError:
    from file_reader import getArcsong, getProfile, getScore, getJacket, saveScore
    from search import detectTime, getSongId


class DiffNotFoundError(ValueError):
    pass


class ChartNotFoundError(ValueError):
    pass


class PlayerNotFoundError(ValueError):
    pass


class AprilFoolsChartException(Exception):
    pass


diff_mapping = {
    "Past": 0,
    "Present": 1,
    "Future": 2,
    "Beyond": 3
}


async def calculate(score, constant):
    modifier = 0
    if constant <= 0:
        modifier = -999
    elif score >= 10000000:
        modifier = 2
    elif score >= 9800000 and score < 10000000:
        modifier = 1 + (score - 9800000) / 200000
    elif score < 9800000:
        modifier = (score - 9500000) / 300000
    rating = constant + modifier
    if rating < 0:
        return 0
    else:
        return round(rating, 5)


async def get_average_color(path):
    image = getJacket(path)
    image.thumbnail((50, 50))
    pixels = list(image.getdata())

    total_r = 0
    total_g = 0
    total_b = 0

    for r, g, b in pixels:
        total_r += r
        total_g += g
        total_b += b

    total_pixel = len(pixels)
    average_r = total_r // total_pixel
    average_g = total_g // total_pixel
    average_b = total_b // total_pixel

    r = max(0, min(255, average_r))
    g = max(0, min(255, average_g))
    b = max(0, min(255, average_b))

    return "#{:02X}{:02X}{:02X}".format(r, g, b)


async def add_commas_to_number(number):
    number_str = str(number)
    result = []

    for idx, digit in enumerate(reversed(number_str)):
        if idx > 0 and idx % 3 == 0:
            result.append("'")
        result.append(digit)
    return ''.join(reversed(result))\



async def getJacketPath(song_id, difficulty, override):
    if song_id == "melodyoflove":
        jacket = f"Assets/Jackets/{detectTime(song_id)}.jpg"
    elif override == False:
        jacket = f"Assets/Jackets/{song_id}.jpg"
    elif difficulty == 3:
        jacket = f"Assets/Jackets/{song_id}_BYD.jpg"
    elif difficulty == 1:
        jacket = f"Assets/Jackets/{song_id}_PRS.jpg"
    else:
        jacket = f"Assets/Jackets/{song_id}_PST.jpg"
    try:
        with open(jacket, "rb") as f:
            f.close()
    except FileNotFoundError:
        jacket = 'Assets/Jackets/base.jpg'
    return jacket


async def findCode(discord_id):
    players = getProfile()
    for player in players['users']:
        if player['discord_id'] == discord_id:
            return player['code']
    raise PlayerNotFoundError("Cannot find a matching code, please register.")


async def findPlayer(id):
    scores = getScore()
    for score in scores['players']:
        if score['code'] == id:
            return score
    raise PlayerNotFoundError("Cannot find a matching code, please register.")


async def saveData(player):
    players = getScore()
    for i in range(0, len(players['players'])):
        if players['players'][i]['code'] == player['code']:
            players['players'][i] = player
            break
    else:
        players['players'].append(player)
    saveScore(players)


async def result(chart_name, diff_name, score, user_id, s="True"):
    diff = diff_mapping.get(diff_name, None)
    save = bool(s)
    if diff is None:
        raise DiffNotFoundError("Invalid Difficulty.")
    try:
        chart = await getSongId(chart_name)
    except ChartNotFoundError:
        raise ChartNotFoundError(f"Cannot find the chart: {chart_name}")
    

    song_id = chart['song_id']
    try:
        song_name = chart['difficulties'][diff]['name_en']
    except IndexError:
        raise DiffNotFoundError("This chart does not have a Beyond difficulty.")
    cc = chart['difficulties'][diff]['rating'] / 10
    max_score = 10000000 + chart['difficulties'][diff]['note']
    jacket_override = chart['difficulties'][diff]['jacket_override']
    jacket_path = await getJacketPath(song_id, diff, jacket_override)
    rating = await calculate(score, cc)
    score_str = await add_commas_to_number(score)
    if int(score) == max_score:
        score_str = f"[{score_str}](https://youtu.be/dQw4w9WgXcQ?si=4hKe4HWjXd5QX3_G)"
    
    has_improved = False
    play_rank = -1
    old_ptt = 0.0
    new_ptt = 0.0

    
    if save and rating > 0:
        current_time = time.time()
        
        try:
            player = await findPlayer(await findCode(user_id))
        except PlayerNotFoundError:
            raise PlayerNotFoundError("Connot find your code. Have you registered?")


        old_ptt = round(player['best30'], 5)
        new_ptt = 0.0
        for i in range(0, 30):
            try:
                if player['scores'][i]['rating'] <= rating:
                    play_rank = i + 1
                    has_improved = True
                    break
            except IndexError:
                play_rank = i + 1
                has_improved = True
                break


        for play in player['scores']:
            if play['song_id'] == song_id and play['difficulty'] == diff:
                play['rating'] = rating
                play['score'] = score
                play['date'] = current_time
                break
        else:
            player['scores'].append({
                "song_id": song_id,
                "difficulty": diff,
                "score": score,
                "constant": cc,
                "rating": rating,
                "date": current_time
            })

        player['scores'].sort(key=lambda x: x['rating'], reverse=True)
        num_scores = len(player['scores'])
        average = min(num_scores, 30)

        if average > 0:
            b30_rating = sum(entry['rating']
                             for entry in player['scores'][:average]) / average
        else:
            b30_rating = 0

        player['best30'] = b30_rating
        new_ptt = round(player['best30'], 5)

        await saveData(player)
    result = {
        "song_id": song_id,
        "name_en": song_name,
        "difficulty": diff_name,
        "diff_index": diff,
        "constant": cc,
        "rating": rating,
        "score": score_str,
        "jacket": jacket_path,
        "old_ptt": old_ptt,
        "new_ptt": new_ptt,
        "has_improved": has_improved,
        "play_rank": play_rank,
    }
    return result

if __name__ == "__main__":
    # print(asyncio.run(findCode(432050736722083852)))
    print(-1 / 10)
