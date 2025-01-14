"""
Author @Firefly#7113
Help and info
"""

import discord
from discord import slash_command, option
from discord.ext import commands


# ------------------------------------------------------------------------
# COMPONENT CLASSES AND CONSTANTS
# ------------------------------------------------------------------------
HELP_EMBEDS = {
	"Info": {
		"Description": "All command descriptions and instructions can be found by typing `/`into discord and selecting UA in the menu! Parameter hints are also provided by selecting the parameter's box. Use this menu to see overviews and command categories. If anything is unclear or buggy, feel free to ask in the developer's server.",
		"Fields": {
			"Full Instructions": "[Github](https://github.com/Firefly042). Stars and contributions are welcome!",

			"Questions, Answers, and Suggestions": "[Discord Server](https://discord.gg/VZYKBptWFJ)",

			"Support the Developer": "[Ko-fi](https://ko-fi.com/firefly42)",

			"Commissions": "[I can make other things too.](https://docs.google.com/document/d/1kM7qFBWqGsHktgrQHdCSf0HYJCfrTAa9MVsGPE8xF6A/edit?usp=sharing)",

			"Basic Usage": "1. Set application permissions for moderator and player roles in your server settings (Integrations). Here's an official [guide](https://discord.com/blog/slash-commands-permissions-discord-apps-bots) from Discord.\n\n2. Set up character profiles with `/profile_admin` commands. If you plan to use the Messaging features, you will need designated player channels.\n\n3. Players may customize their profiles further with `/profile` commands.\n\n4. Multiple characters can be registered for a single player, but only one may be active at a time (set with `/profile swap`).",

			"Optional Parameters": "Many commands have optional arguments that may be of interest! Make note of the `visible` parameter that makes use of temporary/single-user messages."
		},
		"Footer": "This bot is written by discord user @Firefly#7113. If this code is not running on bot user 517165856933937153, it is being hosted by someone else and should only be used if you trust that person."
	},

	"Profiles": {
		"Description": "A single player may not have more than one character with the same display name. Individual associated channels are required to use Messaging commands.",
		"Fields": {
			"Admin": "`/profile_admin` - Register, remove, and disable characters. Edit names, surnames, and associated channels.",

			"Player": "`/profile` - Edit your character's embed images, fields, descriptions, and colors. View or switch your active character",

			"Public": "`/profile view|list` - View an individual profile or list all registered characters."
		}
	},

	"Gacha": {
		"Description": "All item names must be unique within a server.",
		"Fields": {
			"Admin": "`/gacha_admin` - Register items with `add`, with optional parameters to limit the amount of the item. Remove items by name with `rm`. Edit currency name or increase the cost of a single pull. Give and take currency to/from individual (active) characters or in bulk.",

			"Player": "`/gacha` - Pull from the gacha, view your currency, and give currency to another (active) character."
		}
	},

	"Inventory": {
		"Description": "Item management for players and moderators. You may hold up to 9999 of a single item (case sensitive).",
		"Fields": {
			"Admin": "`/inv_admin` - View inventories for players and give/take items.",

			"Player": "`/inv` - View and manage your own inventory, give items to another active character."
		}
	},

	"Messaging": {
		"Description": "Private and anonymous messaging for players. The latter must be enabled by a moderator, and players will need a set channel (see Profiles) to receive these messages",
		"Fields": {
			"Admin": "`/msg_admin` - Toggle anonymous messaging with `anon` command and view a list of players and channels.",

			"Player": "`/msg whisper|anon` - Send signed or anonymous messages to another active character's private channel."
		}
	},

	"Dice": {
		"Description": "Rolling with d20 notation and custom rolls",
		"Fields": {
			"Admin": "`/roll_admin list` - List rolls for a specified player",

			"Player": "`/roll` - Manage a set of up to 25 named rolls",

			"Public": "`/roll d` - Roll with normal d20 notation"
		}
	},

	"Automated Posts": {
		"Description": "A set of commands to automate regular posts such as time announcements. Be sure to set your **timezone** (`/announcements tz`)! Slash commands do not support line breaks at the time of writing.",
		"Fields": {
			"Admin": "`/announcements` - Add, remove, and view automated posts. Toggle them on or off. PAUSED announcements will still tick forward in time, but will not be posted."
		}
	},

	"Investigations": {
		"Description": "Set up investigatable objects by specifying a channel, names, and a description. Moderators may mark an item as 'stealable', which allows a player to take the item.",
		"Fields": {
			"Admin": "`/investigate_admin` - Add, remove, and view investigations. Items cannot be taken by default",

			"Player": "`/investigate` - Investigate or take an item within a channel (visible only to player by default)"
		}
	}
}


class HelpMenu(discord.ui.View):
	"""Menu of embeds and associated buttons"""

	def __init__(self, embeds, interaction):
		# Is it possible to generate button callbacks according to embed titles?
		super().__init__(timeout=120)
		self.embeds = embeds
		self.interaction = interaction


	async def on_timeout(self):
		"""Disable and stop listening for interaction"""

		self.disable_all_items()
		await self.interaction.edit_original_message(view=self)


	# Row 0 - Info, Profiles, Gacha, Inventory
	@discord.ui.button(label="Info", row=0, style = discord.ButtonStyle.green)
	async def info_button_callback(self, _, interaction):
		await interaction.response.edit_message(embed=self.embeds["Info"], view=self)

	# Row 0 - Info, Profiles, Gacha, Inventory
	@discord.ui.button(label="Profiles", row=0, style = discord.ButtonStyle.green)
	async def profile_button_callback(self, _, interaction):
		await interaction.response.edit_message(embed=self.embeds["Profiles"], view=self)

	# Row 0 - Info, Profiles, Gacha, Inventory
	@discord.ui.button(label="Gacha", row=0, style = discord.ButtonStyle.green)
	async def gacha_button_callback(self, _, interaction):
		await interaction.response.edit_message(embed=self.embeds["Gacha"], view=self)

	# Row 0 - Info, Profiles, Gacha, Inventory
	@discord.ui.button(label="Inventory", row=0, style = discord.ButtonStyle.green)
	async def inventory_button_callback(self, _, interaction):
		await interaction.response.edit_message(embed=self.embeds["Inventory"], view=self)

	# Row 1 - Messaging, Dice, Automated Posts, Investigations
	@discord.ui.button(label="Messaging", row=1, style = discord.ButtonStyle.green)
	async def messaging_button_callback(self, _, interaction):
		await interaction.response.edit_message(embed=self.embeds["Messaging"], view=self)

	# Row 1 - Messaging, Dice, Automated Posts, Investigations
	@discord.ui.button(label="Dice", row=1, style = discord.ButtonStyle.green)
	async def dice_button_callback(self, _, interaction):
		await interaction.response.edit_message(embed=self.embeds["Dice"], view=self)

	# Row 1 - Messaging, Dice, Automated Posts, Investigations
	@discord.ui.button(label="Automated Posts", row=1, style = discord.ButtonStyle.green)
	async def posting_button_callback(self, _, interaction):
		await interaction.response.edit_message(embed=self.embeds["Automated Posts"], view=self)

	# Row 1 - Messaging, Dice, Automated Posts, Investigations
	@discord.ui.button(label="Investigations", row=1, style = discord.ButtonStyle.green)
	async def investigations_button_callback(self, _, interaction):
		await interaction.response.edit_message(embed=self.embeds["Investigations"], view=self)


# ------------------------------------------------------------------------
# COG
# ------------------------------------------------------------------------
def setup(bot):
	bot.add_cog(InfoPublicCog(bot))

# pylint: disable=no-self-use, unnecessary-dict-index-lookup
class InfoPublicCog(commands.Cog):
	"""Information commands"""

	def __init__(self, bot):
		self.bot = bot

		# Initiate embeds to pass into View
		self.embeds = {}
		for (embed_title, _) in HELP_EMBEDS.items():
			embed = discord.Embed(title=embed_title)
			embed.description = HELP_EMBEDS[embed_title]["Description"]

			for (field, content) in HELP_EMBEDS[embed_title]["Fields"].items():
				embed.add_field(name=field, value=content, inline=False)

			try:
				embed.set_footer(text=HELP_EMBEDS[embed_title]["Footer"])
			except KeyError:
				pass

			self.embeds[embed_title] = embed

		print(f"Added {self.__class__.__name__}")


# ------------------------------------------------------------------------
# Commands
# ------------------------------------------------------------------------
	@slash_command(name="help", guild_only=False)
	@option("visible", bool, default=False, description="Set True for public response")
	async def help(self, ctx, visible):
		"""Helpful information and links"""

		await ctx.respond(embed=self.embeds["Info"], view=HelpMenu(self.embeds, ctx.interaction), ephemeral=not visible)
