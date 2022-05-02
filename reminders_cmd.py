import discord

CONST_EMPTY_CHAR = chr(173)

async def reminders(message, scheduled_messages_list):

    args = message.content.split(" ")
    num_of_args = len(args)

    #error checking
    if len(scheduled_messages_list) == 0:
        embed=discord.Embed(title="ERROR: NO CURRENTLY SCHEDULED MESSAGES", color=discord.Color.red())
        await message.channel.send(embed=embed)
    elif not num_of_args<=2 or (num_of_args == 2 and not args[1].isdigit()):
        embed=discord.Embed(title="INVALID COMMAND: *$reminders*", description = "Please follow the syntax below:\n" + CONST_EMPTY_CHAR, color=discord.Color.red())
        embed.add_field(name="All scheduled reminders", value = '*$reminders*', inline=False) 
        embed.add_field(name="Specific # of scheduled reminders", value = '*$reminders* #', inline=False)
        await message.channel.send(embed=embed)  
    # if valid command
    else:
        first_message = True
        reminder_count = 0

        #limit reminders shown if specified by user
        max_reminders = int(args[1]) if num_of_args == 2 else len(scheduled_messages_list)

        #chunk scheduled reminders into groups of 5 so they don't get truncated in embed
        chunked_messages_list =  [scheduled_messages_list[i:i + 5] for i in range(0, len(scheduled_messages_list), 5)]

        embed=discord.Embed(title="CURRENTLY SCHEDULED MESSAGES", color=discord.Color.dark_green())
        embed.add_field(name=CONST_EMPTY_CHAR, value = '**ID**', inline=True)
        embed.add_field(name=CONST_EMPTY_CHAR, value = '**MESSAGE**', inline=True)
        embed.add_field(name=CONST_EMPTY_CHAR, value = '**DELIVERY INFO**', inline=True)

        # loop through reminders and send them to Discord
        for five_messages in chunked_messages_list:

            #if past reminder limit stop sending messages
            if reminder_count >= max_reminders: break

            elif not first_message:
                embed=discord.Embed(title=CONST_EMPTY_CHAR, color=discord.Color.dark_green())
                embed.add_field(name=CONST_EMPTY_CHAR, value = '**ID**', inline=True)
                embed.add_field(name=CONST_EMPTY_CHAR, value = '**MESSAGE**', inline=True)
                embed.add_field(name=CONST_EMPTY_CHAR, value = '**DELIVERY INFO**', inline=True)

            for message_info in five_messages:

                reminder_count = reminder_count + 1

                if reminder_count <= max_reminders:
                    embed.add_field(name = CONST_EMPTY_CHAR, value = message_info.get('id'), inline=True)
                    embed.add_field(name = CONST_EMPTY_CHAR, value = message_info.get('message'), inline=True)
                    embed.add_field(name = CONST_EMPTY_CHAR, value = '<#{}> @ {} EST'.format(message_info.get('channel'), message_info.get('datetime')), inline=True)
                else: break

            # send reminder embed
            await message.channel.send(embed=embed)   
            first_message = False 
    return    