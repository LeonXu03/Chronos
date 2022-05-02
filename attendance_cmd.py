import discord
from discord.utils import get
import helpers

CONST_EMPTY_CHAR = chr(173)

async def attendance(message, guild, id_to_role):

    # parse input
    args = message.content.split(" ")
    number_of_args = len(args)
    list_of_role_ids = list(id_to_role.keys()) + ["@everyone"]

    # checking if input is invalid
    if not number_of_args <= 2 or (number_of_args == 2 and not any(str(role) in args[1] for role in list_of_role_ids)):
        embed=discord.Embed(title="INVALID COMMAND: *$attendance*", description = "Please follow the syntax below:\n" + CONST_EMPTY_CHAR, color=discord.Color.red())
        embed.add_field(name="Server-wide attendance", value = '*$attendance*', inline=False) 
        embed.add_field(name="Role-specific attendance", value = '*$attendance* @rolehere', inline=False) 
        await message.channel.send(embed=embed)
    # valid input
    else:
        present = []
        absent = []
        unregistered = []

        # present, absent attendance for role @everyone
        if number_of_args == 1 or args[1] == "@everyone":
            filtered_members = [member for member in guild.members if member.bot==False]
            [present.append(f'<@{mem.id}>') if mem.voice else absent.append(f'<@{mem.id}>') for mem in filtered_members]
            attendance_section = "@everyone"
            role_name = "@everyone"
        else:
            # attendance for roles that are not @everyone
            role_id = helpers.get_integers_of_string(args[1])
            role_name = id_to_role.get(role_id)
            attendance_section = args[1]

            # if we want expert session attendance
            if role_name == "expert session":
                (present, absent, unregistered) = get_expected_session_experts(guild)

            # take attendance for any role that is not @everyone or @Expert Session
            else:
                filtered_members = [member for member in get(guild.roles, id=role_id).members]
                [present.append(f'<@{mem.id}>') if mem.voice else absent.append(f'<@{mem.id}>') for mem in filtered_members]

        #send attendance message to Discord
        embed=discord.Embed(title="ATTENDANCE", color=discord.Color.blue())
        embed.add_field(name=f'Total users with role ({len(present) + len(absent) + len(unregistered)})', value = attendance_section, inline=False) 
        embed.add_field(name=f'Absent from voice channel ({len(absent)})', value = "\n".join(absent) if absent else "N/A", inline=False)
        embed.add_field(name=f'Present in voice channel ({len(present)})', value = "\n".join(present) if present else "N/A", inline=False)
        if role_name == "expert session": embed.add_field(name=f'Unregistered on Discord ({len(unregistered)})', value = "\n".join(unregistered) if unregistered else "N/A", inline=False)
        await message.channel.send(embed=embed)
    
    return

# function to show present, absent, unregistered attendance for expected session experts
def get_expected_session_experts(guild):

    # get expert channels with roles in them -> these roles are who we expect to be at the expert session
    expert_channels = {category.name: category.channels for category in guild.categories if helpers.is_expert_cohort_name(category.name)}
    expert_channels_with_roles = [(category, channel) for (category, channels) in expert_channels.items() for channel in channels if channel.overwrites]

    #get expected expert role id & their name + cohort
    expected_experts = []
    for category, channel in expert_channels_with_roles:
        channel_expert_role_info = [(role_info.id, f'{helpers.case_insensitive_replace("room", "", role_info.name)} -> {category}') for role_info, _ in channel.overwrites.items() if "room" in role_info.name.lower()]
        expected_experts += channel_expert_role_info
    
    present = []
    absent = []
    unregistered = []
    
    # determine expert attendance based on voice presence/registration on server
    for role_id, role_name_and_cohort in expected_experts:
        role = get(guild.roles, id = role_id)
        if role.members:
            member = role.members[0]
            present.append(f'<@{member.id}>') if member.voice else absent.append(f'<@{member.id}>')
        else:
            unregistered.append(role_name_and_cohort)

    return (present, absent, unregistered)
