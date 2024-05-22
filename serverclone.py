import discord
import asyncio
from colorama import Fore, Style

def print_add(message):
    print(f'{Fore.GREEN}[+]{Style.RESET_ALL} {message}')

def print_delete(message):
    print(f'{Fore.RED}[-]{Style.RESET_ALL} {message}')

def print_warning(message):
    print(f'{Fore.RED}[WARNING]{Style.RESET_ALL} {message}')

def print_error(message):
    print(f'{Fore.RED}[ERROR]{Style.RESET_ALL} {message}')

class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            if role.name != "@everyone":
                try:
                    await role.delete()
                    print_delete(f"Deleted Role: {role.name}")
                except discord.Forbidden as e:
                    print_error(f"Error While Deleting Role: {role.name} - {e}")
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.retry_after
                        print_warning(f"Rate limit exceeded. Waiting for {retry_after:.2f} seconds.")
                        await asyncio.sleep(retry_after)
                        await role.delete()
                    else:
                        print_error(f"HTTP error while deleting role: {role.name} - {e}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for role in guild_from.roles:
            if role.name != "@everyone":
                try:
                    await guild_to.create_role(
                        name=role.name,
                        permissions=role.permissions,
                        colour=role.colour,
                        hoist=role.hoist,
                        mentionable=role.mentionable
                    )
                    print_add(f"Created Role {role.name}")
                except discord.Forbidden as e:
                    print_error(f"Error While Creating Role: {role.name} - {e}")
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.retry_after
                        print_warning(f"Rate limit exceeded. Waiting for {retry_after:.2f} seconds.")
                        await asyncio.sleep(retry_after)
                        await guild_to.create_role(
                            name=role.name,
                            permissions=role.permissions,
                            colour=role.colour,
                            hoist=role.hoist,
                            mentionable=role.mentionable
                        )
                        print_add(f"Created Role {role.name} after rate limit wait.")
                    else:
                        print_error(f"HTTP error while creating role: {role.name} - {e}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(f"Deleted Channel: {channel.name}")
            except discord.Forbidden as e:
                print_error(f"Error While Deleting Channel: {channel.name} - {e}")
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after
                    print_warning(f"Rate limit exceeded. Waiting for {retry_after:.2f} seconds.")
                    await asyncio.sleep(retry_after)
                    await channel.delete()
                    print_delete(f"Deleted Channel: {channel.name} after rate limit wait.")
                else:
                    print_error(f"HTTP error while deleting channel: {channel.name} - {e}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for category in guild_from.categories:
            try:
                overwrites_to = {}
                for key, value in category.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                new_category = await guild_to.create_category(
                    name=category.name,
                    overwrites=overwrites_to
                )
                await new_category.edit(position=category.position)
                print_add(f"Created Category: {category.name}")
            except discord.Forbidden as e:
                print_error(f"Error While Creating Category: {category.name} - {e}")
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after
                    print_warning(f"Rate limit exceeded. Waiting for {retry_after:.2f} seconds.")
                    await asyncio.sleep(retry_after)
                    await guild_to.create_category(
                        name=category.name,
                        overwrites=overwrites_to
                    )
                    print_add(f"Created Category: {category.name} after rate limit wait.")
                else:
                    print_error(f"HTTP error while creating category: {category.name} - {e}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for channel in guild_from.text_channels:
            try:
                category = None
                if channel.category is not None:
                    category = discord.utils.get(guild_to.categories, name=channel.category.name)
                overwrites_to = {}
                if channel.overwrites:
                    for key, value in channel.overwrites.items():
                        if isinstance(key, discord.Role):
                            target = discord.utils.get(guild_to.roles, name=key.name)
                            if target:
                                overwrites_to[target] = value
                new_channel = await guild_to.create_text_channel(
                    name=channel.name,
                    overwrites=overwrites_to,
                    position=channel.position,
                    topic=channel.topic,
                    slowmode_delay=channel.slowmode_delay,
                    nsfw=channel.nsfw,
                    category=category
                )
                print_add(f"Created Text Channel: {channel.name}")
            except discord.Forbidden as e:
                print_error(f"Error While Creating Text Channel: {channel.name} - {e}")
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after
                    print_warning(f"Rate limit exceeded. Waiting for {retry_after:.2f} seconds.")
                    await asyncio.sleep(retry_after)
                    await guild_to.create_text_channel(
                        name=channel.name,
                        overwrites=overwrites_to,
                        position=channel.position,
                        topic=channel.topic,
                        slowmode_delay=channel.slowmode_delay,
                        nsfw=channel.nsfw,
                        category=category
                    )
                    print_add(f"Created Text Channel: {channel.name} after rate limit wait.")
                else:
                    print_error(f"HTTP error while creating text channel: {channel.name} - {e}")

        for channel in guild_from.voice_channels:
            try:
                category = None
                if channel.category is not None:
                    category = discord.utils.get(guild_to.categories, name=channel.category.name)
                overwrites_to = {}
                if channel.overwrites:
                    for key, value in channel.overwrites.items():
                        if isinstance(key, discord.Role):
                            role = discord.utils.get(guild_to.roles, name=key.name)
                            if role:
                                overwrites_to[role] = value
                new_channel = await guild_to.create_voice_channel(
                    name=channel.name,
                    overwrites=overwrites_to,
                    position=channel.position,
                    bitrate=channel.bitrate,
                    user_limit=channel.user_limit,
                    category=category
                )
                print_add(f"Created Voice Channel: {channel.name}")
            except discord.Forbidden as e:
                print_error(f"Error While Creating Voice Channel: {channel.name} - {e}")
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after
                    print_warning(f"Rate limit exceeded. Waiting for {retry_after:.2f} seconds.")
                    await asyncio.sleep(retry_after)
                    await guild_to.create_voice_channel(
                        name=channel.name,
                        overwrites=overwrites_to,
                        position=channel.position,
                        bitrate=channel.bitrate,
                        user_limit=channel.user_limit,
                        category=category
                    )
                    print_add(f"Created Voice Channel: {channel.name} after rate limit wait.")
                else:
                    print_error(f"HTTP error while creating voice channel: {channel.name} - {e}")

    @staticmethod
    async def emojis_delete(guild_to: discord.Guild):
        for emoji in guild_to.emojis:
            try:
                await emoji.delete()
                print_delete(f"Deleted Emoji: {emoji.name}")
            except discord.Forbidden as e:
                print_error(f"Error While Deleting Emoji {emoji.name} - {e}")
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after
                    print_warning(f"Rate limit exceeded. Waiting for {retry_after:.2f} seconds.")
                    await asyncio.sleep(retry_after)
                    await emoji.delete()
                    print_delete(f"Deleted Emoji: {emoji.name} after rate limit wait.")
                else:
                    print_error(f"HTTP error while deleting emoji: {emoji.name} - {e}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for emoji in guild_from.emojis:
            try:
                emoji_image = await emoji.url.read()
                await guild_to.create_custom_emoji(
                    name=emoji.name,
                    image=emoji_image
                )
                print_add(f"Created Emoji {emoji.name}")
            except discord.Forbidden as e:
                print_error(f"Error While Creating Emoji {emoji.name} - {e}")
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after
                    print_warning(f"Rate limit exceeded. Waiting for {retry_after:.2f} seconds.")
                    await asyncio.sleep(retry_after)
                    await guild_to.create_custom_emoji(
                        name=emoji.name,
                        image=emoji_image
                    )
                    print_add(f"Created Emoji {emoji.name} after rate limit wait.")
                else:
                    print_error(f"HTTP error while creating emoji: {emoji.name} - {e}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            icon_image = await guild_from.icon.read()
            await guild_to.edit(name=guild_from.name, icon=icon_image)
            print_add(f"Guild Icon Changed: {guild_to.name}")
        except discord.Forbidden as e:
            print_error(f"Error While Changing Guild Icon: {guild_to.name} - {e}")
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = e.retry_after
                print_warning(f"Rate limit exceeded. Waiting for {retry_after:.2f} seconds.")
                await asyncio.sleep(retry_after)
                await guild_to.edit(name=guild_from.name, icon=icon_image)
                print_add(f"Guild Icon Changed: {guild_to.name} after rate limit wait.")
            else:
                print_error(f"HTTP error while changing guild icon: {guild_to.name} - {e}")
        except Exception as e:
            print_error(f"Unexpected Error: {e}")