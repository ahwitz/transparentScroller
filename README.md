animatedScroller.sh / scroller README:

To use:

from anywhere on the machine, enter: “scroller -s SPEED -o OUTPUT -i input1 (input2 input3…)”

where:

SPEED = an integer number of images to render per second in the movie. 45 is preferred but it can be changed.

OUTPUT = a file name WITHOUT EXTENSION relative to where you are for the output file. The script will automatically append “.mov” to whatever name you give it.

input1/2/3 = either one PDF with multiple pages (not implemented yet) or a series of PNG files to use as input. They will be stacked vertically in the order they are declared in this script.


Thus:

If /Users/vp2 looks like:

-test1.png
-test2.png
-test3.png

…and the command “scroller -s 35 -o testMovie -i test1.png test2.png test3.png” is run, /Users/vp2 will look like:

-testMovie.mov
-test1.png
-test2.png
-test3.png

…after a while. This script takes a LONG time to run and will update you on where in image rendering (every ten images)/video compiling(every .5 seconds) it is throughout.