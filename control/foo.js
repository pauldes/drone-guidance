/* HIJACK & GUIDANCE PROJECT */
/*        INSA Lyon          */
/*   P.Désigaud / A.Stoica   */

var pictureCount = 0
main();

/*****************************/

function main(){

  //findTarget("../img/30-10@11-18-59#0.png",1000);

  console.log("Launching foo.js script");
  var arDrone = require('ar-drone');
  console.log("Connecting to the drone...");
  var client = arDrone.createClient({'frameRate':'0.1'});
  client.animateLeds('blinkGreen', 5, 1)
  console.log("Success ! Starting operations");

  client.takePhotoStream(client);

//  client.takeoff();

//  client
//    .after(5000, function() {this.clockwise(1);})
//    .after(10000, function() {takePhoto(client);})
//    .after(5000, function() {this.counterClockwise(0.5);})
//    .after(3000, function() {this.animate('flipLeft', 15);})
//    .after(5000, function() {this.stop();this.land();})
//    .after(10000, function() {process.exit();})
//      ;
  }

function takePhotoStream(client) {

  var fs = require('fs');
  var pngStream = client.getPngStream();

  var dir = '../img/';

  pngStream.on('data', function (data) { // 'once' could be 'on'

      var nowFormat = getDateTime();

      fs.writeFile(dir + nowFormat + '#'+ pictureCount + '.png', data, function (err) {
          if (err)
              console.error(err);
          else
              client.animateLeds('blinkRed', 5, 1)
              console.log('Photo saved');
              findTarget(dir + nowFormat + '#'+ pictureCount + '.png',4000);
              pictureCount++;

      })
  });
}

function takePhoto(client) {

  var fs = require('fs');
  var pngStream = client.getPngStream();

  var dir = '../img/';

  pngStream.once('data', function (data) { // 'once' could be 'on'

      var nowFormat = getDateTime();

      fs.writeFile(dir + nowFormat + '#'+ pictureCount + '.png', data, function (err) {
          if (err)
              console.error(err);
          else
              console.log('Photo saved');
              findTarget(dir + nowFormat + '#'+ pictureCount + '.png',4000);
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

function findTarget(img_url, period) {

  var python_script_url = '../vision/'+'detect_blobs.py';

  var spawn = require('child_process').spawn;
  var process = spawn('python',[python_script_url,img_url,period]);

  process.stdout.on('data',function(data){

    if( ! data.toString().startsWith('{')){
      console.log(data.toString());
    }
    else{
      var jsonData = JSON.parse(data.toString());
      var radius = jsonData['r'];
      var vector_x = jsonData['vx'];
      var vector_y = jsonData['vy'];
      console.log('data retrieved');
    }

  });

}


