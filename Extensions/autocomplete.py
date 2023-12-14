from .file_reader import getArcsong

class InvalidConstantException(ValueError):
    pass


global_past = []
global_present = []
global_future = []
global_beyond = []
featured = [
    "Ouvertüre",
    "Stratoliner",
    "eden",
    "XTREME",
    "Meta-Mysteria",
    "Wish Upon a Snow",
    "Alone & Lorn"
]
quon_mapping = [
    "Quon (Feryquitous)",
    "Quon (DJ Noriken)"
]
specials = [
    {
        "title": "nέο κόsmo",
        "alias": [
            "neokosmo"
        ]
    },
    {
        "title": "ΟΔΥΣΣΕΙΑ",
        "alias": [
            "odysseia"
        ]
    },
    {
        "title": "µ",
        "alias": [
            "mu"
        ]
    },
    {
        "title": "αterlβus",
        "alias": [
            "aterlbus"
        ]
    },
    {
        "title": "γuarδina",
        "alias": [
            "guardina",
            "yuardina"
        ]
    },
    {
        "title": " ͟͝͞Ⅱ́̕ ",
        "alias": [
            "ii"
        ]
    },
    {
        "title": "ω4",
        "alias": [
            "omegafour",
            "omega4"
            "w4"
        ]
    }
]

def load_auto():
    arcsong = getArcsong()
    global global_future
    global global_beyond
    global global_past
    global global_present
    
    global_past = []
    global_present = []
    global_future = []
    global_beyond = []
    
    for song in arcsong['songs']:
        global_past.append(song['difficulties'][0])
        global_present.append(song['difficulties'][1])
        global_future.append(song['difficulties'][2])
        
        if len(song['difficulties']) > 3:
            global_beyond.append(song['difficulties'][3])

load_auto()

async def chart_autocomplete(query):
    if query == "":
        return featured

    future = global_future
    beyond = global_beyond
    try:
        cc = float(query)
        if cc < 1.0 or cc > 12.0:
            raise InvalidConstantException

        found_songs = []

        if cc >= 7.0:
            found_songs += [
                f"{chart['name_en']} (Future)" 
                for chart in future 
                if cc == chart['rating'] / 10
            ]

            found_songs += [
                f"{chart['name_en']} (Beyond)"
                for chart in beyond
                if cc == chart['rating'] / 10
            ]

        if cc < 10.0:
            past = global_past
            present = global_present

            found_songs += [
                f"{chart['name_en']} (Past)"
                for chart in past
                if cc == chart['rating'] / 10
            ]

            found_songs += [
                f"{chart['name_en']} (Present)"
                for chart in present
                if cc == chart['rating'] / 10
            ]

        return found_songs[:25]

    except InvalidConstantException:
        pass
    except ValueError:
        pass

    query = query.lower().replace(" ", "")
    quon_idex = 0
    found_songs = []
    
    for chart in future:
        if query in chart["name_en"].lower().replace(" ", ""):
            name = chart["name_en"]
            if name == "Quon":
                name = quon_mapping[quon_idex]
                quon_idex += 1
            found_songs.append(name)
            if len(found_songs) == 15:
                return found_songs

    for special in specials:
        for alias in special["alias"]:
            if query in alias:
                found_songs.append(special["title"])
                if len(found_songs) == 15:
                    return found_songs
                break

    return found_songs[:15]
