import shlex
import discord
import pprint

import helpers

CONST_EMPTY_CHAR = chr(173)

async def schedule(message, scheduled_messages_list, ID, id_to_channel):

    #check if proper $schedule command input
    try: 
        args = shlex.split(message.content, posix=False)
    except:
        embed=discord.Embed(title="INVALID COMMAND: $schedule", description = "Error: no closing quotations", color=discord.Color.red())
        await message.channel.send(embed=embed)
        return (ID, scheduled_messages_list)
            
    error_type = ""
    # error checking
    if len(args)!=5 and len(args)!=7:
        error_type = "$schedule needs 5 args or 7 args"
    elif not args[1].startswith('"') or not args[1].endswith('"'):
        error_type = "message needs to be wrapped in quotation marks -> " + args[1]
    elif not helpers.check_valid_datetime(args[2] + " " + args[3]):
        error_type = f'invalid datetime -> "{args[2]} {args[3]}"'
    elif not valid_channel(args[4], id_to_channel):
        error_type = f'channel could not be found -> "{args[4]}"'
    elif len(args) == 7 and not args[5].isdigit():
        error_type = f'repetition count must be an integer -> "{args[5]}"'
    elif len(args) == 7 and not helpers.valid_interval(args[6]):
        error_type = f'not a valid interval -> "{args[6]}"'

    #if there's an error
    if error_type:
        embed=discord.Embed(title="INVALID COMMAND: $schedule", description = "Error: " + error_type + "\n" + CONST_EMPTY_CHAR, color=discord.Color.red())
        embed.add_field(name='Did you mean:', value = '*$schedule\t"your message here"\tYYYY-MM-DD\tHH:MM\t#textchannel*\n\n**Multiple reminders:**\n *$schedule\t"your message here"\tYYYY-MM-DD\tHH:MM\t#textchannel\t#\t#d/h/m*', inline=False)
        await message.channel.send(embed=embed)
        return (ID, scheduled_messages_list)

    #if valid command
    else:

        user_message = args[1][1:-1]
        user_datetime_input = args[2] + " " + args[3]
        channel_id = helpers.get_integers_of_string(args[4])

        ID_list = [ID]

        datetime_list = [helpers.get_valid_datetime(user_datetime_input)]

        # if user wanted to schedule multiple messages
        if len(args) == 7:
            
            num_of_repeats = int(args[5])
            time_interval = args[6]

            #store IDs and datetimes for specified # of repeats and interval between repeats
            for iteration in range(num_of_repeats-1):
                new_date = helpers.add_time_to_datetime(datetime_list[-1], time_interval)
                datetime_list.append(new_date)
                ID_list.append(ID_list[-1] + 1)

        #format datetime so it's easier to read (without the seconds)
        datetime_list = [helpers.datetime_to_string_no_seconds(x) for x in datetime_list]    

        #updated scheduled reminders list
        for index in range(len(ID_list)):
            scheduled_messages_list.append({"id": ID_list[index], "message": user_message, "datetime": datetime_list[index], "channel": channel_id})
        scheduled_messages_list = sorted(scheduled_messages_list, key=lambda x: x['datetime'])

        ID = ID_list[-1] + 1

        # successful command
        embed=discord.Embed(title="SUCCESSFUL COMMAND: $schedule\n" + CONST_EMPTY_CHAR, color=discord.Color.dark_green())
        embed.add_field(name='MESSAGE:', value = user_message + "\n" + CONST_EMPTY_CHAR, inline=False)
        embed.add_field(name='ID:', value = "\n".join([str(id) for id in ID_list]) + "\n" + CONST_EMPTY_CHAR, inline=False)
        embed.add_field(name='DATETIME', value = "\n".join([x + " EST" for x in datetime_list]) + "\n" + CONST_EMPTY_CHAR, inline=False)
        embed.add_field(name='CHAT:', value = f'<#{channel_id}>', inline=False)
        await message.channel.send(embed=embed)

        pprint.pprint(scheduled_messages_list)
        
        return (ID, scheduled_messages_list)

def valid_channel(string, id_to_channel):
    if any(str(valid_channel) in string for valid_channel in list(id_to_channel.keys())): return True
    else: return False