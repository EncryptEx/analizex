from importlib import reload
import sys
import coreAnalizer
import click

debug = False

modesList = ['topPaths','topIps','topSprayNPrayers','topWordpress']
part1Cache = None

@click.command()
@click.option('--top', default=5, help='The number of rows to show in each category (5 by default)')
@click.option('--output', default="console", help='Specify the type of output (console by default): console/html')
@click.option('--categories', default="all", help='Sets the categories to show (all by default): all/'+'/'.join(modesList))
@click.option('--ipgeoloc', default=False, help='Shows IP Geolocation (uses external API), disabled by default')
@click.option('--reqtreshold', default=1, help='Time between requests to determine that they are enumerators/crawlers. 1\" by default')
@click.argument('filename')
def analize(filename, top, output, categories, ipgeoloc, reqtreshold):
    # Initial CLI parsing
    global part1Cache, modesList
    modes = {}
    if(top < 1 or reqtreshold < 1 ):
        click.echo("Please introduce a valid top/reqteshold number (>1)")
        quit(2)

    if(categories == "all"):
        for mode in modesList:
            modes[mode] = True
    else:
        for category in categories.split(","):
            if(category not in modesList): 
                click.echo("You typed a mode that doesn't exist: "+str(category))
                quit(2)
            modes[category] = True

    # Output parse
    if(output not in ['console', 'html']): 
        click.echo("You typed an output type that doesn't exist: "+str(output))
        exit(2)

    # Main program
    while True:
        if not part1Cache:
            part1Cache = coreAnalizer.readData(filename, reqtreshold)
        if(output == "console"):
            coreAnalizer.consoleOutput(part1Cache, top, modes, ipgeoloc, reqtreshold)
        if(not debug):
            quit(0)
        click.echo("Press enter to re-run the script, CTRL-C to exit")
        sys.stdin.readline()
        reload(coreAnalizer)


if __name__ == "__main__":
    analize()
