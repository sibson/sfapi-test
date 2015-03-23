var jsforce = require('jsforce');
var conn = new jsforce.Connection();

function timer(name, callback) {
	var start = new Date().getTime();
	callback();
	console.log(name + " - " + (new Date().getTime() - start) + " secs");
}

conn.login('scottp+test@heroku.com', process.env.PASSWORD + process.env.TOKEN, function(err, res) {
  if (err) { return console.error(err); }

  var records = [];
  var start = new Date().getTime();

  conn.query("Select Id, Name, Birthdate__c, FirstName__c, LastName__c from Contact1m__c")
  	.on('record', function(record) {
  		if ((records.length % 1000) == 0) {
  			console.log(records.length);
  		}
  		records.push(record);
  	})
  	.on('end', function() {
  		var delta = new Date().getTime() - start;
  		console.log("Total fetch of " + records.length + " records took " + delta + " secs");
  	})
  	.run({autoFetch:true, maxFetch:9999999});

});

// On localhost this took:
// Total fetch of 1000001 records took 14 minutes