# ChessFriends

ChessFriends is a Python project that enables the creation and administration of a chess tournament. It includes classes to represent players, matches, and tournaments, and provides functionality for managing players, generating match pairings with additional time handicaps, and calculating scores.

## Features

- **Player Management**: Add players with attributes such as name and rating.
- **Tournament Management**: Create tournaments with start and end dates.
- **Round-Robin Pairing**: Automatically generate match pairings for a round-robin tournament.
- **Time Handicaps**: Assign time handicaps based on player ratings.
- **Score Calculation**: Evaluate match results and update player scores.
- **Match Schedule**: View the schedule of matches for each matchday of the tournament.

## Installation

1. Clone the repository.
2. Ensure you have Python 3.11 or later installed.
3. Run the `demo.py` file to see the functionality in action.

## Usage

### Main Classes

- **`CfPlayer`**: Represents a chess player with attributes for first name, last name, and rating.
- **`CfTournament`**: Manages a chess tournament, including players, match pairings, and scores.
- **`CfMatch`**: Represents a chess match between two players, including the result and time limits.

### Example

Running the `demo.py` file initializes a chess tournament and demonstrates two methods for adding players to the tournament. It then generates all match pairings using the round-robin pairing system.
As an example, results for four matches are recorded. Finally, the program evaluates the scores, displays the statistics for each player (score-points and number of evaluated matches), and prints the complete current match schedule.


John Apple: 0 (1)  
Jane Flowers: 3 (1)  
Michael Hunter: 0 (1)  
Emily Smith: 1 (1)  
David Porter: 0 (1)  
Sarah Waters: 3 (1)  
Robert Peters: 1 (1)  
Laura Howard: 3 (1)  

--------------------------- Matchday 1 ---------------------------  
Game 1: (BLACK_WINS) John Apple (1450, 60 min.) vs. Jane Flowers (1750, 53 min.)  
Game 2: (WHITE_WINS) Laura Howard (1400, 55 min.) vs. Michael Hunter (1200, 60 min.)  
Game 3: (DRAW) Emily Smith (1600, 59 min.) vs. Robert Peters (1550, 60 min.)  
Game 4: (WHITE_WINS) Sarah Waters (1900, 45 min.) vs. David Porter (1300, 60 min.)  

--------------------------- Matchday 2 ---------------------------  
Game 1: (ONGOING) Michael Hunter (1200, 60 min.) vs. John Apple (1450, 54 min.)  
Game 2: (ONGOING) Jane Flowers (1750, 57 min.) vs. Emily Smith (1600, 60 min.)  
Game 3: (ONGOING) David Porter (1300, 60 min.) vs. Laura Howard (1400, 58 min.)  
Game 4: (ONGOING) Robert Peters (1550, 60 min.) vs. Sarah Waters (1900, 52 min.)  

--------------------------- Matchday 3 ---------------------------  
Game 1: (ONGOING) John Apple (1450, 60 min.) vs. Emily Smith (1600, 57 min.)  
Game 2: (ONGOING) Michael Hunter (1200, 60 min.) vs. David Porter (1300, 58 min.)  
Game 3: (ONGOING) Sarah Waters (1900, 57 min.) vs. Jane Flowers (1750, 60 min.)  
Game 4: (ONGOING) Laura Howard (1400, 60 min.) vs. Robert Peters (1550, 57 min.)  

--------------------------- Matchday 4 ---------------------------  
Game 1: (ONGOING) David Porter (1300, 60 min.) vs. John Apple (1450, 57 min.)  
Game 2: (ONGOING) Emily Smith (1600, 60 min.) vs. Sarah Waters (1900, 53 min.)  
Game 3: (ONGOING) Robert Peters (1550, 52 min.) vs. Michael Hunter (1200, 60 min.)  
Game 4: (ONGOING) Jane Flowers (1750, 52 min.) vs. Laura Howard (1400, 60 min.)  

--------------------------- Matchday 5 ---------------------------  
Game 1: (ONGOING) John Apple (1450, 60 min.) vs. Sarah Waters (1900, 49 min.)  
Game 2: (ONGOING) David Porter (1300, 60 min.) vs. Robert Peters (1550, 54 min.)  
Game 3: (ONGOING) Laura Howard (1400, 60 min.) vs. Emily Smith (1600, 55 min.)  
Game 4: (ONGOING) Michael Hunter (1200, 60 min.) vs. Jane Flowers (1750, 47 min.)  

--------------------------- Matchday 6 ---------------------------  
Game 1: (ONGOING) Robert Peters (1550, 58 min.) vs. John Apple (1450, 60 min.)  
Game 2: (ONGOING) Sarah Waters (1900, 48 min.) vs. Laura Howard (1400, 60 min.)  
Game 3: (ONGOING) Jane Flowers (1750, 49 min.) vs. David Porter (1300, 60 min.)  
Game 4: (ONGOING) Emily Smith (1600, 50 min.) vs. Michael Hunter (1200, 60 min.)  

--------------------------- Matchday 7 ---------------------------  
Game 1: (ONGOING) John Apple (1450, 59 min.) vs. Laura Howard (1400, 60 min.)  
Game 2: (ONGOING) Robert Peters (1550, 60 min.) vs. Jane Flowers (1750, 55 min.)  
Game 3: (ONGOING) Michael Hunter (1200, 60 min.) vs. Sarah Waters (1900, 43 min.)  
Game 4: (ONGOING) David Porter (1300, 60 min.) vs. Emily Smith (1600, 53 min.)  