# MicropythonLife
An implementation of Conway's Game of Life on the Raspberry Pi Pico.

This is pure Micropython, and displays to a common OLED screen hooked up via I2C. It keeps an array which indicates which cells are currently active, which dramatically improves the speed. A list of active cells would take up too much memory. Also, it keeps a copy of the board as it goes, at progressively longer intervals. This lets it detect when a loop has occurred so as to reset itself.

At some point in the future I would like to get the life step action (which takes most of the processing time, and is the current bottleneck) redone in compiled C code. I have made a stab at it, but I am sure there are bugs there and I have not figured out the C/micropython interface yet. When that is done this could be a useful building block for more involved projects.