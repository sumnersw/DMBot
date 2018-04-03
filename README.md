DM-Bot

This is a Bot for Discord.
To initialize your bot, create a config.json file with the following format:

{
    "token" : "<your_token_here>",
    "prefix" : "<your_prefix_here>",
    "general" : "<channel_id>",
    "dicechannel" : "<channel_id>",
    "initiativechannel" : "<channel_id>"
}

The token is your unique server token for this bot to connect and send messages to your server.
the general channel is where you would prefer to send the bot join message
the dicechannel channel is where you would prefer to send the dice rolling messages
the initiativechannel channel is where you would prefer to send the initiative messages

You can of course forgo all of those and instead just put message.channel in place of all the 
channels in the send_message() commands.


These are the bot commands:

!roll = roll dice to the channel which the command was sent. The format is the following:
        NdK where N is the number of dice, and K is the size of the die.
        multiple dice can be rolled with a + command or a - command. the format is the same,
        NdK +NdK -NdK 

        the formating is important here, there must be a space before the + or - sign, and no spaces
        should be after it.

!initiative = draw a random card from a deck of cards and send it via private message.
        it's important to note that the card that is drawn from the deck will be removed from 
        the deck and no one else will be able to redraw it till it is shuffled again.

!reveal = tell the initiativechannel what card the user has drawn
        after the card is revealed, the bot will not keep information on what card the user had
        drawn after that and the user will need to draw another one.

!initreset = reshuffles/repopulates the deck of cards.

!cards = the bot will send a message informing you of how many cards are left in the deck.
