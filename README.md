We hijacked a connected Parrot drone (model AR 2.0) and make him follow a target : a red circle held by hands.
The script allows the malicious user to look for drone wifi networks, deauthenticate the owner, and then connect to the drone to get the video stream.
Then the script uses OpenCV with the DetectBlob method to find the target in the video stream and give instructions in real time to make the drone follow it.

Install dependencies:

Node-ar-drone 
```bash
npm install git://github.com/felixge/node-ar-drone.git
```
OpenCV for Python
```bash
pip install opencv-python
```




