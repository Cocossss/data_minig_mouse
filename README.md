# data_minig_mouse
needed preinstalled packages: PyQt5, pynput, pyautogui

# Usage (tested only for linux)
After running the script with command 'python3 ./data_minig_mouse.py', a window appears in which there are a start button and a stop button:

* start button starts tracking the mouse: if left mouse button is clicked, then script saves coordinates of the mouse in file 'mpc_centers.csv', if right mouse button is clicked, then script saves screenshot of entire screen in the 'screenshots' directory;
* stop button stops tracking the mouse.

If file 'mpc_centers.csv' and directory 'screenshots' exist, then their contets will be rewritten.
