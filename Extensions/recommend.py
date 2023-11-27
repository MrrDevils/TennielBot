import asyncio
import random
import re
try:
    from .file_reader import getArcsong
except ImportError:
    from file_reader import getArcsong
    

pattern = re.compile(r"(recommend|give|show|suggest|something|another).*(song|chart|another|different|alternative|else|one)")

with open('Assets/templates.txt', 'r', encoding='utf-8') as f:
    templates = f.read().splitlines()

async def getRandomTemplate():
    return random.choice(templates)

async def getRandomChart():
    arcsong = getArcsong()
    chart = random.choice(arcsong['songs'])
    return chart["difficulties"][2]["name_en"], chart["difficulties"][2]["artist"]

async def generate():
    template = await getRandomTemplate()
    chart = await getRandomChart()
    return template.format(Song=chart[0], Artist=chart[1])
    
async def regenerate(prompt):
    if pattern.search(prompt.lower()):
        return await generate()
    else:
        raise Exception

if __name__ == "__main__":
    print(asyncio.run(generate()))
    