"""
    Talos regular event loops. Done as a cog so as to keep clutter out of the main file.

    Author: CraftSpider
"""
import os
import pathlib
import httplib2
import asyncio
import logging
import random
import argparse
import inspect
import utils
import utils.command_lang as command_lang
import datetime as dt
from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

# Google API values
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.dat'
APPLICATION_NAME = 'TalosBot Prompt Reader'

log = logging.getLogger("talos.events")
cl_parser = command_lang.ContextLessCL()


def align_period(period):
    now = dt.datetime.now()
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    if period.days:
        hours = 24 - now.hour
        minutes = 60 - now.minute
        seconds = 60 - now.second
    elif period.hours:
        minutes = 60 - now.minute
        seconds = 60 - now.second
    elif period.minutes:
        seconds = 60 - now.second

    days += period.days - 1
    hours += period.hours - 1
    minutes += period.minutes - 1
    seconds += period.seconds - 1

    return dt.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


class StopEventLoop(Exception):

    def __init__(self, message=None):
        super().__init__(message)
        self.message = message


class EventLoop:

    __slots__ = ("_task", "_callback", "period", "persist", "start_time", "loop")

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Access internal method through self.callback")

    def __init__(self, coro, period, *, persist=True, start_time=None, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._task = None
        self._callback = coro
        self.period = utils.EventPeriod(period)
        self.persist = persist
        self.start_time = start_time
        self.loop = loop

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, value):
        self._callback = value

    def set_start_time(self, time):
        self.start_time = time

    def start(self, *args, **kwargs):
        log.info(f"Starting event loop {self._callback.__name__}")
        self._task = self.loop.create_task(self.run(*args, **kwargs))

    async def run(self, *args, **kwargs):
        if self.start_time is not None:
            now = dt.datetime.now()
            delta = self.start_time - now
            await asyncio.sleep(delta.total_seconds())
        else:
            delta = align_period(self.period)
            await asyncio.sleep(delta.total_seconds())
        while True:
            try:
                await self._callback(*args, **kwargs)
            except StopEventLoop as e:
                if e.message:
                    log.warning(e.message)
                return
            except Exception as e:
                if self.persist:
                    log.warning(f"Ignoring error in event loop {self._callback.__name__}: {e}")
                else:
                    log.error(f"Stopping event loop {self._callback.__name__}: {e}")
                    self._task = None
                    return
            delta = align_period(self.period)
            await asyncio.sleep(delta.total_seconds())

    def stop(self):
        self._task.cancel()


def eventloop(period, *, persist=True, start_time=None):

    def decorator(coro):
        return EventLoop(coro, period, persist=persist, start_time=start_time)

    return decorator


class EventLoops(utils.TalosCog):
    """Handles the Talos regulated events, time based loops. How did you even figure out this help page existed?"""

    __slots__ = ('service', 'flags', 'last_guild_count', 'bg_tasks', "__local_check")

    def __init__(self, bot):
        """Initialize the EventLoops cog. Takes in an instance of Talos to use while running."""
        super().__init__(bot)
        self.service = None
        self.flags = None
        self.last_guild_count = 0
        self.bg_tasks = {}

        members = inspect.getmembers(self)
        for loop in filter(lambda x: isinstance(x[1], EventLoop), members):
            print(loop)
            self.bg_tasks[loop[0]] = loop[1]

    def __unload(self):
        """Cleans up the cog on unload, cancelling all tasks."""
        for task in self.bg_tasks:
            self.bg_tasks[task].stop()

    def start_all_tasks(self):
        """Initializes and starts all event tasks"""
        self.start_prompt()
        for task in self.bg_tasks:
            self.bg_tasks[task].start()

    def start_prompt(self):
        """Starts prompts task"""
        # TODO: something else here. This is not where flags should be handled
        self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        self.service = self.create_service()
        time = dt.datetime.now().replace(hour=self.bot.PROMPT_TIME, minute=0, second=0, microsecond=0)
        if time < dt.datetime.now():
            time += dt.timedelta(days=1)
        self.prompt_task.set_start_time(time)

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        if not pathlib.Path(CLIENT_SECRET_FILE).is_file():
            raise FileNotFoundError("No client secret file")
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store, self.flags)
            print('Storing credentials to ' + credential_path)
        return credentials

    def create_service(self):
        """Creates and returns a google API service"""
        try:
            credentials = self.get_credentials()
            http = credentials.authorize(httplib2.Http())
            discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
            service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url,
                                      cache_discovery=False)
            return service
        except FileNotFoundError:
            log.warning("Couldn't load client_secret.dat for google services")
            return None

    def get_spreadsheet(self, sheet_id, sheet_range):
        """Get a google spreadsheet range from service"""
        result = self.service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=sheet_range).execute()
        return result.get('values', [])

    def set_spreadsheet(self, sheet_id, values, sheet_range=None):
        """Set a google spreadsheet range through service"""
        body = {
            'values': values
        }
        if sheet_range:
            result = self.service.spreadsheets().values().update(
                spreadsheetId=sheet_id, range=sheet_range,
                valueInputOption="RAW", body=body).execute()
        else:
            result = self.service.spreadsheets().values().append(
                spreadsheetId=sheet_id, range=sheet_range,
                valueInputOption="RAW", body=body).execute()
        return result

    @eventloop("1m")
    async def minute_task(self):
        """Called once at the start of every minute"""
        for guild in self.bot.guilds:
            events = self.database.get_guild_events(guild.id)
            for event in events:
                period = int(event.period)
                time = int(dt.datetime.now().timestamp())
                current = int(time / period)
                if current > event.last_active:
                    channel = list(filter(lambda x: x.id == event.channel, guild.channels))[0]
                    log.info("Kicking off event " + event.name)
                    await channel.send(cl_parser.parse_lang(channel, event.text))
                    event.last_active = current
                    self.database.save_item(event)

    @eventloop("1h")
    async def hourly_task(self):
        """Called once at the top of every hour."""
        log.debug("Hourly task runs")
        guild_count = len(self.bot.guilds)
        if self.bot.botlist != "" and guild_count != self.last_guild_count:
            self.last_guild_count = guild_count
            headers = {'Authorization': self.bot.botlist}
            data = {'server_count': guild_count}
            api_url = 'https://discordbots.org/api/bots/199965612691292160/stats'
            await self.bot.session.post(api_url, data=data, headers=headers)

    @eventloop("1d")
    async def daily_task(self):
        """Called once every day at midnight, does most time-consuming tasks."""
        log.debug("Daily task runs")
        self.database.remove_uptime(int((dt.datetime.now() - dt.timedelta(days=30)).timestamp()))

    @eventloop("1m")
    async def uptime_task(self):
        """Called once a minute, to verify uptime. Old uptimes cleaned once a day."""
        log.debug("Uptime task runs")
        self.database.add_uptime(int(dt.datetime.now().replace(microsecond=0).timestamp()))

    @eventloop("1d")
    async def prompt_task(self):
        """Once a day, grabs a prompt from google sheets and posts it to the defined prompts chat, if enabled."""
        if self.service is None:
            raise StopEventLoop("No google service, prompt task quitting")
        log.debug("Prompt task runs")
        prompt_sheet_id = "1bL0mSDGK4ypn8wioQCBqkZH47HmYp6GnmJbXkIOg2fA"
        values = self.get_spreadsheet(prompt_sheet_id, "Form Responses 1!B:E")
        possibilities = []
        values = list(values)
        for item in values:
            if len(item[3:]) == 0:
                possibilities.append(item)
        prompt = random.choice(possibilities)

        log.debug(prompt)
        out = f"__Daily Prompt {dt.date.today().strftime('%m/%d')}__\n\n"
        prompt[0] = prompt[0].strip("\"")
        out += f"{prompt[0]}\n\n"
        original = "Original prompt" if prompt[1].upper() == "YES" else "Submitted"
        out += f"({original} by {prompt[2]})"
        for guild in self.bot.guilds:
            if not self.database.get_guild_options(guild.id).writing_prompts:
                continue
            for channel in guild.channels:
                if channel.name == self.database.get_guild_options(guild.id).prompts_channel:
                    await channel.send(out)

        prompt.append("POSTED")
        self.set_spreadsheet(prompt_sheet_id, [prompt],
                             f"Form Responses 1!B{values.index(prompt) + 1}:E{values.index(prompt) + 1}")


def setup(bot):
    bot.add_cog(EventLoops(bot))
