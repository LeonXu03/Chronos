import discord
import pprint
import csv as CSV

# Relevant Discord.py documentation
# Channel object docs: https://discordpy.readthedocs.io/en/stable/api.html#guildchannel
# Message object docs: https://discordpy.readthedocs.io/en/stable/api.html#message

guild_id = 961281351204618352
client = discord.Client()

# change as necessary
num_of_cols_before_overall_stats = 6
# set message_limit = None for no message limit
message_limit = 100

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    await analysis()

async def analysis():

    guild = client.get_guild(guild_id)

    for channel in guild.channels: 

        if channel.type == discord.ChannelType.text and str(channel.category) == "Text Channels":
            #sheet headers
            csv = [['DATE OF MESSAGE', 'USER', 'MESSAGE', 'LINK FOUND']]

            messages = await channel.history(limit=message_limit).flatten()

            number_of_commands = 0
            number_of_websites = 0

            for message in [msg for msg in messages if msg.author.bot == False]:
                msg_datetime = message.created_at.strftime("%m/%d/%Y, %H:%M:%S") + " UTC"
                msg_author = message.author.name
                # if you don't replace the '\n' char there will be an error in AppScript with reading the csv file
                msg_content = message.content.replace('\n', ' ')

                if any(substring in msg_content for substring in ["$confirm","$attendance","$schedule","$reminders","$delete","$merge","$set_zoom","$zoom","$background","$program","$help","$command"]):
                    number_of_commands+=1
                    
                if "https" in msg_content:
                    number_of_websites+=1
                    link = next(text for text in msg_content.split(" ") if text.startswith("https"))
                    csv.append([msg_datetime, msg_author, msg_content, link])
                else:
                    csv.append([msg_datetime, msg_author, msg_content])

            overall_stats = []                
            overall_stats.append(["Commands Used: ", str(number_of_commands)])
            overall_stats.append(["Websites Linked: ", str(number_of_websites)])

            while len(csv)<len(overall_stats):
                csv.append([])
            
            for index in range(len(overall_stats)):
                
                empty_cols = [chr(173) for i in range(num_of_cols_before_overall_stats-len(csv[index]))]

                csv[index] = csv[index] + empty_cols + overall_stats[index] 
            
            with open(f'#{channel.name}.csv', 'w', encoding='UTF8', newline='') as f:
                writer = CSV.writer(f)

                for row in csv:
                    print(f'Print to #{channel.name}.csv: ', row)
                    writer.writerow(row)

            #pprint.pprint(csv)

    print("Analysis complete")
    return


if __name__ == "__main__":
    #load_dotenv()
    client.run('OTYxMjgzNDQzMzg2MzcyMTU5.Yk2u-A.yfYOErqIYqrwATM33UmnTAGrfts')
    #client.run(os.environ.get('TOKEN'))