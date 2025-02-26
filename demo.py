from datetime import datetime
from chessfriends import CfTournament, CfPlayer


start_date = datetime(2025,9,1)
end_date = datetime(2025,5,30)

vp = CfTournament(start_date, end_date)

vp.players = [CfPlayer("John", "Apple", 1450),
              CfPlayer("Jane", "Flowers", 1750),
              CfPlayer("Michael", "Hunter", 1200),
              CfPlayer("Emily", "Smith", 1600),
              CfPlayer("David", "Porter", 1300),
              CfPlayer("Sarah", "Waters", 1900),
              CfPlayer("Robert", "Peters", 1550),
              CfPlayer("Laura", "Howard", 1400)]

vp.round_robin_pairing()

vp.matchdays[0][0].black_wins()
vp.matchdays[0][1].white_wins()
vp.matchdays[0][2].draw()
vp.matchdays[0][3].white_wins()

vp.match_schedule()
