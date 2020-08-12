from collections import deque
from commands.base_command import BaseCommand


class rawDisplayLogs(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Display Debug Logs in Raw Format"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["number_lines"]

        super().__init__(description, params)

    def returnLogLines(self, file_name, lines=1):
        with open(file_name) as fileObject:
            return list(deque(fileObject, lines))

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object
        try:
            number_lines = int(params[0])
        except Exception:
            await message.channel.send(
                "Please, provide valid number of lines")
            return

        list_lines = self.returnLogLines("discord.log", number_lines)
        embed_msg = "Log Information\n"

        for i in range(number_lines):
            embed_msg += f"Line {i + 1} : {list_lines[i]}\n"

        await message.channel.send(embed_msg)
        return
