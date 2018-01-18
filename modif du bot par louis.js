const  Discord  =  require ( ' discord.js ' )
const  client  =  nouveau  Discord.Client


client . login ( processus : env . TOKEN )

client . on ( ' ready ' , function () {
	client . utilisateur . setGame ( ' vous surveiller. [-help] ' )
	console . log ( ' Bot Ready! ' )})

client . on ( ' message ' , fonction ( message ) {
	si ( un message . guilde . id  ===  ' 388393287335280640 ' ) {
  
  	if ( message . content  ===  ' -test ' ) {
	un message . canal . envoyer ( ' Tout est OK, enfin verser l \' instant. ' )}
	
  if ( message . content  ===  ' -help ' ) {
	un message . canal . send ( ' Voici la liste des commandes disponibles: \ n -test: si le bot repond c \' est que tout est OK \ n -aide: affiche le menu d \ ' aide \ n -source-code: affiche le code source . ' )}
	
                             if ( message . content  ===  ' -source-code ' ) {
	un message . canal . envoyer ( ' is Le code source disponible à l \' adresse suivante: https://github.com/anonymocraft/bot/ ' )}
 }}) 
