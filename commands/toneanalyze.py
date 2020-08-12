from commands.base_command import BaseCommand
from discord import Embed, Message
import bs4
import requests
import time

class ToneAnalyze(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Analyze Tone within text"

        self.data = {
            'formIdentify': 'tone_analyze',
            'text_toning': ''
        }

        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["text"]

        super().__init__(description, params)

    def send_request(self):
        response = requests.post('https://smartnotes101.herokuapp.com/', data=self.data,
                                 headers={'Cache-Control': 'no-cache'})
        soup = bs4.BeautifulSoup(response.text, features="lxml")
        return soup.findAll('h1', {'class': 'value'})[0].find_all_next(text=True)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object
        message_author = str(message.author)

        # Get member object
        activeServers = list(client.guilds)[0]
        member_object = activeServers.get_member_named(message_author)

        try:
            self.data['text_toning'] = (" ".join(params)).replace('"', '').replace("'", "")
            list_tone = self.send_request()
        except Exception:
            await message.channel.send(
                "Please enter valid text")
            return

        tones = []
        for element in list_tone:
            element = element.replace('\n', '')
            if element and 'Return to Home Page' not in element:
                tones.append(element)

        embed_message = Embed(title=f'Summary of The Text', color=0xff0000)
        embed_message.set_footer(text=message_author, icon_url=member_object.avatar_url)

        for individual_tone in tones:
            embed_message.add_field(name="\u200b", value=individual_tone, inline=False)
        try:
            await message.channel.send(embed=embed_message)
        except Exception:
            await message.channel.send(message.author.mention + " The Text is too large!!!")
