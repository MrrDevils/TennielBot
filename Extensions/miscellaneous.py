import asyncio

async def sideFormat(num):
    if num == 0:
        side = "Light"
        color = "#2da2c0"
    elif num == 1:
        side = "Conflict"
        color = "#391749"
    elif num == 2:
        side = "Colorless"
        color = "#eae9e0"
    return side, color

async def diffColorFormat(diff):
    if diff == 3:
        return "#a74f4f"
    elif diff == 2:
        return "#a64ba6"
    elif diff == 1:
        return "#55aa55"
    else:
        return "#44a2a2"