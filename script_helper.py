import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import re

import json
import hashlib
import requests
import shutil

RAW_URL = "https://raw.githubusercontent.com/maxuser0/minescript/main/docs/README.md"

OUTPUT_DIR = "md_snippets"
HASH_FILE = ".readme_hash"


def get_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_old_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None


def save_hash(hash_value):
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        f.write(hash_value)


def download_readme():
    response = requests.get(RAW_URL)
    response.raise_for_status()
    return response.text


def clean_header_name(header):
    """
    Converts markdown-escaped text like:
    \\_\\_init()\\_\\_
    into:
    __init()__
    """

    # Remove markdown escaping backslashes
    header = header.replace("\\", "")

    # Remove illegal filename characters
    header = re.sub(r'[<>:"/\\\\|?*]', "_", header)

    return header.strip()


def parse_sections(markdown):
    pattern = re.compile(r"^(#{2,4})\s+(.+)$", re.MULTILINE)

    matches = list(pattern.finditer(markdown))
    sections = []

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)

        content = markdown[start:end].strip()

        title = clean_header_name(match.group(2))

        sections.append({
            "title": title,
            "content": content
        })

    return sections


def save_sections(sections):
    # Clear old snippets
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for section in sections:
        filename = f"{section['title']}.md"

        path = os.path.join(OUTPUT_DIR, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(section["content"])

        print(f"Saved: {filename}")


def update_docs():
    print("Checking for updates...")

    markdown = download_readme()

    new_hash = get_hash(markdown)
    old_hash = load_old_hash()

    if new_hash == old_hash:
        print("No changes detected.")
        return

    print("Changes detected. Rebuilding snippets...")

    sections = parse_sections(markdown)

    save_sections(sections)

    save_hash(new_hash)

    print(f"Done. Parsed {len(sections)} sections.")


if __name__ == "__main__":
    update_docs()

with open("error_conversions.json","r", encoding="utf-8") as f:
    error_conversions = json.load(f)
    print(error_conversions)

class LogModal(discord.ui.Modal, title="Upload Log"):

    log = discord.ui.TextInput(
        label="Paste your log",
        style=discord.TextStyle.paragraph,
        placeholder="Paste log to redact C:Users/#####/...\n" \
        "If this isn't the main bot, be careful with what you share!",
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction):
        content = self.log.value

        anon_log = re.sub(r"(C:[/\\]Users[/\\])[^/\\]+", r"\1#####", content)
    

        await interaction.response.send_message(
            "Redacted Log:\n```\n"+anon_log+"```"
        )
        
class FixModal(discord.ui.Modal, title="Upload Log"):

    log = discord.ui.TextInput(
        label="Paste your log",
        style=discord.TextStyle.paragraph,
        placeholder="Paste your log to get a quick fix.\n" \
        "If this isn't the main bot, be careful with what you share!",
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction):
        content = self.log.value
        
        for line in content.splitlines():
            for key in error_conversions.keys():
                if key in line:
                    with open("errors/"+error_conversions[key]+".md", "r") as f:
                        await interaction.response.send_message(f.read(), ephemeral=True)
                        return
        
        await interaction.response.send_message("Hmm.. nothing in the common error catologue.", ephemeral=True)

    



files = os.listdir("topics")
topics = []
for topic in files:
    topics.append(topic.removesuffix(".md"))

files = os.listdir("md_snippets")
wikis = []
for wiki in files:
    wikis.append(wiki.removesuffix(".md"))
# Load environment variables
load_dotenv()

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
intents.members = True          # Required for member-related events

# Initialize bot
bot = commands.Bot(command_prefix="+", intents=intents, help_command=None)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready!")
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game("with you!"))

# Example command
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command(name="t")
async def topic(ctx, page=None):
    
    if not page is None:
        
        req = page.lower()
        if req in topics:
            with open("topics/"+req+".md","r") as f:
                await ctx.send(f.read())
        else:
            await ctx.message.add_reaction("❌")
    
    else:
        resp = """
`+t topic` | Get information on a topic

topics: 
"""
        for topic in topics:
            resp += topic+", "
        resp.removesuffix(", ")
        
        await ctx.send(resp)

@bot.command(name="refresh")
async def refresh(ctx):
    global topics, error_conversions
    files = os.listdir("topics")
    topics = []
    for topic in files:
        topics.append(topic.removesuffix(".md"))
    
    with open("error_conversions.json","r") as f:
        error_conversions = json.load(f)

    
    await ctx.message.add_reaction("🔄")
    
@bot.command(name="format")
async def format(ctx):
    msg = ctx.message
    if msg.reference:
        try:
             # Try to use the cached message first
            original_message = msg.reference.resolved 
            if original_message is None:
                # If not in cache, fetch the message from the API
                original_message = await msg.channel.fetch_message(msg.reference.message_id)
            await msg.channel.send("```python\n"+original_message.content+"```")
        except:
            pass
    else:
        await ctx.send("Respond to a message to use this command.")

@bot.command(name="help")
async def get_help(ctx):
    resp = """
**Welcome to the Script Helper bot!**
Current commands:
```
+t <topic>      | Quickly get information on a topic!
+quickfix <log> | Reply to or paste a log to get a quick fix!
+format         | Reply to a message to format as python code!
+refresh        | Refresh .md cache
+ping           | Get ping stats
==== PRIVATE COMMANDS =====
/quickfix       | Privately share a log and get a quick fix!
/redactlog      | Paste a log to redact it!
```
"""

    await ctx.send(resp)


def find_fix(lines: str):
    for line in lines:
        for key in error_conversions.keys():
            if key in line:
                with open("errors/"+error_conversions[key]+".md","r") as f:
                    
                    return f.read()
    
    return None

@bot.command(name="w")
async def getwiki(ctx, page=None):
    if not page is None:
        
        req = page
        if req in wikis:
            with open("md_snippets/"+req+".md","r") as f:
                await ctx.send(f.read())
        else:
            await ctx.message.add_reaction("❌")
    
    else:
        resp = """
`+w wikipage` | Get information on a specific wiki page

These are indicated by:

`##`, `###`, and `####` on the minescript wiki!
"""
    
        
        await ctx.send(resp)
    

@bot.command(name="quickfix")
async def quickfix(ctx):
    msg = ctx.message
    original_message = None
    

    if msg.reference:
        try: 
            
            original_message = msg.reference.resolved

            if original_message is None:
            
                original_message = await msg.channel.fetch_message(msg.reference.message_id)


        except:
            pass
    
    if original_message is None:
        lines = msg.content.splitlines()
    else:
        lines = original_message.content.splitlines()
    
    

    for line in lines:
        for key in error_conversions.keys():
            if key in line:
                with open("errors/"+error_conversions[key]+".md","r") as f:
                    await ctx.send(f.read())
                    return
    
    if msg.content == "+quickfix":
        await ctx.send("`+quickfix` | Paste a log or respond to one to get a quick fix!")
    else:
        await ctx.send("Hmm.. nothing in the common error catologue.")

@bot.tree.command(name="redactlog", description="Redact a log before uploading it.")
async def upload_log(interaction: discord.Interaction):
    await interaction.response.send_modal(LogModal())

@bot.tree.command(name="quickfix", description="Upload a log to get a quick fix suggestion (not shown to others).")
async def anon_fix(interaction: discord.Interaction):
    await interaction.response.send_modal(FixModal())

# Main entry point
if __name__ == "__main__":


    # Run bot
    bot.run(os.getenv("DISCORD_TOKEN"))   