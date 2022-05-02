import discord
import helpers

CONST_EMPTY_CHAR = chr(173)

async def delete(message, scheduled_messages_list):
    args = message.content.split(" ")

    # check if $delete command is invalid
    if len(args)!=2 or not args[1].isdigit():
        embed=discord.Embed(title="INVALID COMMAND: *$delete*", description = "Please follow the syntax below:\n" + CONST_EMPTY_CHAR, color=discord.Color.red())
        embed.add_field(name="Did you mean:", value = '$delete #', inline=False) 
        await message.channel.send(embed=embed)
        return scheduled_messages_list

    #if valid $delete command
    else:
        id_to_be_deleted = helpers.get_integers_of_string(args[1])
        # loop through all scheduled reminders and delete if reminder id = id to be deleted
        for index in range(len(scheduled_messages_list)):
            message_info = scheduled_messages_list[index]
            if message_info.get('id') == id_to_be_deleted:
                embed=discord.Embed(title="SUCCESSFULLY REMOVED MESSAGE\n" + CONST_EMPTY_CHAR, color=discord.Color.green())
                embed.add_field(name='MESSAGE:', value = message_info.get('message') + "\n" + CONST_EMPTY_CHAR, inline=False)
                embed.add_field(name='ID:', value = str(message_info.get('id')) + "\n" + CONST_EMPTY_CHAR, inline=False)
                embed.add_field(name='DATETIME:', value = message_info.get('datetime') + " EST\n" + CONST_EMPTY_CHAR, inline=False)
                embed.add_field(name='CHAT:', value = f'<#{message_info.get("channel")}>', inline=False)
                await message.channel.send(embed=embed)
                scheduled_messages_list.pop(index)
                return scheduled_messages_list
        
        # if id to be deleted not found 
        embed=discord.Embed(title="COULD NOT FIND MESSAGE WITH ID " + str(id_to_be_deleted), color=discord.Color.red())
        await message.channel.send(embed=embed)
        return scheduled_messages_list