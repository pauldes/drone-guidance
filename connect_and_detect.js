/* HIJACK & GUIDANCE PROJECT */
/*        INSA Lyon          */
/*   P.Désigaud / A.Stoica   */

var currentPictureCount = 0;
var dir = 'bin/';
var FRAMERATE_TRACKING = 10;
var TRESHOLD_X = 100;
var TRESHOLD_RADIUS = 40;
var EPSILON_RADIUS = 10;
var SPEED_ROTATION = 0.3;
var SPEED_TRANSLATION = 0.2;
var PERIOD_ROTATION = 1000;
var PERIOD_TRANSLATION = 1500;

main();

/*****************************/

function main(){

  console.log("Launching connect_and_detect.js script");
  var arDrone = require('ar-drone');
  console.log("Connecting to the drone...");
  var client = arDrone.createClient({'frameRate':FRAMERATE_TRACKING});
  client.animateLeds('snakeGreenRed', 5, 1)
  console.log("Success ! Starting operations");

  client.takeoff();
  client.after(5000,function(){ doAction('GO_RIGHT',this);})
    .after(PERIOD_ROTATION, function(){this.stop(); doAction('GO_LEFT',this);})
    .after(PERIOD_ROTATION, function(){this.stop();})
    .after(2000,function(){ this.stop(); this.land(); })
    .after(5000, function() {process.exit();});


  //takePhotoStream(client);
  //require('ar-drone-png-stream')(client, { port: 8000 });
  

  //client.takeoff();
  //doAction('GO_BACK',client);

/* client
   .after(5000, function() {this.clockwise(1);})
   .after(10000, function() {takePhoto(client);})
   .after(5000, function() {this.counterClockwise(0.5);})
   .after(3000, function() {this.animate('flipLeft', 15);})
   .after(5000, function() {this.stop();this.land();})
   .after(10000, function() {process.exit();})
     ;*/
  }

function takePhotoStream(client) {

  var fs = require('fs');
  var pngStream = client.getPngStream();
  var period = 10;
  var counter = 10;

  var global_counter = 0;
  var global_limit = 20;

  pngStream.on('data', function (data) { // 'once' OR 'on'

    if(global_counter==global_limit-1){
      client.land();
    } else if(global_counter==global_limit){
      //nothing
    } else {
      if (counter==period){
        global_counter++;
        counter = 0;
        var nowFormat = getDateTime();

        fs.writeFile(dir + nowFormat + '#'+ currentPictureCount + '.png', data, function (err) {
            if (err)
                console.error(err);
            else{
                client.animateLeds('blinkOrange', 5, 1);
                console.log('Photo saved');
                findTarget(dir + nowFormat + '#'+ currentPictureCount + '.png',(1000*period/FRAMERATE_TRACKING),client);
                currentPictureCount++;
            }
        })
      }
      else{
        counter++;
      }
    }
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
      // doAction(getNextAction(r,vx,vy),client);
    }
  });

}

function getNextAction(r,vx,vy){

  if(vx > TRESHOLD_X){
    direction = 'GO_RIGHT';
  }
  else if(vx < - TRESHOLD_X){
    direction = 'GO_LEFT';
  }else if(r > TRESHOLD_RADIUS + EPSILON_RADIUS){
    direction = 'GO_BACK';
  }
  else if(r < TRESHOLD_RADIUS - EPSILON_RADIUS){
    direction = 'GO_FORWARD';
  }
  else{
    direction = 'WAIT';
  }

  return direction;
}

function doAction(action_keyword,client){

  switch(action_keyword) {
      case 'GO_RIGHT':
          console.log("I am starting to go right");
          client.clockwise(SPEED_ROTATION);
          break;  
      case 'GO_LEFT':
          console.log("I am starting to go left");
          client.counterClockwise(SPEED_ROTATION);
          break;    
      case 'GO_FORWARD':
          client.front(SPEED_TRANSLATION);
          client.after(PERIOD_TRANSLATION, function(){this.stop();});
          break;
      case 'GO_BACK':
          client.back(SPEED_TRANSLATION);
          client.after(PERIOD_TRANSLATION, function(){this.stop();});
          break;
      default:
          client.stop();
          console.log(action_keyword);
          break;
  }

}