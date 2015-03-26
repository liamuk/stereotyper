var casper = require('casper').create();
/*casper.on('remote.message', function(msg) {
    this.echo('remote message caught: ' + msg);
})*/

function url_to_username(url) {
    var start = url.lastIndexOf("/")+1;
    if (url.lastIndexOf("?") != -1) {
        var end = url.lastIndexOf("?");
    }
    else {
        var end = url.length
    }
    return url.substr(start, end-start);
}

var page_url = casper.cli.get(0);
username = url_to_username(page_url);
var email = "testtest123123@safetymail.info";
var pass = "dfg580";
var results = []

function graph_search(self) {
    return self.evaluate(function() {
        var results = [];
        //query = document.querySelectorAll('div._zs.fwb > a');
        query = document.querySelectorAll('div._gll > a');
        console.log(query.length + ' results found');
        for (var i=0; i<query.length; ++i) {
            results.push(query[i].href);
        }
        return results;
    });
}

casper.start('http://www.facebook.com/login.php', function() {
    this.fill('#login_form', {'email': email, 'pass':pass}, true)
});
casper.waitForSelector('._586i', function(){
    this.viewport(1366, 9000);
});
casper.thenOpen(page_url, function() {
});
// casper.waitForSelector('div._zs.fwb').wait(3000, function(){
casper.waitForSelector('div._gll').wait(1500, function(){
    results = graph_search(this);
    for (var i=0; i<results.length; ++i) {
        this.echo(url_to_username(results[i]));
    }
});
casper.run();
