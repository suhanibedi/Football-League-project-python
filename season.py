from __future__ import annotations
from data_structures.bset import BSet
from data_structures.referential_array import ArrayR
from dataclasses import dataclass
from team import Team
from typing import Generator, Union
from data_structures.array_sorted_list import ArraySortedList
from constants import TeamStats, PlayerStats, ResultStats
from data_structures.linked_list import LinkedList
from game_simulator import GameSimulator


@dataclass
class Game:
    """
    Simple container for a game between two teams.
    Both teams must be team objects, there cannot be a game without two teams.

    Note: Python will automatically generate the init for you.
    Use Game(home_team: Team, away_team: Team) to use this class.
    See: https://docs.python.org/3/library/dataclasses.html
    """
    home_team: Team = None
    away_team: Team = None



class WeekOfGames:
    """
    Simple container for a week of games.

    A fixture must have at least one game.
    """

    def __init__(self, week: int, games: ArrayR[Game]) -> None:
        """
        Container for a week of games.

        Args:
            week (int): The week number.
            games (ArrayR[Game]): The games for this week.
        """
        self.games: ArrayR[Game] = games
        self.week: int = week
        self.current_index = 0

    def get_games(self) -> ArrayR:
        """
        Returns the games in a given week.

        Returns:
            ArrayR: The games in a given week.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.games

    def get_week(self) -> int:
        """
        Returns the week number.

        Returns:
            int: The week number.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.week

    def __iter__(self):
        """
        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        self.current_index = 0
        return self

    def __next__(self):
        """
        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        if self.current_index < len(self.games):
            value = self.games[self.current_index]
            self.current_index += 1
            return value
        else:
            raise StopIteration


class Season:
    def __init__(self, teams: ArrayR[Team]) -> None:
        """
        Initializes the season with a schedule.

        Args:
            teams (ArrayR[Team]): The teams played in this season.

        Complexity:
            Best Case Complexity: O(N^2), where N is the number of teams in the season.
            Worst Case Complexity: O(N^2), where N is the number of teams in the season.
        
        Complexity Analysis:
        The best case scenario occurs when each team is added to the end of the leaderboard arraysortedlist. This
        makes the complexity of the add method in arraysortedlist class as O(log(N)), where N is the number of teams 
        in the season. Each team playing the season is added to the leaderboard, so complexity of adding teams to 
        leaderboard becomes O(N(log(N))). However, the ArrayR produced by _generate_schedule method into self.schedule
        linked list has complexity of O(N^2) (as complexity of _generate_schedule method grows at faster rate than complexity
        of append method in linked list). When simplifying overall best case complexity, O(N^2) has a faster growth rate than
        O(N(log(N))), and as a result best case complexity is O(N^2), where N is the number of teams in the season.

        The worst case scenario occurs when each team is added to the start of the leaderboard arraysortedlist. This
        makes the complexity of the add method in arraysortedlist class as O(N), where N is the number of teams 
        in the season. Each team playing the season is added to the leaderboard, so complexity of adding teams to 
        leaderboard becomes O(N^2). However, the ArrayR produced by _generate_schedule method into self.schedule
        linked list has complexity of O(N^2) (as complexity of _generate_schedule method grows at faster rate than complexity
        of append method in linked list). When simplifying overall best case complexity, the worst case complexity is O(N^2), 
        where N is the number of teams in the season.
        """
        Team.reset_counter()
        self.w = 1
        self.leaderboard = ArraySortedList(len(teams))
        self.teams = teams
        for t in self.teams:
            self.leaderboard.add(t)
        self.schedule = LinkedList()
        for w in self._generate_schedule():
            self.schedule.append(w)


    def _generate_schedule(self) -> ArrayR[ArrayR[Game]]:
        """
        Generates a schedule by generating all possible games between the teams.

        Return:
            ArrayR[ArrayR[Game]]: The schedule of the season.
                The outer array is the weeks in the season.
                The inner array is the games for that given week.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams in the season.
            Worst Case Complexity: O(N^2) where N is the number of teams in the season.
        """
        num_teams: int = len(self.teams)
        weekly_games: list[ArrayR[Game]] = []
        flipped_weeks: list[ArrayR[Game]] = []
        games: list[Game] = []

        # Generate all possible matchups (team1 vs team2, team2 vs team1, etc.)
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                games.append(Game(self.teams[i], self.teams[j]))

        # Allocate games into each week ensuring no team plays more than once in a week
        week: int = 0
        while games:
            current_week: list[Game] = []
            flipped_week: list[Game] = []
            used_teams: BSet = BSet()

            week_game_no: int = 0
            for game in games[:]:  # Iterate over a copy of the list
                if game.home_team.get_number() not in used_teams and game.away_team.get_number() not in used_teams:
                    current_week.append(game)
                    used_teams.add(game.home_team.get_number())
                    used_teams.add(game.away_team.get_number())

                    flipped_week.append(Game(game.away_team, game.home_team))
                    games.remove(game)
                    week_game_no += 1

            weekly_games.append(ArrayR.from_list(current_week))
            flipped_weeks.append(ArrayR.from_list(flipped_week))
            week += 1

        return ArrayR.from_list(weekly_games + flipped_weeks)

    def simulate_season(self) -> None:
        """
        Simulates the season.

        Complexity:
            Assume simulate_game is O(1)
            Remember to define your variables and their complexity.

            Best Case Complexity: O(W(W^2)), where W is the number of weeks in a season (or equivalently, length of 
            self.schedule).
        
            Worst Case Complexity: O(W^2(W^4 + g(G + D + M + S + N(k+N) + GS + l + R(h^2 + a^2)))), where W is the 
            number of weeks in a season (or equivalently, length of self.schedule), g is number of games in a week, G is 
            number of goalkeeper players in team with most number of players, D is number of defender players in team with
            most number of players, M is number of midfielder players in team with most number of players, S is number of 
            striker players in team with most number of players, N is table_size from HashyStepTable class, k is len(teamstatskey),
            GS is GameSimulator.simulate() complexity, l is the TABLE_SIZE from HashyStepTable class, R is len(resultstatskey),
            h is number of players in home_team and a is number of players in away_team.
        
        Complexity analysis:
        The best case scenario is when the season has no games, due to no teams playing the season. As a result, this means that
        the program ends at the break statement, making best case complexity O(W(W^2)) (where W is best complexity of no_of_games()
        method and W^2 is best complexity of get_next_game method). 

        The worst case scenario occurs when a season contains games, and the games have valid scorers, tacklers, assisters and 
        intercepters. This means the worst case complexity of get_players method, getitem method for hash table, getitem method for
        hashysteptable, players_stats_update method and adding teams to leaderboard should be considered. This makes the simplification
        of worst case complexity as answered above.
        """
        while self.w <= self.no_of_games():
            game_played_week = self.get_next_game()
            if game_played_week is None:
                self.w = 1
                break
            for g in game_played_week:
                self.home_team_players = g.home_team.get_players()
                self.away_team_players = g.away_team.get_players()
                self.outcome = GameSimulator.simulate(g.home_team, g.away_team)

                if self.outcome[ResultStats(ResultStats.HOME_GOALS).value] > self.outcome[ResultStats(ResultStats.AWAY_GOALS).value]:
                    g.home_team[TeamStats.WINS] = g.home_team[TeamStats.WINS] + 1
                    g.away_team[TeamStats.LOSSES] = g.away_team[TeamStats.LOSSES] + 1

                if self.outcome[ResultStats(ResultStats.HOME_GOALS).value] < self.outcome[ResultStats(ResultStats.AWAY_GOALS).value]:
                    g.away_team[TeamStats.WINS] = g.away_team[TeamStats.WINS] + 1
                    g.home_team[TeamStats.LOSSES] = g.home_team[TeamStats.LOSSES] + 1

                if self.outcome[ResultStats(ResultStats.HOME_GOALS).value] == self.outcome[ResultStats(ResultStats.AWAY_GOALS).value]:
                    g.away_team[TeamStats.DRAWS] = g.away_team[TeamStats.DRAWS] + 1
                    g.home_team[TeamStats.DRAWS] = g.home_team[TeamStats.DRAWS] + 1

                g.home_team[TeamStats.GOALS_FOR] += self.outcome[ResultStats(ResultStats.HOME_GOALS).value]
                g.away_team[TeamStats.GOALS_AGAINST] += self.outcome[ResultStats(ResultStats.HOME_GOALS).value]
                g.away_team[TeamStats.GOALS_FOR] += self.outcome[ResultStats(ResultStats.AWAY_GOALS).value]
                g.home_team[TeamStats.GOALS_AGAINST] += self.outcome[ResultStats(ResultStats.AWAY_GOALS).value]

                if self.outcome[ResultStats(ResultStats.GOAL_SCORERS).value] is not None:
                    self.player_stats_update(ResultStats.GOAL_SCORERS, PlayerStats.GOALS)

                if self.outcome[ResultStats(ResultStats.GOAL_ASSISTS).value] is not None:
                    self.player_stats_update(ResultStats.GOAL_ASSISTS, PlayerStats.ASSISTS)

                if self.outcome[ResultStats(ResultStats.INTERCEPTIONS).value] is not None:
                    self.player_stats_update(ResultStats.INTERCEPTIONS, PlayerStats.INTERCEPTIONS)

                if self.outcome[ResultStats(ResultStats.TACKLES).value] is not None:
                    self.player_stats_update(ResultStats.TACKLES, PlayerStats.TACKLES)
        
                self.w += 1
                self.leaderboard = ArraySortedList(len(self.teams))
                for t in self.teams:
                    self.leaderboard.add(t)

    def player_stats_update(self, key: ResultStats, stat: PlayerStats):
        """
        Updates the player statistic.

        Args:
            key: The resultstats key to be updated.
            stat: The playerstat to be updated.

        Complexity:
            Best Case Complexity: O(R(h + a)), where R is len(resultstats key), h is number
            of players in home_team and a is number of players in away_team.
        
            Worst Case Complexity: O(R(h^2 + a^2)), where R is len(resultstats key), h is number
            of players in home_team and a is number of players in away_team.
        
        Complexity analysis:
        The best case scenario occurs when the getitem method of linkedlist runs in best time complexity, 
        which is when the index argument is zero, making time complexity of getitem method O(1). The outer 
        loop has complexity of O(R), and the inner loop has complexity of O(h) or O(a) (depending on which 
        team). Hence, the simplified best case complexity is O(R(h + a)), where R is len(resultstats key), 
        h is number of players in home_team and a is number of players in away_team.

        The worst case scenario occurs when the getitem method of linkedlist runs in worst time complexity,
        which is when the index argument is the length of home_team or away_team. Hence, the simplified time
        complexity is O(R(h^2 + a^2)), where R is len(resultstats key), h is number
        of players in home_team and a is number of players in away_team.
        """
        for p_name in self.outcome[ResultStats(key).value]:
            i = 0
            while i < len(self.home_team_players):
                if self.home_team_players[i].get_name() == p_name:
                    self.home_team_players[i][stat] += 1
                    break
                i += 1
        for p_name in self.outcome[ResultStats(key).value]:
            i = 0
            while i < len(self.away_team_players):
                if self.away_team_players[i].get_name() == p_name:
                    self.away_team_players[i][stat] += 1
                    break
                i += 1

    def delay_week_of_games(self, orig_week: int, new_week: Union[int, None] = None) -> None:
        """
        Delay a week of games from one week to another.

        Args:
            orig_week (int): The original week to move the games from.
            new_week (Union[int, None]): The new week to move the games to. If this is None, it moves the games to the end of the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(W^2), where W is the 
            number of weeks in a season (or equivalently, length of self.schedule)
        
        Complexity analysis:
        The best case occurs when new_week equals None. This means that the best case complexity of
        index method and delete_at_index method would be considered, which occur when index argument is 0.
        As a result, the best case complexities for these methods is constant, and so the overall best case
        complexity can be simplified to O(1) since the for loop would terminate in the first iteration.

        The worst case complexity occurs when new_week is not None. This means the worst case complexity of
        index method would be considered. This occurs when index argument is the length of the self.schedule
        linkedlist. As a result, the worst case complexity for this methods would be O(W). So, the overall
        worst case complexity can be simplified to O(W^2) since the for loop would iterate through all
        weeks of games in self.schedule.
        """
        if new_week is not None:
            updated_schedule = LinkedList()
            for w in self.schedule:
                if self.schedule.index(w) is not orig_week - 1 and self.schedule.index(w) is not new_week - 1:
                    updated_schedule.append(w)
                else:
                    if self.schedule.index(w) is new_week - 1:
                        updated_schedule.append(w)
                        updated_schedule.append(self.schedule[orig_week - 1])
            self.schedule = updated_schedule

        else:
            for w in self.schedule:
                if self.schedule.index(w) == orig_week - 1:
                    moved = self.schedule[self.schedule.index(w)]
                    self.schedule.delete_at_index(orig_week-1)
                    break
            self.schedule.append(moved)


    def get_next_game(self) -> Union[Generator[Game], None]:
        """
        Gets the next game in the season.

        Returns:
            Game: The next game in the season.
            or None if there are no more games left.

        Complexity:
            Best Case Complexity: O(W^2), where W is the number of weeks in a season (or equivalently, length of 
            self.schedule).
            Worst Case Complexity: O(W^4), where W is the number of weeks in a season (or equivalently, length of 
            self.schedule).
        
        Complexity analysis:
        The best case scenario occurs when the return statement is reached in the first iteration of the outer and
        inner loop. The outer loop uses the no_of_games() method, which has best time complexity of O(W). The inner 
        loop uses the getitem method of linkedlist, which has best time complexity of O(1). The getitem method of 
        linkedlist is also used in the return statement, however the best complexity cannot be applied for both getitems,
        because it is not possible for index input in both these getitem calls to be 0 (at index 0 the best case occurs). 
        Hence, the overall best case complexity can be simplified to O(W^2), where W is the number of weeks in a season 
        (or equivalently, length of self.schedule).

        The worst case scenario occurs when all iterations of the outer ane inner loop take place, before reaching return
        statement (where self.schedule[week-1] is returned). The outer loop uses the no_of_games() method, which has worst
        time complexity of O(W^2). The inner loop uses the getitem of linkedlist, which has worst time complexity of O(W). 
        The return statement that calls getitem method of linkedlist also has worst time complexity of O(W^2). As a result,
        the overall worst case complexity can be simplified to O(W^4), where W is the number of weeks in a season 
        (or equivalently, length of self.schedule).
        """
        G = 0
        i = 0
        week = 1
        while G <= self.no_of_games():
            for g in self.schedule[i]:
                G += 1
                if G == self.w:
                    return self.schedule[week-1]
            week += 1 
            i += 1
        return None
    
    def no_of_games(self) -> int:
        """
        Calculates the number of games in a season.

        Returns:
            int: number of games in a season.

        Complexity:
            Best Case Complexity: O(W), where W is the number of weeks in a season (or equivalently, length of 
            self.schedule).
            Worst Case Complexity: O(W^2), where W is the number of weeks in a season (or equivalently, length of 
            self.schedule).
        
        Complexity analysis:
        The best case complexity occurs when the getitem method of linkedlist runs in best complexity time. As this
        getitem calls _get_node_of_index method of linkedlist class, the best complexity time of getitem depends on
        the best complexity time of _get_node_of_index method. The best complexity time of _get_node_of_index method 
        occurs when the index argument is zero, making the complexity of _get_node_of_index method and hence the 
        complexity of getitem method O(1). Because the getitem method of linkedlist is called in a while loop over
        the length of self.schedule linkedlist, the best case complexity can be expressed as O(W), where W is the 
        number of weeks in a season (or equivalently, length of self.schedule).

        The worst case complexity occurs when the getitem method of linkedlist runs in worst complexity time. As this
        getitem calls _get_node_of_index method of linkedlist class, the worst complexity time of getitem depends on
        the worst complexity time of _get_node_of_index method. The worst complexity time of _get_node_of_index method 
        occurs when the index argument is len(linkedlist), making the complexity of _get_node_of_index method and hence the 
        complexity of getitem method O(W). Because the getitem method of linkedlist is called in a while loop over
        the length of self.schedule linkedlist, the best case complexity can be expressed as O(W^2), where W is the 
        number of weeks in a season (or equivalently, length of self.schedule).

        """
        c = 0
        no_games = 0
        while c < len(self.schedule):
            no_games += len(self.schedule[c])
            c += 1
        return no_games

    def get_leaderboard(self) -> ArrayR[ArrayR[Union[int, str]]]:
        """
        Generates the final season leaderboard.

        Returns:
            ArrayR(ArrayR[ArrayR[Union[int, str]]]):
                Outer array represents each team in the leaderboard
                Inner array consists of 10 elements:
                    - Team name (str)
                    - Games Played (int)
                    - Points (int)
                    - Wins (int)
                    - Draws (int)
                    - Losses (int)
                    - Goals For (int)
                    - Goals Against (int)
                    - Goal Difference (int)
                    - Previous Five Results (ArrayR(str)) where result should be WIN LOSS OR DRAW

        Complexity:
            Best Case Complexity: O(T * k), where k is len(teamstats key), T is number of teams in self.leaderboard
            Worst Case Complexity: O(T(k+N)), where k is len(teamstats key), N is table_size from HashyStepTable class
            and T is number of teams in self.leaderboard.
        
        Complexity analysis:
        The best case complexity occurs when the getitem method of hashystep table called for team.statistics runs in best
        time complexity, which would be O(k). Because this getitem method is called for all teams in self.leaderboard, the best
        case complexity can be expressed as O(T * k), where k is len(teamstats key), T is number of teams in self.leaderboard.

        The worst case complexity occurs when the getitem method of hashystep table called for team.statistics runs in worst
        time complexity, which would be O(k+N). Because this getitem method is called for all teams in self.leaderboard, the best
        case complexity can be expressed as O(T(k+N)), where k is len(teamstats key), T is number of teams in self.leaderboard.
        """
        return_array = ArrayR(len(self.teams))
        c = 0
        for t in self.leaderboard:
            each_team = ArrayR(10)
            each_team[0] = t.get_name()
            each_team[1] = t.statistics[TeamStats(TeamStats.GAMES_PLAYED).value]
            each_team[2] = t.statistics[TeamStats(TeamStats.POINTS).value]
            each_team[3] = t.statistics[TeamStats(TeamStats.WINS).value]
            each_team[4] = t.statistics[TeamStats(TeamStats.DRAWS).value]
            each_team[5] = t.statistics[TeamStats(TeamStats.LOSSES).value]
            each_team[6] = t.statistics[TeamStats(TeamStats.GOALS_FOR).value]
            each_team[7] = t.statistics[TeamStats(TeamStats.GOALS_AGAINST).value]
            each_team[8] = t.statistics[TeamStats(TeamStats.GOALS_DIFFERENCE).value]
            each_team[9] = t.statistics[TeamStats(TeamStats.LAST_FIVE_RESULTS).value]
            return_array[c] = each_team
            c += 1
        print(return_array)
        return return_array


    def get_teams(self) -> ArrayR[Team]:
        """
        Returns:
            PlayerPosition (ArrayR(Team)): The teams participating in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.teams

    def __len__(self) -> int:
        """
        Returns the number of teams in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return len(self.teams)

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the season object.

        Complexity:
            Analysis not required.
        """
        return ""

    def __repr__(self) -> str:
        """Returns a string representation of the Season object.
        Useful for debugging or when the Season is held in another data structure."""
        return str(self)
