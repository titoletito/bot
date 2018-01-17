const Discord = require('discord.js')
const client = new Discord.Client


client.login(process.env.TOKEN)

client.on('message', function (message) {
	if ( message.content === '-test' ) {
	message.channel.send('Tout est OK, enfin pour l\'instant.') }
})
