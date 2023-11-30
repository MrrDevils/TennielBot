from asyncio import sleep
import os
from dotenv import load_dotenv
import hikari
import lightbulb
import time
from Extensions.search import search
from Extensions.result import result
from Extensions.miscellaneous import sideFormat, diffColorFormat
from Extensions.autocomplete import chart_autocomplete, loadAuto
from Extensions.file_reader import reload
from Extensions.recommend import generate, regenerate
from Extensions.b30 import b30Generate
from Extensions.register import register, getCode

load_dotenv()
guilds = os.getenv("GUILDS").split(',')
blacklisted_channels = os.getenv("BLACKLISTED_CHANNELS").split(',')
me = os.getenv("ME").split(',')
recommended_channels = {}

async def check_blacklist(user_id, channel_id = 0):
    channel_id = str(channel_id)
    user_id = str(user_id)
    if channel_id in blacklisted_channels and user_id not in me:
        return True
    return False

async def check_is_me(user_id):
    return user_id in me

tenniel = lightbulb.BotApp(
    token=os.getenv("TOKEN"),
    default_enabled_guilds=guilds,
    intents=hikari.Intents.ALL,
    prefix="+"
)

@tenniel.listen()
async def on_message(ctx: hikari.GuildMessageCreateEvent) -> None:
    time_now = time.time()
    if ctx.channel_id not in recommended_channels or ctx.author.is_bot:
        return
    elif recommended_channels[ctx.channel_id] - int(time_now) > 300:
        return
    try:
        output = await regenerate(ctx.content)
        recommended_channels[ctx.channel_id] = time_now
        await ctx.message.respond(output, reply=True)
    except Exception:
        return
    
# prefix command
@tenniel.command

    
@tenniel.command
@lightbulb.command("getcode", "Get your code.")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_get_code(ctx: lightbulb.SlashCommand) -> None:
    user_id = ctx.author.id
    try:
        code = await getCode(user_id)
    except Exception as e:
        embed = hikari.Embed(title=type(e).__name__,description=e.args[0] , color='#cc0000')
        await ctx.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                embed,
                flags=hikari.MessageFlag.EPHEMERAL,
            )
        return
    embed = hikari.Embed(title="Here's your code.", description=code, color='#00cc00')
    await ctx.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            embed,
            flags=hikari.MessageFlag.EPHEMERAL,
        )
    return
    
@tenniel.command
@lightbulb.option("name", "Add a custom name. (not required)",
                  default="",
                  type=str,
                  required=False)
@lightbulb.option("code", "Enter an existing code. (not required)",
                  default="",
                  type=str,
                  required=False)
@lightbulb.command("register", "Link your Discord to the bot.")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_register(ctx: lightbulb.SlashCommand) -> None:
    code = ctx.options.code
    code = code.translate(str.maketrans("", "", " ,.-'"))
    user_id = ctx.author.id
    user_name = ctx.author.username
    name = ctx.options.name
    if name == "":
        name = user_name
    try:
        output = await register(user_id, name, code)
    except Exception as e:
        embed = hikari.Embed(title=type(e).__name__,description=e.args[0] , color='#cc0000')
        await ctx.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                embed,
                flags=hikari.MessageFlag.EPHEMERAL,
            )
        return
    print(f'{user_name}: Registered as "{name}" with code: {code}')
    if output == 0:
        embed = hikari.Embed(title="Success!", description="Successfully registered to an existing code.", color='#00cc00')
        await ctx.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                embed,
                flags=hikari.MessageFlag.EPHEMERAL,
            )
        return
    new_code = output
    embed = hikari.Embed(title="Success!", description=f"Successfully registered. Your code is {new_code}.", color="#00cc00")
    await ctx.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            embed,
            flags=hikari.MessageFlag.EPHEMERAL,
        )
    return


@tenniel.command
@lightbulb.option("difficulty",
                  "Enter the difficulty of the song.",
                  choices=["Past", "Present", "Future", "Beyond", "All"],
                  default="All",
                  required=False,
                  type=str)
@lightbulb.option("chart", "Enter the song name.", autocomplete=True,)
@lightbulb.command("song", "Get a song's information.")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_song(ctx: lightbulb.SlashCommand) -> None:
    channel_id = ctx.channel_id
    user_id = ctx.author.id
    if await check_blacklist(user_id, channel_id):
        await ctx.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                "This command is not allowed in this channel.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
        return
    query = ctx.options.chart
    difficulty = ctx.options.difficulty
    try:
        output = await search(query, difficulty)
        if output[0] == None:
            raise Exception("Song not found.")
    except Exception as e:
        embed = hikari.Embed(title=type(e).__name__,description=e.args[0] , color='#cc0000')
        await ctx.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                embed,
                flags=hikari.MessageFlag.EPHEMERAL,
            )
        return
    if output[0] == 0: # Song Search
        chart = output[1]
        jacket = hikari.File(chart['jacket_path'])
        side_output = await sideFormat(chart['side'])
        side = side_output[0]
        color = side_output[1]
        description = ""
        if chart["name_jp"] != "":
            description = f'**Japanese Title:** {chart["name_jp"]}\n'
        description += f'**Artist:** {chart["artist"]}\n**Illustration:** {chart["jacket_designer"]}\n**Duration:** {chart["time"]}\n**BPM:** {chart["bpm"]}\n**Side:** {side}\n**Pack:** {chart["set_friendly"]}'
        field = ''
        for difficulty in chart['difficulties']:
            field += f"- {difficulty['difficulty_name']} {difficulty['difficulty']}: {difficulty['rating']}\n"
        footer = f'Enter /song {chart["song_id"]} <difficulty> to get difficulty details.'
        embed = hikari.Embed(color=color,
                            title=f'**{chart["name_en"]}**',
                            description=description)
        embed.set_author(name="Chart Details")
        embed.set_footer(text=footer)
        embed.set_image(jacket)
        embed.add_field(name="Difficulties", value=field, inline=False)
        await ctx.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                embed
        )
        
        return
    elif output[0] == 1: # Difficulty Search
        chart = output[1]
        jacket = hikari.File(chart['jacket_path'])
        side = await sideFormat(chart['side'])
        color = await diffColorFormat(output[2])
        description = ""
        if chart["name_jp"] != "":
            description = f'**Japanese Title:** {chart["name_jp"]}\n'
        description += f'**Artist:** {chart["artist"]}\n**Illustration:** {chart["jacket_designer"]}\n**Duration:** {chart["time"]}\n**BPM:** {chart["bpm"]}\n**Side:** {side[0]}\n**Pack:** {chart["set_friendly"]}'
        field = f'**CC:** {chart["rating"]}\n**Chart Design:** {chart["chart_designer"]}\n**Notes:** {chart["note"]}'
        embed = hikari.Embed(color=color,
                            title=f'**{chart["name_en"]}**',
                            description=description)
        embed.set_author(name="Chart Details")
        embed.set_image(jacket)
        embed.add_field(name=f'{chart["difficulty_name"]} {chart["difficulty"]}', value=field)
        await ctx.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                embed
        )
        return
    elif output[0] == 2: # Constant Search
        songs = output[1]
        chart = ''
        title = 'Songs Found'
        if len(songs) == 1:
            title = 'Song Found'
        for song in songs:
            chart += f"- **{song['name_en']}** ({song['difficulty_name']})\n"
        embed = hikari.Embed(title=title, description=chart, color='#eae9e0')
        embed.set_author(name=str(float(query)))
        await ctx.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                embed,
                flags=hikari.MessageFlag.EPHEMERAL,
        )
        return
    
@tenniel.command
@lightbulb.option("layout", "Choose the layout",
                  choices=["LxBot Full", "LxBot Simple", "Official"])
@lightbulb.command("b30", "Generate your best 30 scores.")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_b30(ctx: lightbulb.SlashCommand) -> None:
    channel_id = ctx.channel_id
    user_id = ctx.author.id
    if await check_blacklist(user_id, channel_id):
        await ctx.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                "This command is not allowed in this channel.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
        return
    layout = ctx.options.layout
    user_name = ctx.author.username
    print(f'{user_name}: Requested their B30.')
    if layout in ["LxBot Full", "Official"]:
        await ctx.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                "Haven't made that yet lol. Use LxBot Simple.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
        return
    await ctx.interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    try:
        b30 = await b30Generate(user_id, layout)
    except Exception as e:
        print(e)
        embed = hikari.Embed(title=type(e).__name__,description=e.args[0] , color='#cc0000')
        await ctx.interaction.edit_initial_response(embed)
        await sleep(5)
        await ctx.interaction.delete_initial_response()
        return
    f = hikari.File(b30)
    embed = hikari.Embed(title="", color='#eae9e0')
    embed.set_author(name='Inquiry Result')
    embed.set_image(f)
    await ctx.interaction.edit_initial_response(embed)
    

@tenniel.command
@lightbulb.option("hidden",
                  "Show or hide the outcome message.",
                  choices=["True", "False"],
                  required=False,
                  default="False")
@lightbulb.option("details",
                  "Get Potential details.",
                  choices=["Show", "Hide"],
                  required=False,
                  default="Hide")
@lightbulb.option("submit",
                  "Save the score to your B30.",
                  choices=["Save", "Don't save"],
                  required=False,
                  default="Save")
@lightbulb.option("score", "Enter the score for the song.",
                  type=str)
@lightbulb.option("difficulty",
                  "Enter the difficulty of the song.",
                  choices=["Past", "Present", "Future", "Beyond"],
                  type=str)
@lightbulb.option("chart", "Enter the song name.", autocomplete=True,)
@lightbulb.command("result", "Calculate the result of a play.")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_result(ctx: lightbulb.SlashCommand) -> None:
    channel_id = ctx.channel_id
    user_id = ctx.author.id
    user_name = ctx.author.username
    chartStr = ctx.options.chart
    score = ctx.options.score
    score = score.translate(str.maketrans("", "", " ,.-'"))
    try:
        score = int(score)
        if score < 1000000 or score > 10002221:
            raise Exception("InvalidScoreError")
    except Exception:
        await ctx.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                hikari.Embed(title="InvalidScoreError", description="Please enter a valid score.", color='#cc0000'),
                flags=hikari.MessageFlag.EPHEMERAL,
            )
        return
        
    diffStr = ctx.options.difficulty
    hidden = bool(ctx.options.hidden)
    details = ctx.options.details
    submit = ctx.options.submit
    try:
        output = await result(chartStr, diffStr, score, user_id, submit)
    except Exception as e:
        print(e)
        embed = hikari.Embed(title=type(e).__name__,description=e.args[0] , color='#cc0000')
        await ctx.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                embed,
                flags=hikari.MessageFlag.EPHEMERAL,
            )
        return
    song_name = output["name_en"]
    diff_name = output["difficulty"]
    rating = output["rating"]
    cc = output["constant"]
    score_str = output["score"]
    jacket_path = output["jacket"]
    old_ptt = output["old_ptt"]
    new_ptt = output["new_ptt"]
    has_improved = output["has_improved"]
    rank = output["play_rank"]
    color = await diffColorFormat(output["diff_index"])
    jacket = hikari.File(jacket_path)
    embed = hikari.Embed(color=color,
                        description=f'**{song_name}**\n{score_str}\n{diff_name} {cc} > {rating}')
    embed.set_thumbnail(jacket)
    if submit == "Save":
        print(f'{user_name}: Saved a score for "{song_name}" with the score: {score_str} ({rating})')
        if details == "Show" and cc > 0:
            if has_improved:
                embed.add_field(
                    name="Details",
                    value=
                    f"This score is now your top **#{rank}** score.\nBest 30 average: {old_ptt} > **{new_ptt}**."
                )
            else:
                embed.add_field(
                    name="Details",
                    value=
                    f"This score did not make it to your Best 30 scores.\nBest 30 average: **{new_ptt}**."
                )
        if cc > 0:
            embed.set_author(name="Result")
        elif cc == 0:
            embed.set_author(name="Not saved. Chart costant is unavailable.")
        else:
            embed.set_author(name="Not saved. This chart cannot give Potential.")
    else:
        print(f'{user_name}: Did not save a score for "{song_name}" with the score: {score_str} ({rating})')
        embed.set_author(name="Result (Not saved)")

    if hidden or await check_blacklist(user_id, channel_id):
        await ctx.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            embed,
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return
    await ctx.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            embed,
    )
    return

@tenniel.command
# @lightbulb.add_checks(lightbulb.Check(check_author_is_me)) I don't use check.
@lightbulb.command("reload", "Reload files. (For development only)")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_reload(ctx: lightbulb.SlashCommand) -> None:
    if await check_is_me(ctx.author.id):
        await ctx.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            "You are not allowed to use this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return
    await reload()
    loadAuto()
    await ctx.interaction.create_initial_response(
        hikari.ResponseType.MESSAGE_CREATE,
        hikari.Embed(title="Reloaded", description="Cleared cached files.", color='#eae9e0'),
        flags=hikari.MessageFlag.EPHEMERAL,
    )
    return

@tenniel.command
@lightbulb.command("recommend", "Get a chart recommendation.")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_recom(ctx: lightbulb.SlashCommand) -> None:
    channel = ctx.channel_id
    if await check_blacklist(ctx.author.id, channel):
        await ctx.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            "This command is not allowed in this channel.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return
    time_now = time.time()
    output = await generate()
    global recommended_channels
    recommended_channels[channel] = int(time_now)
    await ctx.interaction.create_initial_response(
        hikari.ResponseType.MESSAGE_CREATE,
        output
    )
    

@cmd_result.autocomplete('chart')
@cmd_song.autocomplete('chart')
async def autocomplete_chart(
    opt: hikari.AutocompleteInteractionOption, 
    inter: hikari.AutocompleteInteraction
) -> None:
    current_input = opt.value
    output = await chart_autocomplete(current_input)
    return output

tenniel.run(status=hikari.Status.ONLINE,
        activity=hikari.Activity(
            name="Arcaea",
            type=hikari.ActivityType.PLAYING,
        ))