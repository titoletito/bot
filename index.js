const Discord = require('discord.js')
const client = new Discord.Client


client.login(process.env.TOKEN)

client.on('ready', function() {
	client.user.setGame('vous surveiller. [-help]')
	console.log('Bot Ready!') } )

client.on('message', function (message) {
	if ( message.guild.id === '388393287335280640' ) {
	
	if ( message.content === '-test' ) {
	message.channel.send('Tout est OK, enfin pour l\'instant.') } 
	
	if ( message.content === '-help' ) {
	message.channel.send('Voici la liste des commandes disponibles : \n -test : si le bot repond c\'est que tout est OK \n -help : affiche le menu d\'aide \n -source-code : affiche le code source.') }
	
	if ( message.content === '-source-code') {
	message.channel.send('Le code source est disponible à l\'adresse suivante : https://github.com/anonymocraft/bot/') } 
 } 
        if ( message.guild.id === '402563276606537738' ) {
		
	}
	} ) 
