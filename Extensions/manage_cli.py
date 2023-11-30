import os
import time
import json
from thefuzz import process

def getArcsong():
    with open ('Assets/arcsong.json', 'r', encoding='utf-8') as json_file:
            arcsong = json.load(json_file)
            return arcsong

def saveArcsong(data):
    with open ('Assets/arcsong.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    return

def getSongs():
    arcsong = getArcsong()
    return arcsong['songs']

def convert_time_to_seconds(time_str):
    if ':' not in time_str:
        try:
            return int(time_str)
        except ValueError:
            return 0
        
    parts = time_str.split(':')
    
    if len(parts) != 2:
        return 0
    
    try:
        minutes = int(parts[0])
        seconds = int(parts[1])
        total_seconds = minutes * 60 + seconds
        return total_seconds
    except ValueError:
        return 0
    
def get_difficulty(prompt):
    while True:
        diff = input(prompt)
        if diff == '0':
            return 0
        if '+' in diff:
            diff = diff.replace("+", "")
            try:
                diff = int(diff)
                return diff * 2 + 1
            except ValueError:
                print("Invalid input. Please provide a valid difficulty level.")
        else:
            try:
                diff = int(diff)
                return diff * 2
            except ValueError:
                print("Invalid input. Please provide a valid difficulty level.")
                
def get_side(prompt):
    while True:
        side = input(prompt).lower()
        if side == '0' or side == 'light':
            return 0
        elif side == '1' or side == 'conflict':
            return 1
        elif side == '2' or side == 'colorless' or side == 'colourless':
            return 2
        else:
            print("Invalid input. Please provide a valid side.")
                
def get_rating(prompt):
    while True:
        rating = input(prompt)
        if rating == '0':
            return 0
        try:
            rating = float(rating)
            return int(rating * 10)
        except ValueError:
            print("Invalid input. Please provide a valid rating.")
    
def get_bool(prompt):
    while True:
        response = input(prompt).lower()
        if response in 'yes' or response in 'true':
            return True
        elif response in 'no' or response in 'false':
            return False
        else:
            print("Invalid response. Please enter 'y' or 'n'.")
            
def getSongId(query):
    highest_confidence = 0
    top_song = None
    
    for song in songs:
        compare = process.extractOne(query, song['alias'])
        if compare[1] > 80:
            if compare[1] > highest_confidence:
                highest_confidence = compare[1]
                top_song = song
    if top_song is None:
        return None
    return top_song

def addSong():
    time_now = int(time.time())
    while True:
        os.system('cls')
        print("==== Add Song ====")
        song_id = input("Enter Song ID (0 to exit): ")
        if song_id == '0':
            return
        for song in songs:
            if song_id == song['song_id']:
                print("Song already exists.")
                time.sleep(2)
                continue
        difficulties = []
        
        print("---> Past")
        name_en = input("Name EN: ")
        name_jp = input("Name JP: ")
        artist = input("Artist: ")
        bpm = input("BPM: ")
        bpm_base = float(input("BPM Base: "))
        set = input("Set: ")
        set_friendly = input("Pack Name: ")
        times = input("Time (seconds or m:s): ")
        try:
            times = int(times)
        except ValueError:
            times = convert_time_to_seconds(times)
        side = get_side("Side: ")
        world_unlock = get_bool("Is World Unlock? (y/n): ")
        remote_download = get_bool("Is Remote Download? (y/n): ")
        bg = input("Background: ")
        date = time_now
        version = input("Version: ")
        difficulty = get_difficulty("Difficulty: ")
        rating = get_rating("Rating: ")
        note = int(input("Note: "))
        chart_designer = input("Chart Designer: ")
        jacket_designer = input("Illustration: ")
        jacket_override = get_bool("Is jacket override? (y/n): ")
        audio_override = get_bool("Is audio override? (y/n): ")
        
        entry = {
            "name_en": name_en,
            "name_jp": name_jp,
            "artist": artist,
            "bpm": bpm,
            "bpm_base": float(bpm_base),
            "set": set,
            "set_friendly": set_friendly,
            "time": times,
            "side": side,
            "world_unlock": world_unlock,
            "remote_download": remote_download,
            "bg": bg,
            "date": date,
            "version": version,
            "difficulty": difficulty,
            "rating": rating,
            "note": note,
            "chart_designer": chart_designer,
            "jacket_designer": jacket_designer,
            "jacket_override": jacket_override,
            "audio_override": audio_override,
        }
        difficulties.append(entry)
        os.system('cls')
        
        
        print("---> Present")
        if get_bool("Override? (y/n): "):
            name_en = input("Name EN: ")
            name_jp = input("Name JP: ")
            artist = input("Artist: ")
            bpm = input("BPM: ")
            bpm_base = float(input("BPM Base: "))
            times = input("Time (seconds or m:s): ")
            try:
                times = int(times)
            except ValueError:
                times = convert_time_to_seconds(times)
            world_unlock = get_bool("Is World Unlock? (y/n): ")
            remote_download = get_bool("Is Remote Download? (y/n): ")
            bg = input("Background: ")
            jacket_designer = input("Illustration: ")
            jacket_override = get_bool("Is jacket override? (y/n): ")
            audio_override = get_bool("Is audio override? (y/n): ")
            
            
        difficulty = get_difficulty("Difficulty: ")
        rating = get_rating("Rating: ")
        note = int(input("Note: "))
        chart_designer = input("Chart Designer: ")
            
        entry = {
            "name_en": name_en,
            "name_jp": name_jp,
            "artist": artist,
            "bpm": bpm,
            "bpm_base": float(bpm_base),
            "set": set,
            "set_friendly": set_friendly,
            "time": times,
            "side": side,
            "world_unlock": world_unlock,
            "remote_download": remote_download,
            "bg": bg,
            "date": date,
            "version": version,
            "difficulty": difficulty,
            "rating": rating,
            "note": note,
            "chart_designer": chart_designer,
            "jacket_designer": jacket_designer,
            "jacket_override": jacket_override,
            "audio_override": audio_override,
        }
        difficulties.append(entry)
        os.system('cls')

        print("---> Future")
        if get_bool("Override? (y/n): "):
            name_en = input("Name EN: ")
            name_jp = input("Name JP: ")
            artist = input("Artist: ")
            bpm = input("BPM: ")
            bpm_base = float(input("BPM Base: "))
            times = input("Time (seconds or m:s): ")
            try:
                times = int(times)
            except ValueError:
                times = convert_time_to_seconds(times)
            world_unlock = get_bool("Is World Unlock? (y/n): ")
            remote_download = get_bool("Is Remote Download? (y/n): ")
            bg = input("Background: ")
            jacket_designer = input("Illustration: ")
            jacket_override = get_bool("Is jacket override? (y/n): ")
            audio_override = get_bool("Is audio override? (y/n): ")
            
            
        difficulty = get_difficulty("Difficulty: ")
        rating = get_rating("Rating: ")
        note = int(input("Note: "))
        chart_designer = input("Chart Designer: ")
            
        entry = {
            "name_en": name_en,
            "name_jp": name_jp,
            "artist": artist,
            "bpm": bpm,
            "bpm_base": float(bpm_base),
            "set": set,
            "set_friendly": set_friendly,
            "time": times,
            "side": side,
            "world_unlock": world_unlock,
            "remote_download": remote_download,
            "bg": bg,
            "date": date,
            "version": version,
            "difficulty": difficulty,
            "rating": rating,
            "note": note,
            "chart_designer": chart_designer,
            "jacket_designer": jacket_designer,
            "jacket_override": jacket_override,
            "audio_override": audio_override,
        }
        difficulties.append(entry)
        os.system('cls')
        if get_bool("Has Beyond? (y/n): "):
            print("---> Beyond")
            if get_bool("Override? (y/n): "):
                name_en = input("Name EN: ")
                name_jp = input("Name JP: ")
                artist = input("Artist: ")
                bpm = input("BPM: ")
                bpm_base = float(input("BPM Base: "))
                world_unlock = get_bool("Is World Unlock? (y/n): ")
                remote_download = get_bool("Is Remote Download? (y/n): ")
                bg = input("Background: ")
                jacket_designer = input("Illustration: ")
                jacket_override = get_bool("Is jacket override? (y/n): ")
                audio_override = get_bool("Is audio override? (y/n): ")
                
                
            difficulty = get_difficulty("Difficulty: ")
            rating = get_rating("Rating: ")
            note = int(input("Note: "))
            chart_designer = input("Chart Designer: ")
                
            entry = {
                "name_en": name_en,
                "name_jp": name_jp,
                "artist": artist,
                "bpm": bpm,
                "bpm_base": float(bpm_base),
                "set": set,
                "set_friendly": set_friendly,
                "time": times,
                "side": side,
                "world_unlock": world_unlock,
                "remote_download": remote_download,
                "bg": bg,
                "date": date,
                "version": version,
                "difficulty": difficulty,
                "rating": rating,
                "note": note,
                "chart_designer": chart_designer,
                "jacket_designer": jacket_designer,
                "jacket_override": jacket_override,
                "audio_override": audio_override,
            }
            difficulties.append(entry)
            os.system('cls')
            
        aliases = []
        while True:
            alias = input("Enter an alias (0 to finish): ")
            if alias == '0':
                if len(aliases) == 0:
                    print("Must add atleast 1 alias.")
                    continue
                break
            aliases.append(alias)
            
        arcsong_entry = {
            "song_id": song_id,
            "difficulties": difficulties,
            "alias": aliases,
        }
        songs.append(arcsong_entry)
        formatted = json.dumps(arcsong_entry, indent=4, ensure_ascii=False)
        
        os.system('cls')
        print("==== Add Song ====")
        print(formatted)
        if get_bool("Confirm? (y/n): "):
            sorted_songs = sorted(songs, key=lambda x: x['song_id'])
            arcsong = {
                "songs": sorted_songs
            }
            saveArcsong(arcsong)
            print("Song added successfully.")
            time.sleep(2)
            break
        
        print("==== Add Song ====")
        print("1. Add more.")
        print("2. Cancel.")
        opt = input("Enter your option: ")
        if opt == '2':
            break

    
    os.system('cls')
    
def updateGeneral(found_song):
    new_data = {}
    updated = False
    while True:
        os.system('cls')
        print(f"==== Edit {found_song['song_id']} ====")
        print("1.  Update name.")
        print("2.  Update artist.")
        print("3.  Update bpm.")
        print("4.  Update set.")
        print("5.  Update pack.")
        print("6.  Update time.")
        print("7.  Update side.")
        print("8.  Update world unlock.")
        print("9.  Update remote download.")
        print("10. Update background.")
        print("11. Update date.")
        print("12. Update version.")
        print("13. Update chart designer.")
        print("14. Update jacket designer.")
        if updated:
            print("15. Done.\n")
            
            print("Changes: ")
            for key, value in new_data.items():
                print(f"{key}: {value}")
            print()
        else:
            print("15. Cancel.")
        opt = input("Enter your option: ")
        if opt == '1':
            name_en = input("New name EN: ")
            name_jp = input("New name JP: ")
            new_data['name_en'] = name_en
            new_data['name_jp'] = name_jp
        elif opt == '2':
            artist = input("New artist: ")
            new_data['artist'] = artist
        elif opt == '3':
            bpm = input("New bpm: ")
            bpm_base = float(input("New bpm base: "))
            new_data['bpm'] = bpm
            new_data['bpm_base'] = bpm_base
        elif opt == '4':
            set = input("New set: ")
            new_data['set'] = set
        elif opt == '5':
            set_friendly = input("New pack: ")
            new_data['set_friendly'] = set_friendly
        elif opt == '6':
            times = input("New time (seconds or m:s): ")
            try:
                times = int(times)
            except ValueError:
                times = convert_time_to_seconds(times)
            new_data['time'] = times
        elif opt == '7':
            side = get_side("New side: ")
            new_data['side'] = side
        elif opt == '8':
            world_unlock = get_bool("New world unlock? (y/n): ")
            new_data['world_unlock'] = world_unlock
        elif opt == '9':
            remote_download = get_bool("New remote download? (y/n): ")
            new_data['remote_download'] = remote_download
        elif opt == '10':
            bg = input("New background: ")
            new_data['bg'] = bg
        elif opt == '11':
            pass
        elif opt == '12':
            version = input("New version: ")
            new_data['version'] = version
        elif opt == '13':
            chart_designer = input("New chart designer: ")
            new_data['chart_designer'] = chart_designer
        elif opt == '14':
            jacket_designer = input("New jacket designer: ")
            new_data['jacket_designer'] = jacket_designer
        elif opt == '15':
            break
        else:
            print("Invalid option.")
            time.sleep(1)
            continue
        updated = True
    
    os.system('cls')
    temp = found_song
    for i in range(len(temp['difficulties'])):
        for dict, data in new_data.items():
            temp['difficulties'][i][dict]  = data
    print(f"==== Edit {found_song['song_id']} ====")
    print("After Edit:")
    formatted = json.dumps(temp, indent=4, ensure_ascii=False)
    print(formatted)
    if get_bool("Confirm? (y/n): "):
        for song in songs:
            if song['song_id'] == found_song['song_id']:
                song = temp
                break
        arcsong = {
            "songs": songs
        }
        saveArcsong(arcsong)
        print("Song updated successfully.")
        time.sleep(2)
        return
    else:
        print("Song update canceled.")
        time.sleep(2)
        return
        
def updateSong():
    while True:
        os.system('cls')
        print("==== Update Song ====")
        query = input("Song ID (0 to exit): ")
        if query == '0':
            break
        found_song = getSongId(query)
        if found_song is None:
            print("Song not found.")
            time.sleep(1)
            continue
        
        os.system('cls')
        print("==== Update Song ====")
        print("Found: ")
        formatted = json.dumps(found_song, indent=4, ensure_ascii=False)
        print(formatted)
        print("\n1. Update general data.")
        print("2. Update alias data.")
        print("3. Update difficulty data.")
        print("4. Add another difficulty.")
        print("5. Cancel.")
        opt = input("Enter your option: ")
        if opt == '1':
            updateGeneral(found_song)
        break
        

if __name__ == '__main__':
    global songs
    while(True):
        songs = getSongs()
        print("==== Arcsong Management System ====")
        print("1. Add Song")
        print("2. Remove Song")
        print("3. Update Song")
        print("4. View Songs")
        print("5. Exit")
        opt = input("Enter your option: ")
        if opt == '1':
            addSong()
            pass
        elif opt == '2':
            # removeSong()
            pass
        elif opt == '3':
            updateSong()
            pass
        elif opt == '4':
            # viewSongs()
            pass
        elif opt == '5':
            break
        else:
            print("Invalid option.")
            time.sleep(1)
            os.system('cls')
            continue
        os.system('cls')
