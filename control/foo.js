
function main(){

  process.stdout.write("Here we go!");

  var arDrone = require('ar-drone');
  var client = arDrone.createClient();

//  client.takeoff();

  client

//    .after(5000, function() {this.clockwise(1);})
    .after(5000, function() {saveAnImage(client);})
//    .after(3000, function() {this.animate('flipLeft', 15);})
//    .after(5000, function() {this.stop();this.land();});

    return 0;

  }

function saveAnImage(client){

    //var arDrone = require('ar-drone');
    //var client = arDrone.createClient();
    var fs = require('fs');

    var pngStream = client.getPngStream();
    var frameCounter = 0;
    var saveDir = './img'; // Image Dir

    console.log('Inside PNGStream');

    pngStream
      .on('error', console.log)
      .on('data', function(pngBuffer) {
        // Exit after first image saved
        if(frameCounter!=0){
           console.log('Exiting PNGStream');
           process.exit();
         }

        // Create ImageName and save to dir
        var imageName = saveDir + '/savePNG' + '.png';
        fs.writeFile(imageName, pngBuffer, function(err) {
          if (err) {
            console.log('Error saving PNG: ' + err);
          }
        });
        console.log(imageName); // Output imagePath for use in parent

        frameCounter++;
      });
      console.log('Leaving PNGSTREAM');
    }


main();
