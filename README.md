# Hangman_game

### Enviroment, framework and Libraries:

Pipenv, Flask, RandomWords, Random, it will be updated in the process.

### Datase SQLite:

Table User and Games History.
Table User: ID, Name, Surname, Email
Tabla Games History: ID, Game number, Made guesses, Status, Word.
Relationship: Many to Many.

### Word generation:

Word will be generate randomly from RandomWords lib and put to a list, from that list word will be selected with Random lib and submited to database.
In word database there will three types of words list: Junior, Adult, Old Like Dust.
Junior level: 5 letter words.
Adult level: 7 letter words.
Old like Dust: 9 letter words.

# Plan for Hangman game, it will be updated in the process.

1. Setup Environment and Install Dependencies:

Create a new directory for your project and set up a virtual environment.
Install the required packages, such as Flask and SQLite.

2. Database Setup:

Create a SQLite database to store the necessary data for the game, such as words, guesses, and scores.
Design the tables needed for your game, such as a table to store words and a table to store scores.

3. Create Flask Application:

Set up a Flask application with a basic structure (app.py).
Configure the database connection in your Flask app.

4. Create the Frontend:

Create HTML templates for the game interface using Flask's template rendering engine (Jinja2).
Design a form for users to input their guesses.
Display the hangman graphics using ASCII art or images for different stages of the game.

5. Implement Game Logic:

Create Python functions to handle game logic, such as generating a random word, checking if a guess is correct, updating the hangman state, and determining the game outcome (win or lose).
Implement functions to retrieve data from the database, such as getting random words for the game.

6. Route Functions:

Define Flask route functions to handle different parts of the game, such as starting a new game, processing user guesses, and displaying the game result.
Integrate the game logic functions within these route functions.

7. User Interface:

In the Flask route functions, render the appropriate templates and pass necessary data to the frontend (HTML templates).
Show the game status, hidden word, number of attempts, and hangman visuals.

8. Game State Handling:

Store the game state (current word, guessed letters, number of attempts, etc.) in the database, associating it with a session or user ID.
Update the database as the game progresses (new attempts, guessed letters, etc.).

9. Finish Game Logic:

Add logic for handling game termination conditions, such as a maximum number of incorrect guesses or revealing the correct word after a certain number of attempts.

10. Implement Score Tracking:

Create functions to keep track of scores, such as wins and losses, and store them in the database.
Update scores after each completed game.