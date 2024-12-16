import nextcord; from nextcord import Embed, Color
from nextcord.ext import commands; from nextcord.ext.commands import Context
import json
from tinydb import TinyDB, Query
import os; os.system('cls' if os.name == 'nt' else 'clear')
import random

with open('config.json') as f:
    config = json.load(f)
    ownerid = config['owner_id']

db = TinyDB('db.json')
users_table = db.table('users')

intents = nextcord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

def isuserindb(user_id):
    User = Query()
    user = users_table.get(User.id == user_id)
    if not user:
        users_table.insert({'id': user_id, 'balance': 0})
        
def getbal(user_id):
    User = Query()
    user = users_table.get(User.id == user_id)
    return user['balance']

def addbal(user_id, amount):
    User = Query()
    user = users_table.get(User.id == user_id)
    users_table.update({'balance': user['balance'] + amount}, User.id == user_id)
    
def removebal(user_id, amount):
    User = Query()
    user = users_table.get(User.id == user_id)
    users_table.update({'balance': user['balance'] - amount}, User.id == user_id)
    
def setbal(user_id, amount):
    User = Query()
    users_table.update({'balance': amount}, User.id == user_id)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.id}')
    

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("An error occurred while executing the command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required arguments. Please check your command usage!")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command. Please check the available commands.")
    else:
        raise error
    
@client.command(aliases='bal')
async def balance(ctx: Context):
    isuserindb(ctx.author.id)
    
    embed = Embed(
        title=f"{ctx.author.name}'s Balance",
        description=f"💰 {getbal(ctx.author.id)} coins",
        color=Color.random()
    )
    
    await ctx.send(embed=embed)
    
@client.command()
async def work(ctx: Context):
    isuserindb(ctx.author.id)
    
    work_list = [
        'Discord Mod', 'Minecraft Mod', 'McDonalds Cashier', 'Wobmart Cleaner', 'Teacher', 'Doctor', 'Lawyer',
        'Engineer', 'Scientist', 'Programmer', 'Artist', 'Musician', 'Nurse', 'Seller', 'Reseller'
    ]
    
    work_place = [
        'Discord', 'Minecraft', 'McDonalds', 'Wobmart', 'Badland', 'Space', 'The Moon', 'Hypixel', 'River', 'Sea',
        'Ocean', 'Cave', 'Nether', 'The Heaven', 'The Basement', 'Your Room', 'The Future', 'The Air-Condition' 
    ]
    
    random_work = random.choice(work_list)
    random_place = random.choice(work_place)
    random_amount = random.randint(100,500)
    
    addbal(ctx.author.id, random_amount)
    
    embed = Embed(
        title=f"{ctx.author.name} worked as...",
        description=f"You worked as {random_work} in {random_place} and earned **{random_amount} coins**!",
        color=Color.random()
    )
    
    await ctx.send(embed=embed)
    
@client.command()
async def give(ctx: Context, target: nextcord.Member, amount: int):
    if target is None:
        await ctx.send(f"You must specify a user to give coins to!\n```Usage: {client.command_prefix}give <target> <amount>")
        return
    
    if amount < 1:
        await ctx.send(f"You must give at least 1 coin!\n```Usage: {client.command_prefix}give <target> <amount>")
        return
    
    if amount > getbal(ctx.author.id):
        await ctx.send(f"You don't have enough coins to give that amount!\n```Usage: {client.command_prefix}give <target> <amount>")
        return
    
    isuserindb(ctx.author.id)
    isuserindb(target.id)
    
    removebal(ctx.author.id, amount)
    addbal(target.id, amount)
    
    embed = Embed(
        title=f"{ctx.author.name} gave {target.name}...",
        description=f"You gave {target.mention} **{amount} coins**!",
        color=Color.random()
    )
    
    await ctx.send(embed=embed)
    
@client.command()
async def addcoin(ctx: Context, target: nextcord.Member, amount: int):
    if ctx.author.id != ownerid:
        await ctx.send(f"You don't have permission to use this command!")
        return
    
    if target is None:
        await ctx.send(f"You must specify a user to add coins to!\n```Usage: {client.command_prefix}addcoin <target> <amount>")
        return
    
    if amount < 1:
        await ctx.send(f"You must give at least 1 coin!\n```Usage: {client.command_prefix}addcoin <target> <amount>")
        return
    
    isuserindb(target.id)
    addbal(target.id, amount)
    
    embed = Embed(
        description=f"Successfully added {amount} coins to {target.mention}!",
        color=Color.green()
    )
    
    await ctx.send(embed=embed)
    
@client.command()
async def removecoin(ctx: Context, target: nextcord.Member, amount: int):
    if ctx.author.id != ownerid:
        await ctx.send(f"You don't have permission to use this command!")
        return
    
    if target is None:
        await ctx.send(f"You must specify a user to remove their coins!\n```Usage: {client.command_prefix}removecoin <target> <amount>")
        return
    
    if amount < 1:
        await ctx.send(f"You must give at least 1 coin!\n```Usage: {client.command_prefix}removecoin <target> <amount>")
        return
    
    isuserindb(target.id)
    removebal(target.id, amount)
    
    embed = Embed(
        description=f"Successfully removed {amount} coins from {target.mention}!",
        color=Color.green()
    )
    
    await ctx.send(embed=embed)
    
@client.command()
async def setcoin(ctx: Context, target: nextcord.Member, amount: int):
    if ctx.author.id != ownerid:
        await ctx.send(f"You don't have permission to use this command!")
        return
    
    if target is None:
        await ctx.send(f"You must specify a user to set their coins!\n```Usage: {client.command_prefix}setcoin <target> <amount>")
        return
    
    isuserindb(target.id)
    setbal(target.id, amount)
    
    embed = Embed(
        description=f"Successfully set {target.mention}'s coins to {amount}!",
        color=Color.green()
    )
    
    await ctx.send(embed=embed)
    
client.run(config['token'])
