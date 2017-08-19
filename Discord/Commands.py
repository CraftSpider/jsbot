"""
    Commands cog for Talos
    Holds all commands usable by any user, and a couple of classes relevant to those commands.

    Author: CraftSpider
"""
import discord
from discord.ext import commands
import asyncio
import random
import datetime
from collections import defaultdict

active_pw = defaultdict(lambda: None)

perms = {}


def sort_mem(member):
    """Function key for sorting PW_Member objects."""
    return member.end - member.start

def strfdelta(tdelta, fmt):
    d = {"d": tdelta.days}
    d["h"], rem = divmod(tdelta.seconds, 3600)
    d["m"], d["s"] = divmod(rem, 60)
    return fmt.format(**d)


class Commands:
    """These commands can be used by anyone, as long as Talos is awake.\nThey don't care who is using them."""

    __slots__ = ['bot']

    def __init__(self, bot):
        """Initialize the Commands cog. Takes in an instance of bot to use while running."""
        self.bot = bot

    #
    #   Generator Strings
    #
    noun = ["dog", "cat", "robot", "astronaut", "man", "woman", "person", "child", "giant", "elephant", "zebra",
            "animal", "box", "tree", "wizard", "mage", "swordsman", "soldier", "inventor", "doctor", "Talos", "East"
            "dinosaur", "insect", "nerd", "dancer", "singer", "actor", "barista", "acrobat", "gamer", "writer",
            "dragon"]
    adjective = ["happy", "sad", "athletic", "giant", "tiny", "smart", "silly", "unintelligent", "funny",
                 "coffee-loving", "lazy", "spray-tanned", "angry", "disheveled", "annoying", "loud", "quiet", "shy",
                 "extroverted", "jumpy", "ditzy", "strong", "weak", "smiley", "annoyed", "dextrous"]
    goal = ["fly around the world", "go on a date", "win a race", "tell their crush how they feel",
            "find their soulmate", "write a chatbot", "get into university", "graduate high school",
            "plant a hundred trees", "find their biological parents", "fill their bucket list", "find atlantis",
            "learn magic", "learn to paint", "drive a car", "pilot a spaceship", "leave Earth", "go home",
            "redo elementary school", "not spill their beer"]
    obstacle = ["learning to read", "fighting aliens", "saving the world", "doing algebra", "losing their hearing",
                "losing their sense of sight", "learning the language", "hacking the mainframe", "coming of age",
                "the nuclear apocalypse is happening", "incredibly drunk", "drinking coffee", "surfing",
                "spying on the bad guys", "smelling terrible", "having a bad hair day", "exploring the new planet",
                "on the moon", "on Mars"]
    
    place = ["pub", "spaceship", "museum", "office", "jungle", "forest", "coffee shop", "store", "market", "station",
             "tree", "hut", "house", "bed", "bus", "car", "dormitory", "school", "desert", "ballroom", "cattery",
             "shelter", "street"]
    place_adjective = ["quiet", "loud", "crowded", "deserted", "bookish", "colorful", "balloon-filled", "book", "tree",
                       "money", "video game", "cat", "dog", "busy", "apocalypse", "writer", "magic", "light", "dark",
                       "robotic", "futuristic", "old-timey"]
    action = ["learn to read", "jump up and down", "cry a lot", "cry a little", "smile", "spin in a circle",
              "get arrested", "dance to the music", "listen to your favourite song", "eat all the food",
              "win the lottery", "hack the mainframe", "save the world", "find atlantis", "get accepted to Hogwarts",
              "swim around", "defy gravity", "spy on the bad guys", "drive a car", "enter the rocket ship",
              "learn math", "write a lot", "do gymnastics"]

    #
    #   User Commands
    #
    
    @commands.command()
    async def information(self, ctx):
        """Gives a short blurb about Talos."""
        await ctx.send("Hello! I'm Talos, official PtP mod-bot.\
                           \nMy Developers are CraftSpider, Dino, and HiddenStorys.\
                           \nAny suggestions or bugs can be sent to my email, talos.ptp@gmail.com.")

    @commands.command()
    async def discord_tos(self, ctx):
        """Disclaimer for discord TOS"""
        await ctx.send("Talos will in the process of running possibly log your username and log commands that you give "
                       "it. Due to Discord TOS, you must be informed and consent to any storage of data you send here. "
                       "This data will never be publicly shared except at your request, and only used to help run Talos"
                       " and support features that require it. If you have any questions about this or problems with it"
                       " , please talk to one of the Talos developers for information and we'll see what we can do to "
                       "help")

    @commands.command()
    async def version(self, ctx):
        """Returns Talos version."""
        await ctx.send("Version: {0}".format(self.bot.VERSION))

    @commands.command()
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.lower().split('d'))
        except ValueError:
            await ctx.send('Format has to be in NdN!')
            return
        try:
            result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        except ValueError:
            await ctx.send("Minimum second value is 1")
            return
        if result is "":
            await ctx.send("Minimum first value is 1")
            return
        await ctx.send(result)
        
    @commands.command(description='For when you wanna settle the score some other way',
                      usage="[choice 1], [choice 2], ...")
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        choices = " ".join(choices)
        if "," not in choices:
            await ctx.send("I need at least two choices to choose between!")
            return
        out = "I'm choosing between: {}.\n".format(choices)
        if random.randint(1, 500) == 1:
            out += "None of the above"
        elif random.randint(1, 500) == 500:
            out += "All of the above"
        else:
            choices = choices.split(",")
            out += random.choice(choices).strip()
        await ctx.send(out)

    @commands.command()
    async def time(self, ctx):
        """Prints out the current time in UTC, HH:MM:SS format"""
        await ctx.send("It's time to get a watch. {0}".format(datetime.datetime.utcnow().strftime("%H:%M:%S")))
    
    @commands.command(aliases=["ww", "WW"])
    async def wordwar(self, ctx, length: str="", start: str=""):
        """Runs an X minute long word-war"""
        try:
            length = float(length)
        except Exception:
            await ctx.send("Please specify the length of your word war (in minutes).")
            return
        if length > 60 or length < 1:
            await ctx.send("Please choose a length between 1 and 60 minutes.")
            return

        if start:
            try:
                if start[0] == ":":
                    start = int(start[1:])
                elif start[0].isnumeric():
                    start = int(start)
                else:
                    raise Exception
            except Exception:
                await ctx.send("Start time format broken. Starting now.")
                start = ""
            if start != "" and (start > 59 or start < 0):
                await ctx.send("Please specify a start time in the range of 0 to 59.")
                return

        if start is not "":
            dif = abs(datetime.datetime.utcnow() - datetime.datetime.utcnow().replace(minute=start, second=0))
            await ctx.send("Starting WW at :{0:02}".format(start))
            await asyncio.sleep(dif.total_seconds())
        minutes = "minutes" if length != 1 else "minute"
        await ctx.send("Word War for {0:g} {1}.".format(length, minutes))
        await asyncio.sleep(length * 60)
        await ctx.send("Word War Over")

    @commands.command()
    async def credits(self, ctx):
        """Giving credit where it is due"""
        await ctx.send("Primary Developers: CraftSpider, Dino.\n"
                       "Other contributors: Wundrweapon, HiddenStorys\n"
                       "Artist: Misty Tynan")
    
    @commands.command()
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        await ctx.send('{0.name} joined in {0.joined_at}'.format(member))
    
    @commands.command()
    async def uptime(self, ctx):
        """To figure out how long the bot has been online."""
        boot_string = self.bot.BOOT_TIME.strftime("%b %d, %H:%M:%S")
        tdelta = datetime.datetime.now() - self.bot.BOOT_TIME
        delta_string = strfdelta(tdelta, "{d} days, {h:02}:{m:02}:{s:02}")
        out = "I've been online since {0}, a total of {1}".format(boot_string, delta_string)
        await ctx.send(out)

    @commands.command()
    async def favor(self, ctx):
        await ctx.send("!East could I ask you for a favor? I need someone to verify my code.")
        await asyncio.sleep(2)
        async with ctx.typing():
            await asyncio.sleep(1)
            await ctx.send("Oh my. Well, if you insist ;)")

    @commands.command()
    async def my_perms(self, ctx):
        """Has Talos print out your current permissions"""
        perms = ctx.author.guild_permissions
        out = "```Permissions:\n"
        out += "    Administrator: {}\n".format(perms.administrator)
        out += "    Add Reactions: {}\n".format(perms.add_reactions)
        out += "    Attach Files: {}\n".format(perms.attach_files)
        out += "    Ban Members: {}\n".format(perms.ban_members)
        out += "    Change Nickname: {}\n".format(perms.change_nickname)
        out += "    Connect: {}\n".format(perms.connect)
        out += "    Deafen Members: {}\n".format(perms.deafen_members)
        out += "    Embed Links: {}\n".format(perms.embed_links)
        out += "    External Emojis: {}\n".format(perms.external_emojis)
        out += "    Instant Invite: {}\n".format(perms.create_instant_invite)
        out += "    Kick Members: {}\n".format(perms.kick_members)
        out += "    Manage Channels: {}\n".format(perms.manage_channels)
        out += "    Manage Emojis: {}\n".format(perms.manage_emojis)
        out += "    Manage Guild: {}\n".format(perms.manage_guild)
        out += "    Manage Messages: {}\n".format(perms.manage_messages)
        out += "    Manage Nicknames: {}\n".format(perms.manage_nicknames)
        out += "    Manage Roles: {}\n".format(perms.manage_roles)
        out += "    Manage Webhooks: {}\n".format(perms.manage_webhooks)
        out += "    Mention Everyone: {}\n".format(perms.mention_everyone)
        out += "    Move Members: {}\n".format(perms.move_members)
        out += "    Mute Members: {}\n".format(perms.mute_members)
        out += "    Read Message History: {}\n".format(perms.read_message_history)
        out += "    Read Messages: {}\n".format(perms.read_messages)
        out += "    Send Messages: {}\n".format(perms.send_messages)
        out += "    Send TTS: {}\n".format(perms.send_tts_messages)
        out += "    Speak: {}\n".format(perms.speak)
        out += "    Use Voice Activation: {}\n".format(perms.use_voice_activation)
        out += "    View Audit: {}\n".format(perms.view_audit_log)
        out += "```"
        await ctx.send(out)

    @commands.command(name="Hi", hidden=True)
    async def hi(self, ctx, *extra):
        if str(ctx.author) == "East#4048" and extra[0] == "there...":
            async with ctx.typing():
                await asyncio.sleep(1)
                await ctx.send("Hello East.")
            await asyncio.sleep(1)
            async with ctx.typing():
                await asyncio.sleep(2)
                await ctx.send("Thank you. The same to you.")
            return
        await ctx.send("Hello there {}".format(ctx.author.name))
    
    @commands.group()
    async def generate(self, ctx):
        """Generates a crawl or prompt"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Valid options are 'prompt' and 'crawl'.")
    
    @generate.command(name='crawl')
    async def _crawl(self, ctx):
        """Generates a crawl"""
        place_adj = random.choice(self.place_adjective)
        place = random.choice(self.place)
        words = str(random.randint(50, 500))
        action = random.choice(self.action)
        await ctx.send("You enter the {} {}. Write {} words as you {}.".format(place_adj, place, words, action))
    
    @generate.command(name='prompt')
    async def _prompt(self, ctx):
        """Generates a prompt"""
        adj = random.choice(self.adjective)
        noun = random.choice(self.noun)
        goal = random.choice(self.goal)
        obstacle = random.choice(self.obstacle)
        await ctx.send("A story about a {} {} who must {} while {}.".format(adj, noun, goal, obstacle))

    @commands.group(aliases=["pw", "PW"])
    async def productivitywar(self, ctx):
        """Commands for a productivity war."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Valid options are 'create', 'join', 'start', 'leave', and 'end'.")

    @productivitywar.command(name='create')
    async def _create(self, ctx):
        """Begins a new PW, if one isn't already running."""
        if active_pw[ctx.guild.id] is not None:
            await ctx.send("There's already a PW going on. Would you like to **join**?")
        else:
            await ctx.send("Creating a new PW.")
            active_pw[ctx.guild.id] = PW()
            active_pw[ctx.guild.id].join(ctx.author)

    @productivitywar.command(name='join')
    async def _join(self, ctx):
        """Join a currently running PW, if you aren't already in it."""
        if active_pw[ctx.guild.id] is not None:
            if active_pw[ctx.guild.id].join(ctx.author):
                await ctx.send("User {} joined the PW.".format(ctx.author))
            else:
                await ctx.send("You're already in this PW.")
        else:
            await ctx.send("No PW to join. Maybe you want to **create** one?")

    @productivitywar.command(name='start')
    async def _start(self, ctx):
        """Start a PW that isn't yet begun."""
        if active_pw[ctx.guild.id] is not None:
            if not active_pw[ctx.guild.id].get_started():
                await ctx.send("Starting PW")
                active_pw[ctx.guild.id].begin()
            else:
                await ctx.send("PW has already started! Would you like to **join**?")
        else:
            await ctx.send("No PW to start. Maybe you want to **create** one?")

    @productivitywar.command(name='leave')
    async def _leave(self, ctx):
        """End your involvement in a PW, if you're the last person, the whole thing ends."""
        if active_pw[ctx.guild.id] is not None:
            leave = active_pw[ctx.guild.id].leave(ctx.author)
            if leave == 0:
                await ctx.send("User {} left the PW.".format(ctx.author))
            elif leave == 1:
                await ctx.send("You aren't in the PW! Would you like to **join**?")
            elif leave == 2:
                await ctx.send("You've already left this PW! Are you going to **end** it?")
            if active_pw[ctx.guild.id].get_finished():
                await self._end.invoke(ctx)
        else:
            await ctx.send("No PW to leave. Maybe you want to **create** one?")

    @productivitywar.command(name='end')
    async def _end(self, ctx):
        """End the whole PW, if one is currently running."""
        if active_pw[ctx.guild.id] is None:
            await ctx.send("There's currently no PW going on. Would you like to **create** one?")
        elif not active_pw[ctx.guild.id].get_started():
            await ctx.send("Deleting un-started PW.")
            active_pw[ctx.guild.id] = None
        else:
            await ctx.send("Ending PW.")
            active_pw[ctx.guild.id].finish()
            cur_pw = active_pw[ctx.guild.id]
            out = "```"
            out += "Start: {}\n".format(cur_pw.start.replace(microsecond=0).strftime("%b %d - %H:%M:%S"))
            out += "End: {}\n".format(cur_pw.end.replace(microsecond=0).strftime("%b %d - %H:%M:%S"))
            out += "Total: {}\n".format(cur_pw.end.replace(microsecond=0) - cur_pw.start.replace(microsecond=0))
            out += "Times:\n"
            cur_pw.members.sort(key=sort_mem, reverse=True)
            for member in cur_pw.members:
                out += "    {0} - {1}\n".format(member.user, member.end.replace(microsecond=0) - member.start.replace(microsecond=0))
            out += "```"
            await ctx.send(out)
            active_pw[ctx.guild.id] = None

    @productivitywar.command(name='dump', hidden=True)
    async def _dump(self, ctx):
        """Dumps info about the current state of a running PW"""
        cur_pw = active_pw[ctx.guild.id]
        if cur_pw is None:
            await ctx.send("No PW currently running")
            return
        out = "```"
        out += "Start: {}\n".format(cur_pw.start)
        out += "End: {}\n".format(cur_pw.end)
        out += "Members:\n"
        for member in cur_pw.members:
            out += "    {0} - {1} - {2}\n".format(member, member.start, member.end)
        out += "```"
        await ctx.send(out)


class PW:

    __slots__ = ['start', 'end', 'members']

    def __init__(self):
        """Creates a PW object, with empty variables."""
        self.start = None
        self.end = None
        self.members = []

    def get_started(self):
        """Gets whether the PW is started"""
        return self.start is not None

    def get_finished(self):
        """Gets whether the PW is ended"""
        return self.end is not None

    def begin(self):
        """Starts the PW, assumes it isn't started"""
        self.start = datetime.datetime.utcnow()
        for member in self.members:
            if not member.get_started():
                member.begin(self.start)

    def finish(self):
        """Ends the PW, assumes it isn't ended"""
        self.end = datetime.datetime.utcnow()
        for member in self.members:
            if not member.get_finished():
                member.finish(self.end)

    def join(self, member):
        """Have a new member join the PW."""
        if PW_Member(member) not in self.members:
            new_mem = PW_Member(member)
            if self.get_started():
                new_mem.begin(datetime.datetime.utcnow())
            self.members.append(new_mem)
            return True
        else:
            return False

    def leave(self, member):
        """Have a member in the PW leave the PW."""
        if PW_Member(member) in self.members:
            for user in self.members:
                if user == PW_Member(member):
                    if user.get_finished():
                        return 2
                    else:
                        user.finish(datetime.datetime.utcnow())
            for user in self.members:
                if not user.get_finished():
                    return 0
            self.finish()
            return 0
        else:
            return 1


class PW_Member:

    __slots__ = ['user', 'start', 'end']

    def __init__(self, user):
        self.user = user
        self.start = None
        self.end = None

    def __str__(self):
        return str(self.user)

    def __eq__(self, other):
        return isinstance(other, PW_Member) and self.user == other.user

    def get_len(self):
        if self.end is None:
            return -1
        else:
            return self.start - self.end

    def get_started(self):
        return self.start is not None

    def get_finished(self):
        return self.end is not None

    def begin(self, time):
        self.start = time

    def finish(self, time):
        self.end = time


def setup(bot):
    bot.add_cog(Commands(bot))
