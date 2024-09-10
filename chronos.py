import discord
import os
from dotenv import load_dotenv
from discord.ext import tasks

#import other files
import helpers
import attendance_cmd
import program_cmd
import background_cmd
import help_cmd
import zoom_cmd
import schedule_cmd
import delete_cmd
import reminders_cmd
import merge_cmd

#discord bot setup - do not change
intents = discord.Intents().all()
client = discord.Client(intents=intents)
guild = None

# nice formatting variables - do not change
format_without_seconds = '%Y-%m-%d %H:%M'

# server roles/channels database - do not change
role_to_id = {}
id_to_role = {}
channel_to_id = {}
id_to_channel = {}
team_ids_to_channels = {}

# scheduling reminders variables - do not change
scheduled_messages_list = []
expired_messages_indexes = []
ID = 1

# scheduling merge variables - do not change
scheduled_merge_info = {}

# CHANGE THESE VARIABLES AS REQUIRED
guild_id = 1282897115919421480
prefix = "$"
zoom_link = "No Zoom link set"

# function runs when bot starts up
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    guild = client.get_guild(guild_id)
    update_server_ids(guild)
                
    clean_scheduled_messages()
    await send_message.start()

# function runs when discord detects a message
@client.event
async def on_message(message):
    global guild
    global scheduled_messages_list
    global scheduled_merge_info
    global ID
    global scheduled_merge_info
    global zoom_link

    if message.author == client.user:
        return 

    # update database every time we have a message
    guild = client.get_guild(guild_id)
    update_server_ids(guild)

    # list of admin role names
    admin_roles_names = ["tech support", "htctw team", "how to change the world team"]
    admin = any(role.name.lower() in admin_roles_names for role in message.author.roles)
    print("Admin: " + str(admin))

    #try:

    # check if we should merge the scheduled merge
    if message.content.startswith(prefix) and scheduled_merge_info and admin:
        if message.content.startswith(prefix + 'confirm'):
            await merge_cmd.confirm(message, scheduled_merge_info, guild)
        else:
            await merge_cmd.confirm(message, {}, guild)
        scheduled_merge_info = {}
        
    if message.content.startswith(prefix + "attendance") and admin:
        await attendance_cmd.attendance(message, guild, id_to_role)

    elif message.content.startswith(prefix + "schedule") and admin:
        (ID, scheduled_messages_list) = await schedule_cmd.schedule(message, scheduled_messages_list, ID, id_to_channel)
        
    elif message.content.startswith(prefix + 'reminders') and admin:
        await reminders_cmd.reminders(message, scheduled_messages_list)
    
    elif message.content.startswith(prefix + 'delete') and admin:
        scheduled_messages_list = await delete_cmd.delete(message, scheduled_messages_list)

    elif message.content.startswith(prefix + 'merge') and admin:
        scheduled_merge_info = await merge_cmd.merge(message, id_to_channel, role_to_id, guild)

    elif message.content.startswith(prefix + 'set_zoom') and admin:
        zoom_link = await zoom_cmd.set_zoom_link(message)

    elif message.content.startswith(prefix + 'zoom'):
        await zoom_cmd.zoom_link(message, zoom_link)

    elif message.content.startswith(prefix + 'background'):
        await background_cmd.zoom_image(message)
    
    elif message.content.startswith(prefix + 'program'):
        await program_cmd.daily_schedule(message)
    
    elif message.content.startswith(prefix + 'help') or message.content.startswith(prefix + 'command'):
        await help_cmd.help(message, admin)

    elif (message.content.startswith(prefix) and "cancel" not in message.content and "confirm" not in message.content and admin) or (message.content.startswith(prefix) and admin==False):
        await message.channel.send("Sorry that command doesn't exist. If you need help, type $help")
    
    return

    #except:
        #embed=discord.Embed(title="UNEXPECTED ERROR", description = 'Sorry, something went wrong. Please try again. If the error persists, contact Tech Support.', color=discord.Color.red())
        #await message.channel.send(embed=embed)
        #return

# update databse with most recent role/channel information
def update_server_ids(guild):
    global role_to_id
    global id_to_role
    global channel_to_id
    global id_to_channel
    global team_ids_to_channels

    for role in guild.roles:
        role_to_id.update({role.name.lower(): role.id})
        id_to_role.update({role.id: role.name.lower()})
    
    for text_channel in guild.text_channels:
        channel_to_id.update({text_channel.name.lower(): text_channel.id})
        id_to_channel.update({text_channel.id: text_channel.name.lower()})
        if helpers.is_valid_team_channel(text_channel.name.lower()): 
            team_ids_to_channels.update({text_channel.id: text_channel.name.lower()})

# clean reminders that have expired
def clean_scheduled_messages():
    global scheduled_messages_list 
    global expired_messages_indexes

    # get all reminders with expired datetime
    for index in range(len(scheduled_messages_list)):
        if scheduled_messages_list[index].get('datetime') < helpers.get_current_datetime_string_est(format_without_seconds):
            expired_messages_indexes.append(index)

    # remove expired reminders
    for index in expired_messages_indexes:
        print("message expired @ " + scheduled_messages_list[index].get('datetime') + ": " + str(scheduled_messages_list[index].get('id')))
        scheduled_messages_list.pop(index)

    #reset
    expired_messages_indexes = []

# check if we should send reminder based on its datetime
@tasks.loop(seconds=10)
async def send_message():
    global scheduled_messages_list
    global expired_messages_indexes
    current_datetime = helpers.get_current_datetime_string_est(format_without_seconds)

    print("send_message()")
    
    # for every reminder that is scheduled
    for index in range(len(scheduled_messages_list)):
        #if it's supposed to be sent now
        if scheduled_messages_list[index].get('datetime') == current_datetime:
            msg_info = scheduled_messages_list[index]
            msg_channel_id = msg_info.get('channel')
            msg = msg_info.get('message')
            # if message is to be sent to all team chats
            if id_to_channel.get(msg_channel_id) == "team-x-y":
                # if message is to ping each team chat
                if str(role_to_id.get('team x y')) in msg:
                    for (channel_id, channel_name) in team_ids_to_channels.items():
                        team_xy_role_id = role_to_id.get('team x y')
                        channel_name_to_role_id = role_to_id.get(channel_name.replace("-", " "))
                        new_message = msg.replace('<@&{}>'.format(team_xy_role_id), '<@&{}>'.format(channel_name_to_role_id))
                        await client.get_channel(channel_id).send(new_message)
                # if message to each team chat but not pinging them
                else:
                    for (channel_id, _) in team_ids_to_channels.items():
                        await client.get_channel(channel_id).send(msg)
            # if message not sent to all team chats
            else:
                await client.get_channel(msg_channel_id).send(msg)
            # this message is expired since it's been sent already
            expired_messages_indexes.append(index)

    # clean expired messages
    clean_scheduled_messages()

    return

# start the Discord bot
if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('TOKEN')
    if token is None:
        raise ValueError("No Discord bot TOKEN supplied in the .env file")
    client.run(token)