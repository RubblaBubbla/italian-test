"""
Author @Firefly#7113
Commands for character registration and profile management
"""

import discord
from discord import option
from discord.commands import SlashCommandGroup
from discord.ext import commands

import db
import localization as loc


# ------------------------------------------------------------------------
# COG
# ------------------------------------------------------------------------
def setup(bot):
	bot.add_cog(ProfileAdminCog(bot))

# pylint: disable=no-self-use, too-many-arguments
class ProfileAdminCog(commands.Cog):
	"""Admin profile registration and editing"""

	def __init__(self, bot):
		self.bot = bot
		print(f"Added {self.__class__.__name__}")


# ------------------------------------------------------------------------
# Command groups
# Change the decorator to @<name>.command()
# ------------------------------------------------------------------------
	profile_admin = SlashCommandGroup("profile_admin", "Admin Profile setup")
	profile_admin_edit = profile_admin.create_subgroup("edit", "Admin profile editing")


# ------------------------------------------------------------------------
# Commands
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# /profile_admin new
# ------------------------------------------------------------------------
	@profile_admin.command(name="new",
		name_localizations=loc.command_names("profile_admin", "new"),
		description_localizations=loc.command_descriptions("profile_admin", "new"))
	@option("player", discord.Member,
		description="Who will play this character",
		name_localizations=loc.option_names("profile_admin", "new", "player"),
		description_localizations=loc.option_descriptions("profile_admin", "new", "player"))
	@option("name", str,
		description="The character's given/default name to display. 32 character max",
		name_localizations=loc.option_names("profile_admin", "new", "name"),
		description_localizations=loc.option_names("profile_admin", "new", "name"))
	@option("surname", str, default=None,
		description="The rest of the character's name, if any. 32 character max",
		name_localizations=loc.option_names("profile_admin", "new", "surname"),
		description_localizations=loc.option_names("profile_admin", "new", "surname"))
	@option("channel", discord.TextChannel, default=None,
		description="Where anonymous messages and whispers will be sent",
		name_localizations=loc.option_names("profile_admin", "new", "channel"),
		description_localizations=loc.option_names("profile_admin", "new", "channel"))
	async def profile_admin_new(self, ctx, player, name, surname, channel):
		"""Register a player, character, and name to the bot"""

		name = name[:32]
		if (surname):
			surname = surname[:32]

		if (channel):
			channel_id = channel.id
		else:
			channel_id = None

		# Add to db, catches uniqueness error
		try:
			db.new_character(ctx.guild.id, player.id, name, surname, channel_id)
		except:
			error = loc.response("profile_admin", "new", "error1", ctx.interaction.locale).format(name)
			await ctx.respond(error, ephemeral=True)
			return

		# Set it as active character for the player
		db.set_active_character(ctx.guild.id, player.id, name)

		# Discord response (success)
		if (not surname):
			surname = ""

		res = loc.response("profile_admin", "new", "res1", ctx.interaction.locale).format(name, surname)
		await ctx.respond(res)

# ------------------------------------------------------------------------
# /profile_admin edit text
# ------------------------------------------------------------------------
	@profile_admin_edit.command(name="text",
		name_localizations=loc.command_names("profile_admin_edit", "text"),
		description_localizations=loc.command_descriptions("profile_admin_edit", "text"))
	@option("player", discord.Member,
		description="Who plays this character",
		name_localizations=loc.option_names("profile_admin_edit", "text", "player"),
		description_localizations=loc.option_names("profile_admin_edit", "text", "player"))
	@option("name", str,
		description="The character's display name",
		name_localizations=loc.option_names("profile_admin_edit", "text", "name"),
		description_localizations=loc.option_names("profile_admin_edit", "text", "name"))
	@option("field_to_change", str,
		choices=["Name", "Surname"],
		description="Specify Name or Surname.",
		name_localizations=loc.option_names("profile_admin_edit", "text", "field_to_change"),
		description_localizations=loc.option_names("profile_admin_edit", "text", "field_to_change"))
	@option("new_value", str,
		description="New name or surname. 32 character maximum",
		name_localizations=loc.option_names("profile_admin_edit", "text", "new_value"),
		description_localizations=loc.option_names("profile_admin_edit", "text", "new_value"))
	async def profile_admin_edit_text(self, ctx, player, name, field_to_change, new_value):
		"""Edit a character's name or surname"""

		new_value = new_value[:32]

		# Update character, catches uniqueness error. Returns true or false if anything was changed
		try:
			char_updated = db.update_character(ctx.guild.id, player.id, name, field_to_change, new_value)
		except:
			error = loc.response("profile_admin_edit", "text", "error-duplicate", ctx.interaction.locale).format(name)
			await ctx.respond(error, ephemeral=True)
			return

		# Notify if nothing was changed (char not found)
		if (not char_updated):
			error = loc.response("profile_admin_edit", "text", "error1", ctx.interaction.locale)
			await ctx.respond(error, ephemeral=True)
			return

		# Discord response (success)
		res = loc.response("profile_admin_edit", "text", "res1", ctx.interaction.locale).format(player.name)
		await ctx.respond(res)

# ------------------------------------------------------------------------
# /profile_admin edit channel
# ------------------------------------------------------------------------
	@profile_admin_edit.command(name="channel",
		name_localizations=loc.command_names("profile_admin_edit", "channel"),
		description_localizations=loc.command_descriptions("profile_admin_edit", "channel"))
	@option("player", discord.Member,
		description="Who plays this character",
		name_localizations=loc.option_names("profile_admin_edit", "channel", "player"),
		description_localizations=loc.option_names("profile_admin_edit", "channel", "player"))
	@option("name", str,
		description="The character's display name",
		name_localizations=loc.option_names("profile_admin_edit", "channel", "name"),
		description_localizations=loc.option_names("profile_admin_edit", "channel", "name"))
	@option("channel", discord.TextChannel)
	async def profile_admin_edit_channel(self, ctx, player, name, channel):
		"""Add or edit a character's associated channel"""

		# No need to check for uniqueness because no name changes
		char_updated = db.update_character(ctx.guild.id, player.id, name, "ChannelID", channel.id)

		# Notify if nothing was changed (char not found)
		if (not char_updated):
			error = loc.response("profile_admin_edit", "channel", "error1", ctx.interaction.locale)
			await ctx.respond(error, ephemeral=True)
			return

		# Discord response (success)
		res = loc.response("profile_admin_edit", "channel", "res1", ctx.interaction.locale).format(player.name)
		await ctx.respond(res)

# ------------------------------------------------------------------------
# /profile_admin rm
# ------------------------------------------------------------------------
	@profile_admin.command(name="rm",
		name_localizations=loc.command_names("profile_admin", "rm"),
		description_localizations=loc.command_descriptions("profile_admin", "rm"))
	@option("player", discord.Member,
		description="Who played this character",
		name_localizations=loc.option_names("profile_admin", "rm", "player"),
		description_localizations=loc.option_descriptions("profile_admin", "rm", "player"))
	@option("name", str,
		description="The character's display name",
		name_localizations=loc.option_names("profile_admin", "rm", "name"),
		description_localizations=loc.option_descriptions("profile_admin", "rm", "name"))
	async def profile_admin_rm(self, ctx, player, name):
		"""Unregister a character"""

		char_removed = db.remove_character(ctx.guild.id, player.id, name)

		if (not char_removed):
			error = loc.response("profile_admin", "rm", "error1", ctx.interaction.locale)
			await ctx.respond(error, ephemeral=True)
			return

		res = loc.response("profile_admin", "rm", "res1", ctx.interaction.locale).format(name)
		await ctx.respond(res)

# ------------------------------------------------------------------------
# /profile_admin disable
# ------------------------------------------------------------------------
	@profile_admin.command(name="disable",
		name_localizations=loc.command_names("profile_admin", "disable"),
		description_localizations=loc.command_descriptions("profile_admin", "disable"))
	@option("player", discord.Member,
		description="Who plays this character",
		name_localizations=loc.option_names("profile_admin", "disable", "player"),
		description_localizations=loc.option_descriptions("profile_admin", "disable", "player"))
	@option("name", str,
		description="The character's display name",
		name_localizations=loc.option_names("profile_admin", "disable", "name"),
		description_localizations=loc.option_descriptions("profile_admin", "disable", "player"))
	async def profile_admin_disable(self, ctx, player, name):
		"""Set a character to inactive (disabling the player's ability to use commands)"""

		# No need to check for uniqueness because no name changes
		char_updated = db.update_character(ctx.guild.id, player.id, name, "Active", 0)

		# Notify if nothing was changed (char not found)
		if (not char_updated):
			error = loc.response("profile_admin", "disable", "error1", ctx.interaction.locale)
			await ctx.respond(error, ephemeral=True)
			return

		# Discord response
		res = loc.response("profile_admin", "disable", "res1", ctx.interaction.locale).format(player.name)
		await ctx.respond(res)
