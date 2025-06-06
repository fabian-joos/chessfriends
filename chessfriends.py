"""

Copyright (C) 2025 Fabian Joos

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

ChessFriends is a Python project that enables the 
creation and administration of a chess tournament. 
It includes classes to represent players, matches, and tournaments,
and provides functionality for managing players, generating match pairings 
with additional time handicaps, and calculating scores.

Modules:
--------
MatchResults: Enum class to represent the possible results of a chess match.
CfPlayer: Represents a chess player with attributes for first name, last name, and rating.
CfTournament: Manages a chess tournament, including players, match pairings, and scores.
CfMatch: Represents a chess match between two players, including the result and time limits.

For usage demo see the demo.py file
"""


from enum import Enum
from datetime import datetime


class MatchResult(Enum):
    """
    Enum class to represent the possible results of a chess match.
    """
    ONGOING = 0
    WHITE_WINS = 1
    BLACK_WINS = 2
    DRAW = 3

    def __str__(self):
        return self.name



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
        """
        Returns the rating of the player.
        """
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
        evaluate_match(match): Evaluates the result of a match
        and returns the scores for the players.
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
            self.matchdays[matchday].append(CfMatch(
                [fixed_player, rotating_players[matchday]],
                self))
            if matchday % 2 != 0:
                self.matchdays[matchday][0].swap_opponents()

            for i in range(1, (number_of_players // 2)):
                self.matchdays[matchday].append(
                    CfMatch([rotating_players[number_of_players - i - 1 + matchday],
                             rotating_players[matchday + i]],
                             self))
                if i % 2 == 0:
                    self.matchdays[matchday][i].swap_opponents()
        self.reset_scoreboard()

    def match_schedule(self):
        """
        Prints the schedule of matches for each matchday.
        This method iterates through the list of matchdays and prints the details
        of each match, including the match number, result, opponents' names, 
        ratings, and time limits.
        """
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
        """
        Resets the scoreboard for all players.
        This method initializes the scoreboard dictionary for each player in the 
        self.players list. Each player's scoreboard will have their games and 
        score set to 0.
        """
        self.scoreboard = {}
        for player in self.players:
            self.scoreboard[player] = {}
            self.scoreboard[player]["games"] = 0
            self.scoreboard[player]["score"] = 0

    def evaluate_scoreboard(self):
        """
        Evaluates the scoreboard by resetting it and then evaluating all matches.
        This method first resets the scoreboard to its initial state. 
        It then iterates through each matchday and evaluates each match within the matchday
        to update the scoreboard inplace.
        """

        self.reset_scoreboard()
        for matchday in self.matchdays:
            for match in matchday:
                self.evaluate_match(match)

    def print_stats(self):
        """
        Prints the statistics of each player in the scoreboard.
        The statistics include the player's name, score, and the number of games played.
        """
        for player, stats in self.scoreboard.items():
            print(f"{player.name}: "
                f"{stats['score']} "
                f"({stats['games']})")

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

        if match.result == MatchResult.ONGOING:
            return opponents, scores
        if match.result == MatchResult.WHITE_WINS:
            scores[0] = self.score_win
        elif match.result == MatchResult.BLACK_WINS:
            scores[1] = self.score_win
        elif match.result == MatchResult.DRAW:
            scores[0] = self.score_draw
            scores[1] = self.score_draw
        for i, player in enumerate(opponents):
            self.scoreboard[player]["games"] += 1
            self.scoreboard[player]["score"] += scores[i]
        return opponents, scores



class CfMatch:
    """
    Represents a chess match between two players in a tournament.
    Attributes:
        opponents (list): A list containing two CfPlayer objects.
                          The first object in the list represents the White player.
                          Use swap_opponents to change order of list.
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
    def __init__(self, opponents: list[CfPlayer], tournament: CfTournament):
        self.opponents = opponents
        self.tournament = tournament
        self.result = MatchResult.ONGOING
        self.time_limits = [60, 60]
        self.assign_handicap()

    def swap_opponents(self):
        """
        Swap the positions of the two opponents and their corresponding time limits.
        This method exchanges the first and second elements in the `opponents` list
        and the `time_limits` list, effectively swapping the opponents and their
        associated time limits.
        """
        opponent_temp = self.opponents[0]
        self.opponents[0] = self.opponents[1]
        self.opponents[1] = opponent_temp

        time_limit_temp = self.time_limits[0]
        self.time_limits[0] = self.time_limits[1]
        self.time_limits[1] = time_limit_temp

    def assign_handicap(self):
        """
        Assigns a time handicap based on the rating difference between two opponents.
        The time handicap is calculated as 2.5% of the rating difference. 
        The opponent with higher rating gets their time limit decreased by this handicap.
        """
        rating_diff = self.opponents[0].rating - self.opponents[1].rating
        time_handicap = int(rating_diff * 0.025)
        if rating_diff >= 0:
            self.time_limits[0] -= time_handicap
        else:
            self.time_limits[1] += time_handicap # add time handicap because it has a negative value

    def _set_result(self, result):
        if not isinstance(result, MatchResult):
            raise ValueError("Invalid result type: 'result' must be an instance of MatchResult.")
        self.result = result
        print(f"Match result set to: {self.result}")

    def white_wins(self):
        """
        Sets the result of the game to indicate that White has won.
        This method updates the `result` attribute of the game instance to 1,
        signifying that the White player is the winner.
        """
        self._set_result(MatchResult.WHITE_WINS)

    def black_wins(self):
        """
        Sets the result of the game to indicate that Black has won.
        This method updates the `result` attribute of the game instance to 2,
        signifying that the Black player is the winner.
        """
        self._set_result(MatchResult.BLACK_WINS)

    def draw(self):
        """
        Sets the result of the game to indicate a draw.
        This method updates the `result` attribute of the game instance to 3,
        signifying that the game ended in a draw.
        """
        self._set_result(MatchResult.DRAW)
