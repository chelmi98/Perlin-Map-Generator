Perlin Map Generator
==
This program is designed to randomly generate maps using Perlin noise. It creates a heightmap, then uses a series of thresholds to designate areas. The image is then saved as a .png in the current directory.

##Usage
###Requirements
To run the script you must have Python 2.x and [PIL (Python Imaging Library)](www.pythonware.com/products/pil). For linux you can get PIL with

```
sudo apt-get install python-imaging
```
For mac you need to install Homebrew first.

```
ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go/install)"
```
Then you can run the following to install PIL.

```
brew install python-imaging
```
Otherwise, go to the above link and download an installer.

###Downloading
Once you have all of the requirements installed, click [here](https://github.com/chelmi98/Perlin-Map-Generator/archive/master.zip) to download the project. Unzip it, then navigate to the script in the terminal.

###Running
The simplest use is to just run the script.

```
python main.py
```
You can also use tags to customize the map. For instance:

```
python main.py -x -w 512 -h 128
```
This will create a map that wraps around the x axis, has a height of 128 pixels and a width of 512.

###Full list of tags
-x Wraps the terrain around the X axis  
-y Wraps the terrain around the Y axis  
-w [width] Sets the width of the image to specified number of pixels  
-h [height] Sets the height of the image to specified number of pixels  
-s [seed] Specifies a seed for the noise generator  
-f [name] Saves the image as the specified file name
