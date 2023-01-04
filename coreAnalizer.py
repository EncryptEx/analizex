try:
    from alive_progress import alive_bar
    from lars import apache
    import requests
    from texttable import Texttable
except ImportError as e: 
    print(e)
    print("please install it with 'pip install -r requirements.txt'")
    quit(1)

reqTreshold = 1
def readData():
    statuses = {}
    uris = {}
    ips = {}
    IpsTimestamps = {}
    enum = {}
    f = open('log.txt')
    length = len(f.readlines())
    print("Parsing data...")
    with open('log.txt') as f1:
        with apache.ApacheSource(f1) as source:
            with alive_bar(length) as bar:
                for row in source:
                    bar()
                    path = row.request.url.path_str
                    uris[path] = uris.get(path, 0) +1
                    statuses[row.status] = statuses.get(row.status, 0) +1
                    ip = str(row.remote_host)
                    ips[ip] = ips.get(ip, 0) +1

                    lastTimestamp = IpsTimestamps.get(ip, None)
                    # get difference between last ip's request
                    if(lastTimestamp != None and row.time.timestamp() - lastTimestamp < reqTreshold):
                        # last req was also from itself
                        # possible enumerator
                        enum[ip] =enum.get(ip, 0)+1
                    IpsTimestamps[ip] = row.time.timestamp()
    return (uris, ips, enum)

def consoleOutput(cachedData):
    print("Starting report")
    top = 5
    uriOcurrences, ips, enum = cachedData
    topPaths = sorted([(value, key) for (key,value) in uriOcurrences.items()], reverse=True)
    topIPs = sorted([(value, key) for (key,value) in ips.items()], reverse=True)
    enum = sorted([(value, key) for (key,value) in enum.items()], reverse=True)
    
    print("\nTop accessed paths: (top",str(top)+")")
    table_paths = Texttable()
    table_paths.header(['Times', 'Path'])
    for i in range(top if len(topPaths)>top else len(topPaths)):
        times, uri = topPaths[i]
        table_paths.add_row([times,uri])
    print(table_paths.draw())

    
    print("\nTop most req. IP enumerations (top",str(top)+")")
    table_ip = Texttable()
    table_ip.header(['Times', 'IP', 'IP Country'])
    for i in range(top):
        times, ip = topIPs[i]
        table_ip.add_row([times,ip, getIpLoc(ip)])
    print(table_ip.draw())



    print("\n# Possible spray 'n prayers")
    table_enum = Texttable()
    table_enum.header(['Req. '+str(reqTreshold)+'\" between','IP', 'IP Country'])
    for i in range(top):
        times, ip = enum[i]        
        table_enum.add_row([times,ip, getIpLoc(ip)])
    print(table_enum.draw())


    print("\n## Wordpress directory enumeration trials (top",str(top)+")")
    table_wp = Texttable()
    table_wp.header(['Times', 'Path'])
    l=0
    for i in range(len(topPaths)):
        times, uri = topPaths[i]
        if(uri.startswith("/wp") and l<=top):
            l+=1
            table_wp.add_row([times,uri])
    print(table_wp.draw())

    

    # sudo goaccess log.txt --log-format=COMBINED -a -o report.html
    # there's a library forthat     
ipLoc = {}
def getIpLoc(ip): 
    if(ipLoc.get(ip, None) == None):
        url = f"http://ip-api.com/json/{ip}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                country = data['country']
            else:
                country = ""
        except:
            country = ""
    else:
        country = ipLoc.get(ip, None)
    return country