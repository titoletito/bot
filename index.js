const Discord = require('discord.js')
const client = new Discord.Client


client.login(process.env.TOKEN)

client.on('message', function (message) {
	if ( message.content === '-test' ) {
	message.channel.send('Tout est OK, enfin pour l\'instant.') }
	if ( message.content === '-message' ) {
	message.reply('Dsl tu est maigre, trop maigre....') }
	if ( message.content === '-invisible' && channel.user.id === '335118921088630796' ) {
	Presence.status(invisible)  }
})
