/* HIJACK & GUIDANCE PROJECT */
/*        INSA Lyon          */
/*   P.Désigaud / A.Stoica   */

var currentPictureCount = 0;
var currentRadius = 0;
var dir = 'bin/';
var FRAMERATE_TRACKING = 0.1;
var TRESHOLD_UP = -20;
var TRESHOLD_DOWN = 20;

main();

/*****************************/

function main(){

  //findTarget("../img/30-10@11-18-59#0.png",1000);

  console.log("Launching foo.js script");
  var arDrone = require('ar-drone');
  console.log("Connecting to the drone...");
  var client = arDrone.createClient({'frameRate':FRAMERATE_TRACKING});
  client.animateLeds('snakeGreenRed', 5, 1)
  console.log("Success ! Starting operations");

  takePhotoStream(client);

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

  pngStream.on('data', function (data) { // 'once' OR 'on'

      var nowFormat = getDateTime();

      fs.writeFile(dir + nowFormat + '#'+ currentPictureCount + '.png', data, function (err) {
          if (err)
              console.error(err);
          else
              client.animateLeds('blinkOrange', 5, 1);
              console.log('Photo saved');
              findTarget(dir + nowFormat + '#'+ currentPictureCount + '.png',(1000/FRAMERATE_TRACKING)-2000,client);
              currentPictureCount++;

      })
  });
}

function takePhoto(client) {

  var fs = require('fs');
  var pngStream = client.getPngStream();

  pngStream.once('data', function (data) { // 'once' could be 'on'

      var nowFormat = getDateTime();

      fs.writeFile(dir + nowFormat + '#'+ currentPictureCount + '.png', data, function (err) {
          if (err)
              console.error(err);
          else
              //console.log('Photo saved');
              findTarget(dir + nowFormat + '#'+ currentPictureCount + '.png',4000);
              currentPictureCount++;

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

function findTarget(img_url, period, client) {

  console.log('Finding target...');

  var python_script_url = 'detect_blobs.py';
  var real_img_url = img_url;

  console.log(real_img_url);

  var spawn = require('child_process').spawn;
  var process = spawn('python',[python_script_url,real_img_url,period]);

  process.stderr.on('data',function(data){
    console.log('PYTHON ERROR: '+data.toString());
  });

  process.stdout.on('data',function(data){

    if( ! data.toString().startsWith('{')){
      client.animateLeds('blinkRed', 5, 1);
      console.log(data.toString());
    }
    else{
      client.animateLeds('blinkGreen', 5, 1)
      var jsonData = JSON.parse(data.toString());
      var r = jsonData['r'];
      var vx = jsonData['vx'];
      var vy = jsonData['vy'];
      console.log('I should '+getNextAction(r,vx,vy));
    }
  });

}

function getNextAction(r,vx,vy){
  var old_r = currentRadius;
  var direction = 'unexpected';
  if(vy<TRESHOLD_UP){
    direction = 'GO_UP';
  } else
  if (vy>TRESHOLD_DOWN){
    direction = 'GO_DOWN';
  } else
  {
    direction = 'WAIT';
  }
  return direction;
}

function doAction(action_keyword,client){

  switch(action_keyword) {
      case 'GO_UP':
          client.up(0.2);
          //TODO limit ? or going upward forever ? stop() ?
          break;
      case 'GO_DOWN':
          client.down(0.2);
          //TODO limit ? or going downward forever ?
          break;
      default:
          console.log(action_keyword);
  }

}


