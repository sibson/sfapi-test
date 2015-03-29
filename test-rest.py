from datetime import datetime
import os

from simple_salesforce import Salesforce


client = Salesforce(username="scottp+test@heroku.com", password=os.environ['PASSWORD'], security_token=os.environ['TOKEN'])

class Timer():
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = datetime.now()

    def __exit__(self, *args):
        delta = datetime.now() - self.start
        print "{} - {} secs".format(self.name, delta)


with Timer("totalRun"):
    with Timer("query"):
        r = client.query("Select Id, Name, Birthdate__c, FirstName__c, LastName__c from Contact1m__c")

    while not r['done']:
        with Timer("queryMore"):
            r = client.query_more(r['nextRecordsUrl'], True)

    print "Fetched {} total records".format(r['totalSize'])
