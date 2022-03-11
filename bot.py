import discord
import os
from discord.ext import commands
from keep_alive import keep_alive

class Bet:
	def __init__(self, side1, side2, name):
		self.side1 = side1
		self.side1Bets = dict()
		self.side1Total = 0
		self.side2 = side2
		self.side2Bets = dict()
		self.side2Total = 0
		self.name = name
		self.closed = False
	def makeprediction(self, side, user, amount):
		if not self.closed:
			if accounts[user] >= amount:
				accounts[user] -= amount
				if side == self.side1:
					self.side1Total += amount
					self.side1Bets[user] = amount
				else:
					self.side2Total += amount
					self.side2Bets[user] = amount

	def close(self):
		self.closed = True
	def decide(self, side):
		if side == self.side1:
			for user in self.side1Bets:
				share = self.side1Bets[user] / self.side1Total
				gain = self.side1Bets[user] + share * self.side2Total
				accounts[user] += gain
		else:
			for user in self.side2Bets:
				share = self.side2Bets[user] / self.side2Total
				gain = self.side2Bets[user] + share * self.side1Total
				accounts[user] += gain


accounts = dict()
bets = dict()
bot = commands.Bot(command_prefix="%")

@bot.command()	
@commands.cooldown(1,60*60*24, commands.BucketType.user)
async def daily(ctx):
	if ctx.author in accounts:
		accounts[ctx.author] += 100
	else:
		accounts[ctx.author] = 100	
	await ctx.channel.send("100 points added to " + ctx.author.mention)

@bot.command()
async def mypoints(ctx):
	if ctx.author in accounts:
		await ctx.channel.send(ctx.author.mention + " has " + str(accounts[ctx.author]) + " points")
	else:
			await ctx.channel.send(ctx.author.mention + "has 0 points")
		
@bot.command()
async def createbet(ctx, name, side1, side2):
	bets[name] = Bet(side1, side2, name)
	await ctx.channel.send(name + " \n\nVote: " + side1 +" \nor \nVote: " + side2)

@bot.command()
async def vote(ctx, name, side, amount):
	if name not in bets:
		await ctx.channel.send("Bet doesn't exist")
	else:
		bets[name].makeprediction(side, ctx.author, int(amount))
		await ctx.channel.send(ctx.author.mention + " bet " + amount + " points on " + side)

@bot.command()
async def decide(ctx, name, side):
	bets[name].decide(side)
	await ctx.channel.send("Decison was reached and points have been distributed. ")

@bot.command()
async def close(ctx, name):
	bets[name].close()
	await ctx.channel.send(name + " is now closed to all bets.")
keep_alive()
bot.run(os.getenv('token'))

	
	
