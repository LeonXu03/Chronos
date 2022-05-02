import discord

async def zoom_image(message):
    embed=discord.Embed(title="ZOOM BACKGROUND", description = 'To download the Zoom background at the bottom:\n\n1. Click on the image\n2. Click "Open original" on the bottom left of the pop-up\n3. Click "trust this domain"\n4. Right-click on the image in the browser pop-up and download', color=discord.Color.dark_blue())
    embed.set_image(url='https://www.eweek.com/wp-content/uploads/2021/01/Zoom.logo_.jpg')
    await message.channel.send(embed=embed)