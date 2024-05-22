import discord
import asyncio
from PyQt5.QtWidgets import QApplication
from gui import ServerCloneGUI
from serverclone import Clone

class DiscordCloner(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None
        self.input_guild_id = None
        self.output_guild_id = None

    async def on_ready(self):
        print('Logged on as', self.user)
        await self.run_clone()

    async def run_clone(self):
        guild_from = self.get_guild(int(self.input_guild_id))
        guild_to = self.get_guild(int(self.output_guild_id))
        await Clone.guild_edit(guild_to, guild_from)
        await Clone.roles_delete(guild_to)
        await Clone.channels_delete(guild_to)
        await Clone.roles_create(guild_to, guild_from)
        await Clone.categories_create(guild_to, guild_from)
        await Clone.channels_create(guild_to, guild_from)
        await asyncio.sleep(5)
        await self.close()

def main():
    client = DiscordCloner()
    app = QApplication([])
    gui = ServerCloneGUI(client)
    gui.show()
    app.exec_()

if __name__ == "__main__":
    main()