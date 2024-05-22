import discord
import asyncio
from serverclone import Clone

client = discord.Client()

token = input('\n[>]  Enter your Discord token: ')
guild_s = input('\n[>]  Server to Copy ID: ')
guild = input('\n[>]  Your Server ID: ')
input_guild_id = guild_s
output_guild_id = guild

@client.event
async def on_ready():
    guild_from = client.get_guild(int(input_guild_id))
    guild_to = client.get_guild(int(output_guild_id))
    await Clone.guild_edit(guild_to, guild_from)
    await Clone.roles_delete(guild_to)
    await Clone.channels_delete(guild_to)
    await Clone.roles_create(guild_to, guild_from)
    await Clone.categories_create(guild_to, guild_from)
    await Clone.channels_create(guild_to, guild_from)
    await asyncio.sleep(5)
    await client.close()

client.run(token)