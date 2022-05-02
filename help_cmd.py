import discord

CONST_EMPTY_CHAR = chr(173)

# show all Discord bot commands
async def help(message, admin):
    embed=discord.Embed(title="CHRONOS COMMANDS", color=discord.Color.red())
    if admin:
        embed.add_field(name="**$attendance**", value = 'For taking attendance based on presence in a voice channel. Attendance can be limited to a role if specified, otherwise it will be an @everyone attendance.\n\n> *$attendance*\n> *$attendance @rolehere*\n' + CONST_EMPTY_CHAR, inline=False) 
        embed.add_field(name="**$schedule**", value = 'Schedules a message to be sent to a channel at a specific datetime.\n\nIf working with the 7 argument $schedule command:\n [int] = number of time message repeats (ex: 3)\n[interval] = time between messages in #d/h/m (ex: 20m)\n\n> *$schedule [“message”] [YYYY-MM-DD] [HH:MM] [#channel] *\n> *$schedule [“message”] [YYYY-MM-DD] [HH:MM] [#channel] [int] [interval]*\n' + CONST_EMPTY_CHAR, inline=False) 
        embed.add_field(name="**$reminders**", value = 'Show all or # of currently scheduled messages.\n\n> *$reminders*\n> *$reminders #*\n' + CONST_EMPTY_CHAR, inline=False) 
        embed.add_field(name="**$delete**", value = 'Deletes scheduled message with ID #.\n\n> *$delete #*\n' + CONST_EMPTY_CHAR, inline=False) 
        embed.add_field(name="**$merge**", value = 'Merges 2 channels (of type #team-x-y or #open-innovation-table-x). Displaced users are given #channel_2\'s unique role.\n\n> *$merge #channel_1 → #channel_2*\n' + CONST_EMPTY_CHAR, inline=False) 
        embed.add_field(name="**$set_zoom**", value = 'Sets zoom link for $zoom.\n\n> *$set_zoom link*\n' + CONST_EMPTY_CHAR, inline=False) 

    embed.add_field(name="**$zoom**", value = 'Uploads Zoom link.\n\n> *$zoom*\n' + CONST_EMPTY_CHAR, inline=False) 
    embed.add_field(name="**$background**", value = 'Uploads Zoom background to Discord for users to download.\n\n> *$background*\n' + CONST_EMPTY_CHAR, inline=False) 
    embed.add_field(name="**$program**", value = 'Uploads program schedule for current day.\n\n> *$program*\n' + CONST_EMPTY_CHAR, inline=False) 
    if admin: embed.add_field(name=CONST_EMPTY_CHAR, value = "For more information check out [Chronos Documentation](https://www.notion.so/how-to-change-the-world/Discord-Bot-Chronos-Commands-Documentation-WIP-f4790d44748b49769a961dab630f8a8d)")
    await message.channel.send(embed=embed)