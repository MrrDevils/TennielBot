import hikari
import lightbulb
import os
from dotenv import load_dotenv
from asyncio import sleep


load_dotenv()
me = os.getenv("ME").split(',')
message = ""

manage = lightbulb.Plugin("ManagePlugin")

@manage.listen()
async def on_dm(ctx: hikari.DMMessageCreateEvent) -> None:
    if ctx.author.id not in me:
        return
    global message
    message = ctx.content
    

@manage.command
@lightbulb.command("add", "Add a song to arcsong.")
@lightbulb.implements(lightbulb.PrefixCommand)
async def add(ctx: lightbulb.Context) -> None:
    await ctx.respond("Enter a song id (0 to exit):")
    global message
    while message == "":
        sleep(2)
    if message == "0":
        return
    