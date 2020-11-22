import discord #type: ignore
from typing import Union

from bot.helpers import cleanup_file, construct_download_link, construct_upload_link
from bot.types import DMChannel, Message, TextChannel
from bot.models import DBManager, File, User


class Bot(discord.Client):
    def __init__(self, identifier: str, *args, **kwargs) -> None:
        """Creates a new Bot instance.
                :identifier: Character/string pre-fix you want to use to identify targetted bot-commands (EG: '!' or '$').

            Instance variables:
                self.identifier: The character/string pre-fix you want to use to identify targetted bot-commands.
                self.db: A bot.models.DBManager instance so we can easily access SQLAlchemy's session.
        """

        super().__init__(*args, **kwargs)

        self.identifier = identifier
        self.db = DBManager()

    async def on_ready(self) -> None:
        """Discord.py API override for on_ready.  Just a sanity check to make sure my script started properly."""
        print("logged on as {0}".format(self.user))

    async def on_message(self, message: Message) -> None:
        """Discord.py API override for on_message.  This route handles parsing/checking the message/message-channel to figure out what commands to do.
            An "interaction" is just the name that I've given the UI-flow for uploading/downloading a file.
            If the channel is a text-channel, then it looks for the command "!ftp" which either creates a new interaction, or displays the current interactions information to the user.
            If the channel is a DM channel, then it looks for the command "!r" or "!reset", which deletes the current interaction, the old file on disk, and then starts a new interaction.

                :message: The original message on-event from the Discord.py API.
        """

        file: Union[File, None] = None
        if isinstance(message.channel, TextChannel):
            if message.content and message.content[0] == self.identifier and message.content[1:] == 'ftp':
                file = self.db.session.query(File).filter(File.user_id == message.author.id).first()
                dm_chan: DMChannel = await message.author.create_dm()

                if file and file.completed:
                    await dm_chan.send("You already have a file that has been uploaded.  You may only have one file uploaded at a time. If you wish to delete your existing FTP'd file so you can upload another one, please respond with '!reset' or '!r' for short.  Your old file with the ID of {} can be found here: {} ".format(file.id, construct_download_link(file.id)))
                elif file:
                    await dm_chan.send("You have a file slot waiting to be used.  Please upload your file here: {}".format(construct_upload_link(file.id)))
                else:
                    await self.start_new_interaction(message, dm_chan)
        elif isinstance(message.channel, DMChannel):
            if message.content and message.content[0] == self.identifier and (message.content[1:] == 'r' or message.content[1:] == 'reset'):
                file = self.db.session.query(File).filter(File.user_id == message.author.id).first()

                if not file:
                    await self.start_new_interaction(message, message.channel)
                else:
                    # This will get committed when start_new_interaction commits.
                    self.db.session.delete(file)
                    cleanup_file(file.id, file.ext)
                    await self.start_new_interaction(message, message.channel)

    async def start_new_interaction(self, message: Message, dm_chan: DMChannel) -> None:
        """Helper method to start a new interaction.  It either gets/creates the User instance, and then creates a new File (interaction) in the DB associated with the User.
            :message: The original message object that started this interaction (contains the discord User's ID along with some other stuff).
            :dm_chan: The Direct-Message channel so we can send messages back to the user.
        """

        user: Union[User, None] = self.db.session.query(User).get(message.author.id)
        if user is None:
            user = User(id=message.author.id,
                        name=message.author.name,
                        discrim=message.author.discriminator
                        )
            self.db.session.add(user)

        new_file: File = File(user_id=user.id)
        self.db.session.add(new_file)
        self.db.session.commit()

        await dm_chan.send('New file-transfer created. Please upload your file here: {}'.format(construct_upload_link(new_file.id)))

