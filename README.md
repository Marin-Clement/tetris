
<h1>Tetris Game</h1>
<p>This is a classic game of Tetris where the player tries to clear lines by arranging falling Tetriminos.</p>
<h2>How to Play</h2>
<ol>
  <li>Use the left/right arrow keys to move the falling Tetromino</li>
  <li>Use the up arrow key to rotate the Tetromino</li>
  <li>Use the down arrow key to speed up the falling of the Tetromino</li>
  <li>The game is over when a new Tetromino cannot fit into the game field at the start position</li>
</ol>
<h2>Implementation Details</h2>
<p>The game is built using the Pygame library and uses the font module of Pygame to display the text. The game consists of a <code>Tetris</code> class, which is the main game class and a <code>Text</code> class that displays the text on the screen. The <code>Tetromino</code> class implements the functionality of the falling blocks and the <code>Field</code> class manages the game field. The game's speed increases when the player presses the down arrow key. The game keeps track of the score and the number of full lines that the player has cleared. The game restarts when the player loses.</p>