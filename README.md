# Discord Server Cloner

This project allows you to clone a Discord server, including its roles, channels, categories, and emojis. It uses the Discord API and the `discord.py` library to achieve this.

## Features

- **Roles Deletion and Creation**: Deletes existing roles in the target server and recreates them based on the source server.
- **Channels Deletion and Creation**: Deletes existing channels in the target server and recreates them based on the source server, including text and voice channels.
- **Categories Creation**: Ensures that categories in the target server mirror those in the source server.
- **Emojis Deletion and Creation**: Deletes existing emojis in the target server and recreates them based on the source server.
- **Guild Editing**: Updates the target server's name and icon to match the source server.

## Requirements

- Python 3.7+
- `discord.py` library
- `colorama` library

## Installation

1. Clone the repository:

```bash
git clone https://github.com/savisxss/discord-server-cloner.git
cd discord-server-cloner
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:

```bash
python main.py
```

2. Follow the prompts to input your Discord token, the ID of the server you want to clone, and the ID of your target server.

## Code Overview

### main.py

This script handles the main functionality of the bot:

- Connects to Discord using the provided token.
- Gets the source and target guilds.
- Calls cloning functions to replicate the source guild's structure in the target guild.

### serverclone.py

This module contains the `Clone` class with static methods to handle different cloning tasks:

- `roles_delete`: Deletes all roles in the target guild except `@everyone`.
- `roles_create`: Creates roles in the target guild based on the source guild.
- `channels_delete`: Deletes all channels in the target guild.
- `categories_create`: Creates categories in the target guild based on the source guild.
- `channels_create`: Creates text and voice channels in the target guild based on the source guild.
- `emojis_delete`: Deletes all emojis in the target guild.
- `emojis_create`: Creates emojis in the target guild based on the source guild.
- `guild_edit`: Updates the target guild's name and icon to match the source guild.
