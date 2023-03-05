# Piou-Piou

Hey there !

This repo is a submission to the CECI-BEST's hackathon.

## The theme

This year, the theme was "Game Jam", pretty cool uh ;-). 

As you might know, some constraint were there too, we had to build a game that is not controlled by the computer the game is running on !
And the game style had to be related to Arcade Games

## Our submission

We decided to build a Space Shooter controlled by phone, by using accelerometer to control space-ship and take the lead in the universe !

## How to run it ?

### A little confession

This project might be the hardest to run, not because of our incapacity (i hope), but because we choose to use [accelerometer js api](https://developer.mozilla.org/en-US/docs/Web/API/Accelerometer) 
but we figure out too late that it only works on HTTPS, or in pure localhost.

We found a solution, of course, but it requires you to be on Android and to use Google Chrome.

### The web part

To build the web part, just do 

    npm install
    npm run build

and serve `dist` folder the way you want ;-)

### The python part, the easiest

To run python part, just do 
    
    python -m pip install -r requirements.txt
    python main.py

### The usage of the web application

This is the tricky part, if you're running this project on your LAN, you will have to do a quick manipulation.

1. Go to `chrome://flags` in your android browser
2. Search for "Insecure origins treated as secure" 
3. Put the web address (with http:// prefix) into the box, enable the flag, and then click on "Relaunch" to apply changes.

After this manipulation, chrome will consider your web app as it was on a super secure HTTPS server lol, so naïve :)

Then, just go on the web app, enter the IP Address of the server/computer were the game is running, and enjoy

### The gameplay

This is pretty straightforward, you can control your spaceship with your phone orientation, and you can click on the screen to shoot evil ennemies!

There are some "power up" that allows you to get more lasers, or to gain some score if you can catch them quickly !


### Technical Choices

We choose to use pygame because it was the easiest way to get into gamedev for a first time, and a web app for the phone because it was more easy than a native application.

The web app use preact, just because its a pleasure to use !

Anyway, if you have read this README this far, congratulations, you are braver than the half of my team lol.

