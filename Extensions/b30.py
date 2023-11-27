import asyncio
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import time
import json

try:
    from .file_reader import getArcsong, getProfile
    from .result import findPlayer, add_commas_to_number, getJacketPath
except ImportError:
    from file_reader import getArcsong, getProfile
    from result import findPlayer, add_commas_to_number, getJacketPath


class ScoreIndexError(IndexError):
    pass


class SongIdIndexError(IndexError):
    pass

class PlayerNotFoundError(ValueError):
    pass


mode_mapping = {
    "LxBot Full": 0,
    "LxBot Simple": 1,
    "Official": 2
}
reverse_diff_mapping = {
    0: "Past",
    1: "Present",
    2: "Future",
    3: "Beyond"
}
score_grades = {
    (10000000, float('inf')): '[EX+/P]',
    (9900000, 10000000): '[EX+]',
    (9800000, 9900000): '[EX]',
    (9500000, 9800000): '[AA]',
    (9200000, 9500000): '[A]',
    (8900000, 9200000): '[B]',
    (-float('inf'), 8900000): '[D]'
}
special = [
    'omegafour', 'guardina', 'aterlbus', 'odysseia', 'crossover',
    'crosssoul', 'neokosmo', 'mu', 'vector', 'onefr'
]
extra_special = ['ii']
quon_mapping = {
    "quon": "Quon (Feryquitous)",
    "quonwacca": "Quon (DJ Noriken)"
}


background = Image.open('Assets/General/background.jpg')
ii_light = Image.open('Assets/General/ii_light.png')
ii_dark = Image.open('Assets/General/ii_dark.png')
with open('Assets/offset.json', 'r') as f:
    offsets = json.load(f)

arcsong = getArcsong()
song_ids = [song['song_id'] for song in arcsong['songs']]


async def findProfile(discord_id):
    players = getProfile()
    for player in players['users']:
        if player['discord_id'] == discord_id:
            return player
    raise PlayerNotFoundError("Cannot find a matching code, please register.")

async def textlimit(text):
    max_width = 12
    cut_lines = []
    current_line = ""

    for char in text:
        if char == " " and len(current_line) == max_width:
            cut_lines.append(current_line + '...')
            current_line = ""
            break
        elif len(current_line) <= max_width:
            current_line += char
        else:

            cut_lines.append(current_line + '...')
            current_line = ""
            break

    if current_line:
        cut_lines.append(current_line)

    return cut_lines[0]


async def calculate_grade(score):
    for score_range, grade in score_grades.items():
        if score_range[0] <= score < score_range[1]:
            return grade


async def binarySearch(arcsong, target):
    left, right = 0, len(song_ids) - 1
    while left <= right:
        mid = (left + right) // 2
        if song_ids[mid] == target:
            return arcsong['songs'][mid]
        elif song_ids[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    raise SongIdIndexError("Song ID not found")


async def convert_seconds(time_now, date):
    if date == 0:
        return "N/A"
    seconds = time_now - date
    seconds = round(seconds)
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:  # Less than an hour
        minutes = seconds // 60
        return f"{minutes}m"
    elif seconds < 86400:  # Less than a day
        hours = seconds // 3600
        return f"{hours}h"
    else:
        days = seconds // 86400
        return f"{days}d"


async def simple(data):
    primary_font = ImageFont.truetype('Assets/General/Mada-Medium.ttf', 30)
    score_font = ImageFont.truetype('Assets/General/exo_bold.ttf', 29)
    ptt_font = ImageFont.truetype('Assets/General/exo_bold.ttf', 18)
    index_font = ImageFont.truetype('Assets/General/Mada-Medium.ttf', 30)
    info_font = ImageFont.truetype('Assets/General/exo_bold.ttf', 26)
    secondary_font = ImageFont.truetype('Assets/General/Roboto-Medium.ttf', 29)
    b30 = Image.new('RGBA', (1456, 1294), (255, 255, 255, 255))
    draw = ImageDraw.Draw(b30)
    offset = offsets['simple']

    increments = offset['increment']
    title_offset = offset['title']
    score_offset = offset['score']
    grade_offset = offset['grade']
    ptt_offset = offset['potential']
    index_offset = offset['index']
    day_offset = offset['date']

    scores = data['scores']
    
    base_color = (80, 75, 90)
    beyond_color = (130, 45, 60)
    max_color = (80, 128, 140)

    for i in range(0, 6):
        for j in range(0, 5):
            color = base_color
            score_color = base_color
            title_font = primary_font
            index = j + (i * 5)
            if scores[index]['difficulty'] == 3:
                color = beyond_color
                score_color = beyond_color
            x = j * increments[0]
            y = i * increments[1]
            index_str = f'#{index + 1}'
            rating = f'Potential: {scores[index]["cc"]} > {scores[index]["rating"]}'
            
            if scores[index]['is_max']:
                score_color = max_color
            if scores[index]['song_id'] in special:
                title_font = secondary_font

            if scores[index]['song_id'] in extra_special:
                ii = ii_dark.resize((30,30))
                b30.paste(
                    ii, (title_offset[0] + x + 2, title_offset[1] + y + 2), ii)
            else:
                if scores[index]['song_id'] in ["quon", "quonwacca"]:
                    title = quon_mapping.get(scores[index]['song_id'])
                else:
                    title = scores[index]['song']
                draw.text((title_offset[0] + x, title_offset[1] + y), title, font=title_font,
                          fill=color)
            draw.text((score_offset[0] + x, score_offset[1] + y), scores[index]['score'], font=score_font,
                      fill=score_color)
            draw.text((ptt_offset[0] + x, ptt_offset[1] + y), rating, font=ptt_font,
                      fill=color)
            draw.text((grade_offset[0] + x, grade_offset[1] + y), scores[index]['grade'], font=ptt_font,
                      fill=color, anchor='ra')
            draw.text((index_offset[0] + x, index_offset[1] + y), index_str, font=index_font,
                      fill=color)
            draw.text((day_offset[0] + x, day_offset[1] + y), scores[index]['day'], font=ptt_font,
                      fill=color, anchor='ra')
    header_offset = [offset['header1'], offset['header2']]
    name_offset = offset['name']
    b30_offset = offset['b30']
    
    header = "Arcaea Best 30"
    credit = "Generated by TennielBot"
    name = data['name']
    b30_rating = data['b30']
    b30_str = f"Best 30 AVG: {b30_rating}"
    draw.text(header_offset[0], header, font=info_font, fill=base_color)
    draw.text(header_offset[1], credit, font=info_font, fill=base_color, anchor='ra')
    draw.text(name_offset, name, font=primary_font, fill=base_color)
    draw.text(b30_offset, b30_str, font=info_font, fill=base_color, anchor='ra')
    
    file_name = f'Assets/B30/{name}.png'
    try:
        b30.save(file_name, 'PNG', optimize=True, quality=90)
    except FileNotFoundError:
        b30.save('test.png', 'PNG', optimize=True, quality=90)
    return file_name

async def b30Generate(discord_id, mode_text):
    mode = mode_mapping.get(mode_text)
    profile = await findProfile(discord_id)
    player = await findPlayer(profile['code'])
    time_now = time.time()

    scores = []

    try:
        for i in range(0, 30):
            day = await convert_seconds(time_now, player['scores'][i]['date'])
            song = await binarySearch(arcsong, player['scores'][i]['song_id'])
            song_id = song['song_id']
            difficulty = player['scores'][i]['difficulty']
            song_name_full = song['difficulties'][difficulty]['name_en']
            song_name = await textlimit(song_name_full)
            diff_str = reverse_diff_mapping.get(difficulty)
            score = player['scores'][i]['score']
            cc = song['difficulties'][difficulty]['rating'] / 10
            rating = player['scores'][i]['rating']
            grade = await calculate_grade(score)
            override = song['difficulties'][difficulty]['jacket_override']
            max_score = song['difficulties'][difficulty]['note'] + 10000000
            score_str = await add_commas_to_number(score)
            is_max = score == max_score
            jacket_path = await getJacketPath(player['scores'][i]['song_id'], difficulty, override)
            dict = {
                "song": song_name,
                "song_id": song_id,
                "score": score_str,
                "difficulty": difficulty,
                "cc": cc,
                "rating": rating,
                "grade": grade,
                "jacket_path": jacket_path,
                "day": day,
                "is_max": is_max,
            }
            scores.append(dict)
    except IndexError:
        raise ScoreIndexError("Player has less than 30 scores")

    data = {
        "name": profile['username'],
        "b30": round(player['best30'], 5),
        "scores": scores
    }

    if mode == 0:
        # return await full(player) TODO
        return
    elif mode == 1:
        return await simple(data)
    elif mode == 2:
        # return await official(player) TODO
        return

if __name__ == '__main__':
    asyncio.run(b30Generate(732195731045220402, "LxBot Simple"))
    print("Done")