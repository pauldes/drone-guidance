/* HIJACK & GUIDANCE PROJECT */
/*        INSA Lyon          */
/*   P.Désigaud / A.Stoica   */

var pictureCount = 0
main();

/*****************************/

function main(){

  console.log("Launching foo.js script");
  var arDrone = require('ar-drone');
  console.log("Connecting to the drone...");
  var client = arDrone.createClient();
  console.log("Success ! Starting operations");

//  client.takeoff();

  takePhoto(client);

  client

//    .after(5000, function() {this.clockwise(1);})
//    .after(5000, function() {this.clockwise(0.5);})
      .after(10000, function() {takePhoto(client);})
//    .after(5000, function() {this.counterClockwise(0.5);})
//    .after(3000, function() {this.animate('flipLeft', 15);})
//    .after(5000, function() {this.stop();this.land();})
      ;

  client.after(10000, function() {takePhoto(client);});


  }

function takePhoto(client,suffix) {

  var fs = require('fs');
  var pngStream = client.getPngStream();

  var dir = './img/'

  pngStream.once('data', function (data) { // 'once' could be 'on'
      var now = new Date();
      var nowFormat = getDateTime();

      fs.writeFile(dir + nowFormat + '#'+ pictureCount + '.png', data, function (err) {
          if (err)
              console.error(err);
          else
              console.log('Photo saved');
              pictureCount++;
      })
  });
}

function getDateTime() {
    var date = new Date();
    var hour = date.getHours();
    hour = (hour < 10 ? "0" : "") + hour;
    var min  = date.getMinutes();
    min = (min < 10 ? "0" : "") + min;
    var sec  = date.getSeconds();
    sec = (sec < 10 ? "0" : "") + sec;
    //var year = date.getFullYear();
    var month = date.getMonth() + 1;
    month = (month < 10 ? "0" : "") + month;
    var day  = date.getDate();
    day = (day < 10 ? "0" : "") + day;
    return day + "-" + month + "@" + hour + "-" + min + "-" + sec;
}


