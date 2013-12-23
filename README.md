Perlin Map Generator
==
This program is designed to randomly generate maps using Perlin noise. It creates a height map, then uses a series of thresholds to designate areas. It then saves it as an image file in the current directory.

Usage
-----
###Requirements
To run the script you must have Python 2.x and PIL (Python Imaging Library).

####Linux
To install PIL on Linux, just use
```
sudo apt-get install python-imaging
```

####Mac
For mac you need to install Homebrew first.
```
ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go/install)"
```
Then you can run the following to install PIL.
```
brew install python-imaging
```

####Windows
For Windows, if you have pip, just use
```
pip install PIL
```
Otherwise, go to http://www.pythonware.com/products/pil/ and download an installer.

###Downloading
Once you have all of the requirements installed, go to https://github.com/chelmi98/Perlin-Map-Generator/archive/master.zip to download the project. Unzip it, then open the directory in the terminal. Alternately, if you have git just use
```
git clone https://github.com/chelmi98/Perlin-Map-Generator.git
```

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
`-x` Wraps the terrain around the X axis  
`-y` Wraps the terrain around the Y axis  
`-r` Enabels raw height output
`-w [width]` Sets the width of the image to specified number of pixels  
`-h [height]` Sets the height of the image to specified number of pixels  
`-s [seed]` Specifies a seed for the noise generator  
`-n [name]` Saves the image as the specified file name  
`-c [name]` Uses options found in specified JSON file located in `/templates`
