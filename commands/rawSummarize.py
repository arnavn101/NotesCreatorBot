from commands.base_command import BaseCommand
from discord import Embed
import bs4
import requests

class RawSummarize(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Summarize Contents of a Website"

        self.data = {
            'formIdentify': 'notes',
            'bullet_points': '',
            'choice': 'Website',
            'URL': ''
        }

        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["bullet_points", "website_name"]

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

        try:
            self.data['bullet_points'] = str(int(params[0]))
            self.data['URL'] = str(params[1])
            list_summary = self.send_request()
        except Exception:
            await message.channel.send(
                "Please enter a valid number of bullet points and a valid url")
            return

        summaries = []
        for element in list_summary:
            element = element.replace('\n', '')
            if element and 'Return to Home Page' not in element:
                summaries.append(element)

        embed_message = ""

        for individual_summary in summaries:
            embed_message += individual_summary + "\n"
        try:
            await message.channel.send(embed_message)
            return
        except Exception:
            await message.channel.send(message.author.mention + " The Bullet Points Parameter is too large!!!")
            return
