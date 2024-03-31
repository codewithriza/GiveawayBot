# Giveaway Bot

Giveaway Bot is a Discord bot designed to facilitate giveaways on your server. It allows you to easily set up and manage giveaways with customizable options.

## Features

- Start a giveaway in any channel.
- Specify the prize for the giveaway.
- Set the duration of the giveaway.
- Reroll the winner of a giveaway.

## Commands

- `g!help`: Displays a list of available commands and their descriptions.
- `g!giveaway`: Starts a giveaway. Requires the "Giveaway Host" role.
- `g!reroll #channel_name message_id`: Rerolls the winner of a giveaway. Requires the "Giveaway Host" role.

## Installation

1. Clone the repository.
2. Install the dependencies with `pip install -r requirements.txt`.
3. Create a `.env` file with your bot token and admin role ID:

```bash
TOKEN=
ADMIN_ROLE_ID=
```


4. Run the bot with `python3 bot.py`.

## Usage

To start a giveaway, use the `g!giveaway` command. Follow the prompts to set up the giveaway, including the channel, prize, and duration.

## Contributing

Contributions are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
