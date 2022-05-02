import discord
import helpers

CONST_EMPTY_CHAR = chr(173)

async def merge(message, id_to_channel, role_to_id, guild):
    args = message.content.split(" ")
    num_of_args = len(args)
    error_type = ""

    # check if $merge command input is invalid
    if num_of_args != 4:
        error_type = "$merge needs 4 args"
    elif num_of_args == 4 and not valid_channel(args[1], id_to_channel):
        error_type = f'"{args[1]}" is not a valid channel'
    elif num_of_args == 4 and args[2] != '->':
        error_type = '"->" missing between channels'
    elif num_of_args == 4 and not valid_channel(args[3], id_to_channel):
        error_type = f'"{args[3]}" is not a valid channel'
    
    #if command is invalid
    if error_type:
        embed=discord.Embed(title="INVALID COMMAND: $merge", description = "Error: " + error_type + "\n" + CONST_EMPTY_CHAR, color=discord.Color.red())
        embed.add_field(name='Did you mean:', value = '*$merge #channel -> #channel*', inline=False)
        await message.channel.send(embed=embed)
        return {}

    #if command is valid
    else:
        
        #alpha channel/role = channel/role that is staying
        #beta channel/role = channel/role that is being closed. Users move to alpha channel/role
        
        alpha_channel_id = helpers.get_integers_of_string(args[3])
        beta_channel_id = helpers.get_integers_of_string(args[1])

        alpha_role_name = id_to_channel.get(alpha_channel_id).replace("-", " ")
        beta_role_name = id_to_channel.get(beta_channel_id).replace("-", " ")

        alpha_role_id = role_to_id.get(alpha_role_name)
        beta_role_id = role_to_id.get(beta_role_name)

        #if alpha channel's corresponding role doesn't exist
        if alpha_role_id is None:
            embed=discord.Embed(title="ERROR: $merge", description = f'Error: could not find role with name "{alpha_role_name}"', color=discord.Color.red())
            await message.channel.send(embed=embed)
            return {}
        #if beta channel's corresponding role doesn't exist
        elif beta_role_id is None:
            embed=discord.Embed(title="ERROR: $merge", description = f'Error: could not find role with name "{beta_role_name}"', color=discord.Color.red())
            await message.channel.send(embed=embed)
            return {}
        #if corresponding roles exist
        else:

            alpha_role = discord.utils.get(guild.roles, id=alpha_role_id)
            beta_role = discord.utils.get(guild.roles, id=beta_role_id)

            # get beta channel users to be moved's ids
            moved_users_list = [f'<@{member.id}>' for member in beta_role.members]

            # show merge info preview - user still needs to confirm merge before it goes through
            embed_preview=discord.Embed(title="SUCCESSFUL COMMAND: $merge", description = f'<@&{beta_role.id}> -> <@&{alpha_role.id}>', color=discord.Color.green())
            embed_preview.add_field(name= f'Total users to be given role ({len(moved_users_list)})', value = f"<@&{alpha_role.id}>", inline=False)
            embed_preview.add_field(name = "Users to be given role", value = "\n".join(moved_users_list) if len(moved_users_list)>0 else "N/A", inline= False)
            embed_preview.add_field(name = f'Message to {beta_role}', value = f'> A HTCTW team member has merged your channel into <#{alpha_channel_id}>! Please head over to <#{alpha_channel_id}> now!\n\n> This channel has been **DISCONTINUED**. Please head over to <#{alpha_channel_id}>', inline = False)
            embed_preview.add_field(name = f'Message to {alpha_role}', value = f'> A HTCTW team member has merged {beta_role} into your channel! Make sure to welcome your fellow participants :)', inline = False)
            embed_preview.add_field(name = "MERGE?", value = '> Type $confirm to confirm merge, $cancel to cancel', inline=False)
            await message.channel.send(embed=embed_preview)

            return {"moved_users_list": moved_users_list, "alpha_role": alpha_role, "beta_role": beta_role, "alpha_channel_id": alpha_channel_id, "beta_channel_id": beta_channel_id}

async def confirm(message, scheduled_merge_info, guild):
    # if there is a scheduled merge
    if scheduled_merge_info:
        alpha_role = scheduled_merge_info.get('alpha_role')
        beta_role = scheduled_merge_info.get('beta_role')
        alpha_channel_id = scheduled_merge_info.get('alpha_channel_id')
        beta_channel_id = scheduled_merge_info.get('beta_channel_id')
        moved_users_list = scheduled_merge_info.get('moved_users_list')

        # add alpha role to beta users
        for member in beta_role.members:
            await member.add_roles(alpha_role)

        # send appropriate messages
        embed_alpha = discord.Embed(title="EXPECT SOME NEW FRIENDS!", description = f'A HTCTW team member has merged {beta_role} into your channel! Make sure to welcome your fellow participants :)', color=discord.Color.green())
        await guild.get_channel(alpha_channel_id).send(embed = embed_alpha)

        embed_beta = discord.Embed(title="CHANNEL MERGE", description = f'A HTCTW team member has merged your channel into <#{alpha_channel_id}>!\n\nPlease head over to <#{alpha_channel_id}> now!', color=discord.Color.purple())
        embed_close = discord.Embed(title="WARNING", description = f'This channel has been **DISCONTINUED**. Head over to <#{alpha_channel_id}>', color=discord.Color.red())
        await guild.get_channel(beta_channel_id).send(embed=embed_beta)
        await guild.get_channel(beta_channel_id).send(embed=embed_close)

        embed=discord.Embed(title="SUCCESSFUL COMMAND: $merge", description = f'<@&{beta_role.id}> -> <@&{alpha_role.id}>', color=discord.Color.green())
        embed.add_field(name= f'Total users given role ({len(moved_users_list)})', value = f"<@&{alpha_role.id}>", inline=False)
        embed.add_field(name = "Users given role", value = "\n".join(moved_users_list) if len(moved_users_list)>0 else "N/A", inline= False)
        await message.channel.send(embed = embed)

    #if no merge scheduled
    else:

        embed=discord.Embed(title="WARNING: $MERGE FAILED", color=discord.Color.red())
        await message.channel.send(embed = embed)
    
    return


def valid_channel(string, id_to_channel):
    if any(str(valid_channel) in string for valid_channel in list(id_to_channel.keys())): return True
    else: return False