import click
import sqlite3
import dabest   

@click.group()
def cli():
    """Cdabest: Character Database Thing"""

def nodb():
    if click.confirm("We can't find the database. Create a new one?"):
        newdb()
        
@cli.command('newdb')
def newdb():
    """Create a new database. Remove the old one with no mercy."""
    click.echo("Creating a new database...")
    dabest.droptables()
    dabest.createNewDatabase()
    click.echo("Done.")
    
@cli.command('seeallchars')
def seeallchars():
    """See all the characters you've made."""
    try:
        allchars = dabest.listAllChars()
    except sqlite3.OperationalError: #gonna have to make custom exception handling here
        nodb()
        
    if len(allchars) <= 0:
        click.echo("You haven't created any characters!")
    else:
        click.echo("These are all the characters you've created:")
        for character in allchars:
            click.echo("{}. Name: {}".format(character[0], character[1]))  

@cli.command()
@click.option("--charid", prompt="Insert character's ID", type=int)
def seeChar(charid):
    """See or edit a character's profile."""
    click.echo("You're seeing profile with the ID {}!".format(charid) )
    character = dabest.getChar(charid)
    if character == "NOCHAR":
        click.echo("There isn't anyone with that ID")
        return
    
    for dataname in character:
        click.echo("{}: {}".format(dataname, character[dataname]))
        
    click.echo("""
    Commands:
        add [datalabel]: Add a new information to this profile. 
        remove [datalabel]: Remove an information (note that you can't remove name). 
        change [datalabel]: Change an existing data. \nexit: Leave.
    """)
    
    while True:
        inp = click.prompt("What do")
        inp = inp.split()
        if len(inp) < 2:
            inp.append(" ")
        elif inp[1] == "i" or inp[1] == "name":
            click.echo("Sorry, you can't mess with those!")
            continue
            
        if inp[0] == "add":
            addCharData(character, inp[1])
        elif inp[0] == "remove":
            removeCharData(character, inp[1])
        elif inp[0] == "change":
            editCharData(character, inp[1])
        elif inp[0] == "exit":
            break
            
def addCharData(character, label):
    if label == " ":
        label = click.prompt("What's the label for this data?")
    if label in character:
        click.echo("That label already exists!")
        return
    content = click.prompt("Alright, what's the info?")
    dabest.addCharData(character['id'], label, content)
    click.echo("Information added!")
    
def removeCharData(character, label):
    if label == " ":
        label = click.prompt("What's the label for this data?")
    if label not in character:
        click.echo("This character doesn't have that info!")
        return
    if click.confirm("We're gonna remove this info labeled {}. You sure?".format(label)):
        dabest.removeCharData(character['id'], label)
    else:
        click.echo("Roger that.")
        return
        
def editCharData(character, label):
    if label == " ":
        label = click.prompt("What's the label for this data?")
    if label not in character:
        click.echo("This character doesn't have that info!")
        return
    content = click.prompt("Alright, what's the info?")
    dabest.editCharData(character['id'], label, content)

@cli.command()
@click.option("--name", prompt="Insert the name of this character")
def newChar(name):
    """Create a new character."""
    click.echo("Adding {} to the database...".format(name))
    dabest.addChar(name)
    click.echo("Character created!")
    
if __name__ == "__main__":
    cli()