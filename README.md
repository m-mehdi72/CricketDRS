# CricketDRS
This project mimcs the DRS System used in Cricket to review and check whether it was an out, or not, or no-ball. Or any other thing. First the Third Umpire is given Option to Choose what he wants to check then, accordingly, a window opens with options related....

The APK folder contains the main App made using tkinter.
The ball_tracking, preprosessing, and script were made for early development for testing before final Implementation.
The Test Videos folder contains Videos you can use for testing of app. You can find further online. 
The Test Images folder was used for application of preprocessing on before first before applying on videos.

# APK Folder
The APK folder consists of three python files. main.py is the main window which leads to further options. The other Images in this folder are for Tkinter/s Frontend. 

# Working
Run the main.py window. You will have some options. Select what you want to check. Then, Select the video. Once done, You will move to second window. There will bw options to move video forwards and backwards at various speeds. Once the Umpire has decided his decision. He will press Give OUT/Give NOT OUT. A window with decision pending with bit delay will appear. A small animation will play and then the decision will be displayed. 

# For LBW
If the Umpire selects LBW, There is another option to track the trajectory to verify where the ball is going. Then, Umpire can move frames forwards and backwards at various speeds and then give his decision
