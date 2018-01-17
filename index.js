const Discord = require('discord.js')
const client = new Discord.Client


client.login(process.env.TOKEN)

client.on('ready', function() {
	client.user.setGame('vous surveiller.[-help]')
	console.log('Bot Ready!') } )

client.on('message', function (message) {
	if ( message.content === '-test' ) {
	message.channel.send('Tout est OK, enfin pour l\'instant.') } }
