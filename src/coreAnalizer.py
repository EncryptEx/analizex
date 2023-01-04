try:
    from alive_progress import alive_bar
    from lars import apache
    import requests
    from texttable import Texttable
    import click
except ImportError as e:
    click.echo(e)
    click.echo("please install it with 'pip install -r requirements.txt'")
    quit(1)


def readData(filename, reqTreshold):
    statuses = {}
    uris = {}
    ips = {}
    IpsTimestamps = {}
    enum = {}
    f = open(filename)
    length = len(f.readlines())
    click.echo("Parsing data...")
    with open(filename) as f1:
        with apache.ApacheSource(f1) as source:
            with alive_bar(length) as bar:
                for row in source:
                    bar()
                    path = row.request.url.path_str
                    uris[path] = uris.get(path, 0) + 1
                    statuses[row.status] = statuses.get(row.status, 0) + 1
                    ip = str(row.remote_host)
                    ips[ip] = ips.get(ip, 0) + 1

                    lastTimestamp = IpsTimestamps.get(ip, None)
                    # get difference between last ip's request
                    if (
                        lastTimestamp != None
                        and row.time.timestamp() - lastTimestamp < reqTreshold
                    ):
                        # last req was also from itself
                        # possible enumerator
                        enum[ip] = enum.get(ip, 0) + 1
                    IpsTimestamps[ip] = row.time.timestamp()
    return (uris, ips, enum)


def consoleOutput(cachedData, top, modes, wantsIpGeoLoc, reqTreshold):
    click.echo("Starting report")
    uriOcurrences, ips, enum = cachedData
    topPaths = sorted(
        [(value, key) for (key, value) in uriOcurrences.items()], reverse=True
    )
    topIPs = sorted([(value, key) for (key, value) in ips.items()], reverse=True)
    enum = sorted([(value, key) for (key, value) in enum.items()], reverse=True)

    if modes.get("topPaths", False):
        click.echo("\nTop accessed paths: (top " + str(top) + ")")
        table_paths = Texttable()
        table_paths.header(["Times", "Path"])
        for i in range(top if len(topPaths) > top else len(topPaths)):
            times, uri = topPaths[i]
            table_paths.add_row([times, uri])
        click.echo(table_paths.draw())

    if modes.get("topIps", False):
        click.echo("\nTop most req. IP enumerations (top " + str(top) + ")")
        table_ip = Texttable()
        header = ["Times", "IP"]
        if wantsIpGeoLoc:
            header = ["Times", "IP", "IP Country"]
        table_ip.header(header)
        for i in range(top):
            times, ip = topIPs[i]
            dataToAppend = [times, ip]
            if wantsIpGeoLoc:
                dataToAppend.append(getIpLoc(ip))
            table_ip.add_row(dataToAppend)
        click.echo(table_ip.draw())

    if modes.get("topSprayNPrayers", False):
        click.echo("\n# Possible spray 'n prayers")
        table_enum = Texttable()
        header = ["Req. " + str(reqTreshold) + '" between', "IP"]
        if wantsIpGeoLoc:
            header = ["Req. " + str(reqTreshold) + '" between', "IP", "IP Country"]
        table_enum.header(header)
        for i in range(top):
            times, ip = enum[i]
            dataToAppend = [times, ip]
            if wantsIpGeoLoc:
                dataToAppend.append(getIpLoc(ip))
            table_enum.add_row(dataToAppend)
        click.echo(table_enum.draw())

    if modes.get("topWordpress", False):
        click.echo("\n## Wordpress directory enumeration trials (top " + str(top) + ")")
        table_wp = Texttable()
        table_wp.header(["Times", "Path"])
        l = 0
        for i in range(len(topPaths)):
            times, uri = topPaths[i]
            if uri.startswith("/wp") and l <= top:
                l += 1
                table_wp.add_row([times, uri])
        click.echo(table_wp.draw())

    # sudo goaccess log.txt --log-format=COMBINED -a -o report.html
    # there's a library forthat


ipLoc = {}


def getIpLoc(ip):
    if ipLoc.get(ip, None) == None:
        url = f"http://ip-api.com/json/{ip}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                country = data["country"]
            else:
                country = ""
        except:
            country = ""
    else:
        country = ipLoc.get(ip, None)
    return country
