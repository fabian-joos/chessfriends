from datetime import datetime


"""
ChessFriends is a Python project that enables the creation and administration of a chess tournament. 
It includes classes to represent players, matches, and tournaments, and provides functionality for managing players, generating match pairings with additional time handicaps, and calculating scores.

Modules:
--------
CfPlayer: Represents a chess player with attributes for first name, last name, and rating.
CfTournament: Manages a chess tournament, including players, match pairings, and scores.
CfMatch: Represents a chess match between two players, including the result and time limits.

Usage:
------
1. Create CfPlayer objects for each player.
2. Add players to a CfTournament object.
3. Use CfTournament methods to manage the tournament, generate pairings, and calculate scores.

Example:
--------
player1 = CfPlayer("John", "Doe", 1500)
player2 = CfPlayer("Jane", "Smith", 1600)
tournament = CfTournament()
tournament.players = [CfPlayer("0", "Fleur", 1340),
                      CfPlayer("1", "Tim", 1800),
                      CfPlayer("2", "Walt", 1000),
                      CfPlayer("3", "Louis", 1500),
                      CfPlayer("4", "Terry", 1600),
                      CfPlayer("5", "Alex", 2000),
                      CfPlayer("6", "Fred", 1540),
                      CfPlayer("7", "Lisa", 1400)]
tournament.round_robin_pairing()
"""


class CfPlayer:
    """
    A class to represent a chess player.

    Attributes:
    ----------
    first_name : str
        The first name of the player.
    last_name : str
        The last name of the player.
    rating : int
        The rating of the player.

    Methods:
    -------
    __init__(self, first_name: str, last_name: str, rating: int):
        Constructs all the necessary attributes for the player object.
    """
    def __init__(self, first_name: str, last_name: str, rating: int = 1000):
        self.first_name = first_name
        self.last_name = last_name
        self._rating = None
        self.rating = rating

    @property
    def name(self):
        """
        Returns the full name of the person by combining the first name and last name.
        """
        return f"{self.first_name} {self.last_name}"

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        if rating < 0:
            raise ValueError("Rating can not be negative")
        self._rating = rating


class CfTournament:
    """
    CfTournament is a class that represents a chess tournament.
    It includes methods for managing players, generating match pairings, and calculating scores.

    Attributes:
        start_date (datetime): The start date of the tournament.
        end_date (datetime): The end date of the tournament.
        players (list): A list of players participating in the tournament.
        matchdays (list): A list to store the pairings for each round.
        score_win (int): The score awarded for a win.
        score_draw (int): The score awarded for a draw.
        scoreboard (dict): A dictionary to store the scores of the players.

    Methods:
        __init__(): Initializes the tournament with default values.
        add_players(): Adds one or more players to the players list.
        round_robin_pairing(): Generates a round-robin pairing for the players in the tournament.
        match_schedule(): Prints the complete match schedule.
        reset_scoreboard(): Resets the scoreboard for all players.
        evaluate_match(match): Evaluates the result of a match and returns the scores for the players.
    """
    def __init__(self, start_date: datetime, end_date: datetime):
        if not isinstance(start_date, datetime):
            raise TypeError("start_date must be of type datetime")
        if not isinstance(end_date, datetime):
            raise TypeError("end_date must be of type datetime")

        self.start_date = start_date
        self.end_date = end_date
        self.players = []
        self.matchdays = []
        self.score_win = 3
        self.score_draw = 1
        self.scoreboard = {}

    def add_players(self, *args):
        """
        Adds one or more players to the players list.
        Parameters:
        *args: Variable length argument list. Each argument can be a CfPlayer object 
               or a list of CfPlayer objects.
        Raises:
        TypeError: If any argument is not a CfPlayer object or a list of CfPlayer objects,
                   or if any element in a list argument is not a CfPlayer object.
        """

        for arg in args:
            if isinstance(arg, list):
                for player in arg:
                    if isinstance(player, CfPlayer):
                        self.players.append(player)
                    else:
                        raise TypeError("All elements in the list must be CfPlayer objects")
            elif isinstance(arg, CfPlayer):
                self.players.append(arg)
            else:
                raise TypeError("Arguments must be CfPlayer objects or lists of CfPlayer objects")


    def round_robin_pairing(self):
        """
        Generates a round-robin pairing for the players in the tournament.
        This method creates pairings for each round of the tournament using the 
        round-robin algorithm. Each player plays against every other player exactly once.
        The first player in the list is fixed, and the remaining players are rotated 
        to generate the pairings for each round. If the round number is odd, the opponents 
        of the first match are swapped. Similarly, if the index of the match in the round 
        is even, the opponents of that match are swapped.
        The generated pairings are stored in the `self.matchdays` list.
        Attributes:
            self.players (list): List of players participating in the tournament.
            self.matchdays (list): List to store the pairings for each round.
        """

        number_of_players = len(self.players)
        fixed_player = self.players[0]
        rotating_players = self.players[1:number_of_players]
        rotating_players.extend(rotating_players) # prepare array for rotation

        for matchday in range(0, number_of_players-1):
            self.matchdays.append([])
            self.matchdays[matchday].append(CfMatch(fixed_player,
                                              rotating_players[matchday],
                                              self))
            if matchday % 2 != 0: self.matchdays[matchday][0].swap_opponents()

            for i in range(1, (number_of_players // 2)):
                self.matchdays[matchday].append(
                    CfMatch(rotating_players[number_of_players - i - 1 + matchday],
                            rotating_players[matchday + i],
                            self))
                if i % 2 == 0: self.matchdays[matchday][i].swap_opponents()
        self.reset_scoreboard()

    def match_schedule(self):
        for i, matchday in enumerate(self.matchdays):
            print(f"--------------------------- Matchday {i+1} ---------------------------")
            for j, match in enumerate(matchday):
                print(f"Game {j+1}: ({match.result}) "
                    f"{match.opponents[0].name} "
                    f"({match.opponents[0].rating}, {match.time_limits[0]} min.)"
                    f" vs. "
                    f"{match.opponents[1].name} "
                    f"({match.opponents[1].rating}, {match.time_limits[1]} min.)")
            print("\t")
        print("\n")

    def reset_scoreboard(self):
        for player in self.players:
            self.scoreboard[player] = {}
            self.scoreboard[player]["games"] = 0
            self.scoreboard[player]["score"] = 0

    def evaluate_match(self, match):
        """
        Evaluate the result of a chess match and assign bonus scores to the players.
        Args:
            match (CfMatch): An object representing the match, which has a 'result' attribute.
                             The 'result' attribute should be:
                             - 1 if White wins the match
                             - 2 if Black wins the match
                             - 3 if the match ends in a draw
        Returns:
            scores:    A list containing two integers. 
                       The first integer is the bonus score for the White player,
                       and the second integer is the bonus score for the Black player.
            opponents: A list containing the two CfPlayer objects.
                       The first object is the White player,
                       the second object is the Black player.
        """
        opponents = [player for player in match.opponents]
        scores = [0,0]
        if match.result == 1:             # White wins the match
            scores[0] = self.score_win    # White player gets winning bonus score
        elif match.result == 2:           # Black wins the match
            scores[1] = self.score_win    # Black player gets winning bonus score
        elif match.result == 3:           # Match end in a draw
            scores[0] = self.score_draw   # Both players get draw bonus score
            scores[1] = self.score_draw   #
        for i, player in enumerate(opponents):
            self.scoreboard[player]["games"] += 1
            self.scoreboard[player]["score"] += scores[i]
        return opponents, scores



class CfMatch:
    """
    Represents a chess match between two players in a tournament.
    Attributes:
        opponents (list): A list containing two CfPlayer objects, 
                          representing the white and black players.
        tournament (CfTournament): The tournament in which the match is taking place.
        result (int): The result of the match
                      (0 for ongoing, 1 for white wins, 2 for black wins, 3 for draw).
        time_limits (list): A list containing the time limits for the white and black players.
    Methods:
        __init__(player_white: CfPlayer, player_black: CfPlayer, tournament: CfTournament):
            Initializes a CfMatch object with the given players and tournament.
        swap_opponents():
            Swaps the opponents and their respective time limits.
        assign_handicap():
            Assigns a time handicap based on the rating difference between the players.
        white_wins():
            Sets the result of the match to indicate that the white player has won.
        black_wins():
            Sets the result of the match to indicate that the black player has won.
        draw():
            Sets the result of the match to indicate a draw.
    """
    
    def __init__(self, player_white: CfPlayer, player_black: CfPlayer, tournament: CfTournament):
        self.opponents = [player_white, player_black]
        self.tournament = tournament
        self.result = 0
        self.time_limits = [60, 60]
        self.assign_handicap()

    def swap_opponents(self):
        opponent_temp = self.opponents[0]
        self.opponents[0] = self.opponents[1]
        self.opponents[1] = opponent_temp

        time_limit_temp = self.time_limits[0]
        self.time_limits[0] = self.time_limits[1]
        self.time_limits[1] = time_limit_temp

    def assign_handicap(self):
        rating_diff = self.opponents[0].rating - self.opponents[1].rating
        time_handicap = int(rating_diff * 0.025)
        if rating_diff >= 0:
            self.time_limits[0] -= time_handicap
        else:
            self.time_limits[1] += time_handicap # add time handicap because it has a negative value

    def white_wins(self):
        self.result = 1

    def black_wins(self):
        self.result = 2

    def draw(self):
        self.result = 3
