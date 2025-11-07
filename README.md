# Blender-Face-ShapeKeys
Simple Script using MediaPipe library and camera to create shapekey data for a blender mesh, and then translate those points to a fully generated face mesh. 

<img width="568" height="663" alt="image" src="https://github.com/user-attachments/assets/d5bdde73-6994-464b-ad8b-8f40b8851677" />

## **How to to use**
Open ShapeKeys.py, and go into the script. In line 20, change the number inside <code> cap = cv2.VideoCapture(1) </code> to your camera slot. (If you only have one camera on your computer, it should be 0.
While you are in here, change the parameters at the begining of the script to suit your needs. 

## Process framedata in Blender
Open blender, go to the scripting tab, and add new script. 
Paste the ReplaceShapeKeys.py into the script, update the filepath to your needs. Run the script. 

Enjoy!
