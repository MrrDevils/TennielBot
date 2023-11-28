from .file_reader import getArcsong

class InvalidConstantError(ValueError):
    pass

arcsong = getArcsong()
past = []
present = []
future = []
beyond = []

for song in arcsong['songs']:
    past.append(song['difficulties'][0])
    present.append(song['difficulties'][1])
    future.append(song['difficulties'][2])
    try:
        beyond.append(song['difficulties'][3])
    except IndexError:
        pass

async def reloadAuto():
    arcsong = getArcsong()
    global past
    global present
    global future
    global beyond
    past = []
    present = []
    future = []
    beyond = []
    for song in arcsong['songs']:
        past.append(song['difficulties'][0])
        present.append(song['difficulties'][1])
        future.append(song['difficulties'][2])
        try:
            beyond.append(song['difficulties'][3])
        except IndexError:
            pass
        
async def chart_autocomplete(query):
    
    try:
        cc = float(query)
        if cc < 1.0 or cc > 12.0:
            raise InvalidConstantError
        found = 0
        
        found_songs = []

        if cc >= 7.0:
            for chart in future:
                if cc == chart['rating'] / 10:
                    name = f"{chart['name_en']} (Future)"
                    found_songs.append(name)
                    found += 1
                    
            for chart in beyond:
                if cc == chart['rating'] / 10:
                    name = f"{chart['name_en']} (Beyond)"
                    found_songs.append(name)
                    found += 1
        
        if cc < 10.0:
            for chart in past:
                if cc == chart['rating'] / 10:
                    name = f"{chart['name_en']} (Past)"
                    found_songs.append(name)
                    found += 1
            
            for chart in present:
                if cc == chart['rating'] / 10:
                    name = f"{chart['name_en']} (Present)"
                    found_songs.append(name)
                    found += 1
                        
            
        return found_songs[:25]
    except InvalidConstantError:
        return None
    except ValueError:
        pass
    query = query.lower()
    found_songs = []
    found = 0
    quon_idex = 0
    quon_mapping = ["Quon (Feryquitous)", "Quon (DJ Noriken)"]
    for chart in future:
        if query in chart["name_en"].lower():
            name = chart["name_en"]
            if name == "Quon":
                name = quon_mapping[quon_idex]
                quon_idex += 1
            found_songs.append(name)
            found += 1
            if found == 15:
                break
            
    return found_songs[:15]