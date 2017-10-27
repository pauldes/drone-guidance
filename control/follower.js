function takePicture(){
  process.stdout.write("Taking a pic")
};

function findTarget(){
  process.stdout.write("Finding the target")
  var vector = [1,20]
  var radius = 5
  return vector.push(radius)
};

function follow(epsilon_x,epsilon_y,duration=120){

  process.stdout.write("Follower mode starting");
  /*
  var arDrone = require('ar-drone');
  var client = arDrone.createClient();
  */
  i=0;
  while(i<duration){
    i++;
    takePicture();
    var vector_and_radius = findTarget()
    var vector_x = vector_and_radius[0]
    var vector_y = vector_and_radius[1]
    var diameter = vector_and_radius[2]

  }
}

follow(50,50);
