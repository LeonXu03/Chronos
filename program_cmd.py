import helpers
import discord

CONST_FORMAT_DATE = '%Y-%m-%d'
some_backup_image_link = 'https://i.imgur.com/3UWbcYG.jpeg'

async def daily_schedule(message):
    # current date
    date = helpers.get_current_datetime_string_est(CONST_FORMAT_DATE)
    # should be filled with daily program schedule images. {'YYYY-MM-DD': 'image link'}. Image link can be attained by "Open image in new tab"
    daily_program_image_links = {
        '2022-04-18': 'https://i.imgur.com/NBoJJas.jpg', 
        '2022-04-25': 'https://i.imgur.com/3UWbcYG.jpeg'
        }
    embed=discord.Embed(title="TODAY'S SCHEDULE", description = date, color=discord.Color.dark_green())
    embed.set_image(url= daily_program_image_links.get(date, some_backup_image_link))
    await message.channel.send(embed=embed)