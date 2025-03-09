# TIC-TAC-TOE GAME
## An old-skool like tic-tac-toe game (with Multiplayer or Single Player)

This is Tic-Tac-Toe game I developed as a free time project purely using python. 
In this game the user can play his/her school-time favourite tick-cross or X's and O's or Tic-tac-toe game with his/her friends or against a computer.

<b>Here I just implemented frontend I learnt recently to my earlier CLI based game Tic-Tac-Toe<b>

<hr>

<h3>Tech Stack Used</h3>
<ul>
<li>Python</li>
<li>Javascript(very basic) through pyscript</li>
<li>CSS</li>
</ul>


<h3>Run the Project</h3>
Just run in the terminal at the project directory:<br>

  ````
python3 -m http.server 8000
  ````
This will run the project at http://localhost:8000

Enjoy playing  :joystick: (and ofcourse sorry losing to AI :upside_down_face: )

### Multi-Player Mode

In this mode a user can play against his/her friend for a timepass or enjoyment or just as a stress-buster. In this mode there is no algorithm so the person who plays most optimally and tactically wins the game. If both players play optimally then it leads to  a draw.

### Single-Player Mode

In this mode the player plays against the computer(also referred to as <b>AI</b> at some sites reffering to this game. In this mode the computer's playing technique is designed using an algorithm in such a way that Computer never loses. The only results of the game are either the computer wins or there is a draw.
The Algorithm used here is MinMax Algorithm also used in Computer vs. Human Chess Games. In this algorithm we can have only three options for computer/user based on symbol chosen. If computer choses symbol with number as 1 then it has following options:
Options       | Number associated
------------- | -----------------
Win           |  1
Draw          |  0
Lose          | -1

So we can use this rule table to design our Algo. If we give give the computer's symbol as 1 then we need to maximise score so that computer wins. Simultaneosly for user to win it wants to minimise score.
Similarly if computer choses symbol with number as -1 then it has following options:
Options       | Number associated
------------- | -----------------
Win           | -1
Draw          |  0
Lose          |  1

So in this case computer wants to minimise score in order to win. Simultaneosly user wants to maximise score in order to win.

So this MinMax algorithm in achieved using recursion which creates a structure looking like a tree where starting from leaf node we want to move score in such a MinMax way that reaching root we get MinMax accordingly as per the symbol chosen for computer.

So now as we got to know user cannot win :sweat_smile: , to make the child within him happy:smiley: by giving him the freedom to chose:
* To chose the symbol :negative_squared_cross_mark: or :o: for his/her whole game
* Whether he wants to start the game as 1st move or wnats the 2nd move by allowing Computer to start the game
