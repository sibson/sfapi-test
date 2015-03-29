from datetime import datetime
import os
import gc

from sforce.partner import SforcePartnerClient

gc.disable()

client = SforcePartnerClient('./partnerwsdl.xml')
client.login("scottp+test@heroku.com", os.environ['PASSWORD'], os.environ['TOKEN'])
queryOptions = client.generateHeader('QueryOptions')
queryOptions.batchSize = 2000
client.setQueryOptions(queryOptions)


class Timer():
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = datetime.now()

    def __exit__(self, *args):
        delta = datetime.now() - self.start
        print "Last 2000 took {} - {} secs".format(self.name, delta)


total = 0
with Timer("totalRun"):
    with Timer("query"):
        r = client.query("Select Id, Name, Birthdate__c, FirstName__c, LastName__c from Contact1m__c")
    total += len(r.records)
    queryLocator = r.queryLocator
    del r

    done = False
    while not done:
        with Timer("queryMore"):
            r = client.queryMore(queryLocator)
        done = r.done
        queryLocator = r.queryLocator
        del r

    print "Fetched {} total records".format(total)


# Localhost test:
# Fetched 1000001 total records
# totalRun - 0:24:38.476870 (24 mins)
