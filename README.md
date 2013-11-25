Perlin Map Generator
==
This program is designed to randomly generate maps using Perlin noise. It creates a heightmap, then uses a series of thresholds to designate areas. The image is then saved as a .png in the current directory.

Requirements
--
To use the program you must have Python 2.x and [Python Imaging Library](www.pythonware.com/products/pil). For linux you can get the library with
```
  sudo apt-get install python-imaging
```
Otherwise, go to the above link and download an installer.

Usage
--
The simplest use is to just run the script.

```
  python main.py
```
  
You can also use tags to customize the map. For instance:

```
  python main.py -x -w 512 -h 128
```
This will create a map that wraps around the x axis, has a height of 128 pixels and a width of 512.

Full list of tags:
--
-x Wraps around the X axis  
-y Wraps around the Y axis  
-w [pixels] Sets the width of the image to a specified number of pixels  
-h [pixels] Sets the height of the image to a specified number of pixels  
-s [seed] Specifies a seed for the noise generator  
-f [name] Saves the image as the specified file name (Do not include extesion)
