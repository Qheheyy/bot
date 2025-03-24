import discord
from discord.ext import commands
import asyncio

# Bot Setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to log pings
ping_logs = []

# ✅ Ping Alert System
@bot.event
async def on_message(message):
    if message.mentions:
        embed = discord.Embed(
            title="🔔 User Ping Alert",
            description=f"{message.author.mention} pinged someone!",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Ping Logger")
        await message.channel.send(embed=embed)
        ping_logs.append(f"{message.author} pinged at {message.created_at}")
    
    await bot.process_commands(message)

@bot.command()
async def viewpings(ctx):
    """Shows the last 10 logged pings"""
    logs = "\n".join(ping_logs[-10:]) or "No pings logged yet!"
    embed = discord.Embed(title="🔵 Ping Log", description=logs, color=discord.Color.blue())
    await ctx.send(embed=embed)

# ✅ Moderation Commands
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    """Kick a user"""
    await member.kick(reason=reason)
    embed = discord.Embed(title="👢 User Kicked", description=f"{member.mention} was kicked.", color=discord.Color.red())
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    """Ban a user"""
    await member.ban(reason=reason)
    embed = discord.Embed(title="🚫 User Banned", description=f"{member.mention} was banned.", color=discord.Color.red())
    await ctx.send(embed=embed)

# ✅ Interactive Punishment Panel
@bot.command()
@commands.has_permissions(manage_messages=True)
async def punish(ctx, member: discord.Member):
    """Creates a punishment panel with buttons"""
    view = PunishView(member)
    embed = discord.Embed(title="⚠️ Punishment Panel", description=f"Select an action for {member.mention}.", color=discord.Color.orange())
    await ctx.send(embed=embed, view=view)

class PunishView(discord.ui.View):
    def __init__(self, member):
        super().__init__()
        self.member = member

    @discord.ui.button(label="Warn", style=discord.ButtonStyle.blurple)
    async def warn(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="⚠️ Warning", description=f"{self.member.mention} has been warned.", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Kick", style=discord.ButtonStyle.red)
    async def kick(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.member.kick(reason="Violation")
        embed = discord.Embed(title="👢 User Kicked", description=f"{self.member.mention} was kicked.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Ban", style=discord.ButtonStyle.red)
    async def ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.member.ban(reason="Violation")
        embed = discord.Embed(title="🚫 User Banned", description=f"{self.member.mention} was banned.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

# ✅ Embed Ticket System
ticket_channels = {}

@bot.command()
async def ticket(ctx):
    """Creates a ticket"""
    category = discord.utils.get(ctx.guild.categories, name="Tickets")
    if not category:
        category = await ctx.guild.create_category("Tickets")

    ticket_channel = await ctx.guild.create_text_channel(name=f"ticket-{ctx.author.name}", category=category)
    ticket_channels[ctx.author.id] = ticket_channel.id
    embed = discord.Embed(title="🎟️ Ticket Opened", description=f"Your ticket has been created: {ticket_channel.mention}", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command()
async def close(ctx):
    """Closes a ticket"""
    if ctx.channel.id in ticket_channels.values():
        await ctx.channel.delete()
    else:
        await ctx.send("This is not a valid ticket channel!")

# ✅ Utility Commands
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    """Displays user avatar"""
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Color.blue())
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    """Displays server information"""
    embed = discord.Embed(title=f"🌐 {ctx.guild.name} Info", color=discord.Color.blue())
    embed.add_field(name="Members", value=ctx.guild.member_count)
    embed.add_field(name="Owner", value=ctx.guild.owner)
    embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    """Checks bot latency"""
    embed = discord.Embed(title="🏓 Pong!", description=f"Latency: {round(bot.latency * 1000)}ms", color=discord.Color.green())
    await ctx.send(embed=embed)

# ✅ Customizable Prefix
@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, new_prefix):
    """Change bot prefix"""
    bot.command_prefix = new_prefix
    embed = discord.Embed(title="✅ Prefix Changed", description=f"New prefix: `{new_prefix}`", color=discord.Color.green())
    await ctx.send(embed=embed)

# Run the bot
bot.run("MTE4OTM4NDA5MTI3MTk2Njc2MQ.Gfms0Z.mAYAu2jZXen6kEMgKUrpVRUvxsgHpBTqiALXfA")
