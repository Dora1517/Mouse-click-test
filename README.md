# Mouse-click-test
This Python program is a **mouse click counter** with an integrated **stopwatch**, designed to measure your click speed. It uses the **`tkinter`** libraries for the graphical user interface and **`pynput`** for precise mouse click recording.

The core of the program is a threaded process running in the background that records each click. A stopwatch starts with the first click, and a counter increments with each subsequent mouse click. The program stops counting at exactly **100 clicks**, stops timing, and saves the required time in an internal **leaderboard**. This leaderboard is automatically sorted to display the best times.

In addition to the core functionality, the application offers a **"Reset"** button to start a new measurement, as well as a **"Save Ranking"** function. The latter allows you to export the entire ranking as a `.txt` file, ideal for comparing or sharing your best times. The program is therefore a useful tool for testing and continuously improving your own click speed.
