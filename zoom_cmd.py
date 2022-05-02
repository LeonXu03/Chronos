# show current zoom link
async def zoom_link(message, zoom_link):
    await message.channel.send(zoom_link)

#set new zoom link
async def set_zoom_link(message):
    args = message.content.split(" ")
    num_of_args = len(args)

    #check if command input is valid
    if num_of_args != 2:
        await message.channel.send("INVALID COMMAND: follow the format **$set_zoom** ***link***")
        return "No Zoom link set"

    await message.channel.send("New Zoom link set: " + args[1])
    return args[1]