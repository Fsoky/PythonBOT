import discord
from random import randint, choice
from discord.ext import commands
import datetime, pyowm
import speech_recognition as sr
from discord.utils import get

import os
from time import sleep
import requests

PREFIX = '.'
bad_words = [ 'кик', 'флуд', 'спам', 'бан' ]

client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )

@client.event
async def on_ready():
	print( 'BOT connected' )

	await client.change_presence( status = discord.Status.do_not_disturb, activity = discord.Game( '.help' ) )

@client.event
async def on_command_error( ctx, error ):
	pass
	
@client.event
async def on_member_join( member ):
	channel = client.get_channel( 668428362045456415 )

	role = discord.utils.get( member.guild.roles, id = 668111865527795722 )

	await member.add_roles( role )
	await channel.send( embed = discord.Embed( description = f'Пользователь ``{ member.name }``, присоеденился к нам!',
						 color = 0x3ec95d ) )

# Filter
@client.event
async def on_message( message ):
	await client.process_commands( message )

	msg = message.content.lower()

	if msg in bad_words:
		await message.delete()
		await message.author.send( f'{ message.author.name }, не надо такое писать!' )

@client.command()
async def math( ctx, a : int, arg, b : int ):
	if arg == '+':
		await ctx.send( f'Result: { a + b }' )

	elif arg == '-':
		await ctx.send( f'Result: { a - b }' )

	elif arg == '/':
		await ctx.send( f'Result: { a / b }' )

@client.command()
async def ip_info( ctx, arg ):
	response = requests.get( f'http://ipinfo.io/{ arg }/json' )

	user_ip = response.json()[ 'ip' ]
	user_city = response.json()[ 'city' ]
	user_region = response.json()[ 'region' ]
	user_country = response.json()[ 'country' ]
	user_location = response.json()[ 'loc' ]
	user_org = response.json()[ 'org' ]
	user_timezone = response.json()[ 'timezone' ]

	global all_info
	all_info = f'\n<INFO>\nIP : { user_ip }\nCity : { user_city }\nRegion : { user_region }\nCountry : { user_country }\nLocation : { user_location }\nOrganization : { user_org }\nTime zone : { user_timezone }'

	await ctx.author.send( all_info )

@client.command()
async def key( ctx ):
	import uuid

	await ctx.send( f'Key : { uuid.uuid4() }' )

@client.command()
async def w( ctx, *, arg ):
	owm = pyowm.OWM( 'e4e1efbc1a7afebbbc33ed068b32512c' )
	city = arg

	observation = owm.weather_at_place( city )
	w = observation.get_weather()
	temperature = w.get_temperature( 'celsius' )[ 'temp' ]

	await ctx.send( f'Температура в { city } : { temperature }' )

@client.command()
async def phone_info( ctx, arg ):
	response = requests.get( f'https://htmlweb.ru/geo/api.php?json&telcod={ arg }' )

	user_country = response.json()[ 'country' ][ 'english' ]
	user_id = response.json()[ 'country' ][ 'id' ]
	user_location = response.json()[ 'country' ][ 'location' ]
	user_city = response.json()[ 'capital' ][ 'english' ]
	user_width = response.json()[ 'capital' ][ 'latitude' ]
	user_lenth = response.json()[ 'capital' ][ 'longitude' ]
	user_post = response.json()[ 'capital' ][ 'post' ]
	user_oper = response.json()[ '0' ][ 'oper' ]

	global all_info
	all_info = f'<INFO>\nCountry : { user_country }\nID : { user_id }\nLocation : { user_location }\nCity : { user_city }\nLatitude : { user_width }\nLongitude : { user_lenth }\nIndex post : { user_post }\nOperator : { user_oper }'

	await ctx.author.send( all_info )

# Clear message
@client.command()
@commands.has_permissions( administrator = True )

async def clear( ctx, amount : int ):
	await ctx.channel.purge( limit = amount )

	await ctx.send(embed = discord.Embed(description = f':white_check_mark: Удалено {amount} сообщений', color=0x0c0c0c))

# Kick
@client.command()
@commands.has_permissions( administrator = True )

async def kick( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )
	await member.kick( reason = reason )

	emb = discord.Embed( title = 'Информация об изгнании', description = f'{ member.name.title() }, был выгнан в связи нарушений правил',
	color = 0xc25151 )

	emb.set_author( name = member, icon_url = member.avatar_url )
	emb.set_footer( text = f'Был изганан администратором { ctx.message.author.name }', icon_url = ctx.author.avatar_url )

	await ctx.send( embed = emb )

# Ban
@client.command()
@commands.has_permissions( administrator = True )

async def ban( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )
	await member.ban( reason = reason )

	emb = discord.Embed( title = 'Информация о блокировке участника', description = f'{ member.name }, был заблокирован в связи нарушений правил',
	color = 0xc25151 )

	emb.set_author( name = member.name, icon_url = member.avatar_url )
	emb.add_field( name = f'ID: { member.id }', value = f'Блокированный участник : { member }' )
	emb.set_footer( text = 'Был заблокирован администратором {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

	await ctx.send( embed = emb )

# Unban
@client.command()
@commands.has_permissions( administrator = True )

async def unban( ctx, *, member ):
	await ctx.channel.purge( limit = 1 )

	channel = client.get_channel( 669171863179493386 )

	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user

		await ctx.guild.unban( user )
		
		emb = discord.Embed( title = 'Информация о разбаненом участнике', description = f'{ member.name }, был разблокирован по решению администрации',
		color = 0xc25797 )

		emb.set_author( name = member.name, icon_url = member.avatar_url )
		emb.field( name = f'ID: { member.id }', value = f'Name: { member }' )
		emb.set_footer( text = f'Был разблокирован администратором { ctx.author.name }', icon_url = ctx.author.avatar_url )

		await ctx.send( embed = emb )

		return

# Command help
@client.command()
async def help( ctx ):
	emb = discord.Embed( 
		title = 'Навигация по командам :clipboard:',
		color = 0x7aa13d
	 )

	emb.add_field( name = '**Основные команды**', value = '''
		.time - узнать текущее время :clock3:
		.ip_info - узнать информацию о IP адресе :satellite:
		.phone_info - узнать информацию о номере телефона :iphone:
		.w - узнать температуру в городе
		''' )

	emb.add_field( name = '**Приколюшки**', value = '''
		.hack - взлом сервера :tools:
		.joke - шутка дня :face_with_raised_eyebrow:
		.fsociety - сектретная разработка :gear:
		''' )

	await ctx.send( embed = emb )

@client.command()
async def hack( ctx ):
	for x in range( 3 ):
		await ctx.author.send( f'{ ctx.author.name }, спасибо, что предоставил свои данные!' )

@client.command()
async def joke( ctx, *, arg ):
	global jokes
	jokes = []

	if arg:
		jokes.append( arg )

		await ctx.send( f'Шутка { ctx.author.name }: "{ arg }"' )

@joke.error 
async def joke_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( 'Подкинь шутку' )

@client.command()
async def fsociety( ctx ):
	await ctx.send( 'Разработка' )

@client.command()

async def time( ctx ):
	emb = discord.Embed( title = 'ВРЕМЯ', description = 'Вы сможете узнать текущее время', colour = discord.Color.green(), url = 'https://www.timeserver.ru' )

	emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
	emb.set_footer( text = 'Спасибо за использование нашего бота!' )
	emb.set_thumbnail( url = 'https://sun9-35.userapi.com/c200724/v200724757/14f24/BL06miOGVd8.jpg' )

	now_date = datetime.datetime.now()

	emb.add_field( name = 'Time', value = 'Time : {}'.format( now_date ) )

	await ctx.author.send( embed = emb )

@client.command()
@commands.has_permissions( administrator = True )

async def user_mute( ctx, member: discord.Member, amount : int ):
	await ctx.channel.purge( limit = 1 )

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'mute' )

	await member.add_roles( mute_role )
	await ctx.send( f'У { member.mention }, ограничение чата, за нарушение прав!' )

	sleep( amount )
	await member.remove_roles( mute_role )

@client.command()
async def join( ctx ):
	global voice

	channel = ctx.message.author.voice.channel
	voice = get( client.voice_clients, guild = ctx.guild )

	if voice and voice.is_connected():
		await voice.move_to( channel )

	else:
		voice = await channel.connect()

	await voice.disconnect()

	if voice and voice.is_connected():
		await voice.move_to( channel )

	else:
		voice = await channel.connect()
		print( f'Connected to channel : { channel }' )

	await ctx.send( f'Joined { channel }' )

	while True:
		r = sr.Recognizer()
		
		with sr.Microphone( device_index = 1 ) as source:
			audio = r.listen( source )

		qurey = r.recognize_google( audio, language = 'ru-RU' )
		await ctx.send( f'Услыхал : { qurey.lower() }' )

@client.command()
async def leave( ctx ): 
	await ctx.voice_client.disconnect()

@clear.error 
async def clear_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( embed = discord.Embed( description = f':x:{ ctx.author.mention }, перед использованием команды введите кол-во сообщений, которые хотите удалить!' ) )

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send( f'{ ctx.author.name }, у вас недостаточно прав!' )

# Get token
token = os.environ.get( 'TOKEN_BOT' )

client.run( token )