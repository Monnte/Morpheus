import disnake
import re
from utility import split
from config.messages import Messages


class BookmarkFeatures():
    def __init__(self, bot):
        self.bot = bot

    async def create_image_embed(self, inter, image, title_name=None):
        """Create embed from image only"""
        if not title_name:
            title_name = Messages.bookmark_title.format(inter.guild.name)

        author = inter.message.author
        embed = disnake.Embed(title=title_name, color=author.colour)
        embed.set_author(name=author, icon_url=author.display_avatar.url)
        embed.set_image(image)
        embed.add_field(
            name="Channel",
            value=f"{inter.message.channel.mention}"
        )
        return embed

    async def create_bookmark_embed(self, inter, title_name=None):
        if not title_name:
            title_name = Messages.bookmark_title.format(inter.guild.name)

        author = inter.message.author
        embed = disnake.Embed(title=title_name, colour=author.colour)
        embed.set_author(name=author, icon_url=author.display_avatar.url)

        content = ""
        if inter.message.embeds:
            for embed in inter.message.embeds:
                embed.title, embed.colour = title_name, author.colour
                embed.set_author(name=author, icon_url=author.display_avatar.url)

        if inter.message.content:
            content = inter.message.content
        else:
            content += "*Empty*"

        # create list of attachments
        upload_limit = False
        images = []
        files_attached = []
        if inter.message.attachments:
            for attachment in inter.message.attachments:
                if attachment.size > 8388608:
                    upload_limit = True
                    continue
                if re.search(r"\.png|\.jpg|\.jpeg|\.gif$", str(attachment)):
                    images.append(attachment)
                else:
                    files_attached.append(await attachment.to_file())

        if images:
            embed.set_image(images[0])
            del images[0]

        if len(content) > 1024:
            parts = split(content, 1024)
            for msg in parts:
                embed.add_field(name="Původní zpráva", value=msg, inline=False)
        else:
            embed.add_field(name="Původní zpráva", value=content, inline=False)

        if upload_limit:
            embed.add_field(name="Poznámka", value=Messages.bookmark_upload_limit, inline=False)

        embed.add_field(
            name="Channel",
            value=f"{inter.message.channel.mention}"
        )
        return ([embed], images, files_attached)
