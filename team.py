from __future__ import annotations
from data_structures.referential_array import ArrayR
from constants import GameResult, PlayerPosition, PlayerStats, TeamStats
from player import Player
from typing import Collection, Union, TypeVar
from hashy_step_table import HashyStepTable
from data_structures.linked_list import LinkedList
from data_structures.linked_queue import LinkedQueue

T = TypeVar("T")


class Team:
    count = 0
    def __init__(self, team_name: str, players: ArrayR[Player]) -> None:
        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            players (ArrayR[Player]): The players of the team

        Returns:
            None

        Complexity:
            Best Case Complexity: O(l + P(k) + p + TS(k))), where l is the length of TABLE_SIZES in hashy step table class, P is the number of positions in 
            PlayerPosition class, p is the number of players in the ArrayR of players passed as an argument in __init__, TS is the number of statistics in 
            TeamStats and k is the length of the teamstats key.

            Worst Case Complexity: O(P(k + l + N)) + p + TS(k + l + N)), where N is table_size from HashyStepTable class, P is the number of positions 
            in PlayerPosition class, p is the number of players in the ArrayR of players passed as an argument in __init__, TS is the number of statistics
            in TeamStats, k is the length of the teamstats key and l is the length of TABLE_SIZES in HashyStepTable class.
        
        Complexity Analysis:
        The best case scenario and worst case scenario differentiates due to the for loop used to add linkedlists in the self.players hash step table, as
        well as the for loop used to set hashysteptable team statistics to their appropriate values (in reset stats method).

        To set a (PlayerPosition.value, LinkedList()) tuple in the hash step table (using setitem method in HashStepTable class), the best case is when 
        the _hashy_probe method in HashStepTable class first calls hash method (O(k)), then determines final hash position by terminating its for 
        loop early, and the setitem method doesn't need to call the rehash method. Hence, the complexity of the for loop used to add linkedlists in the 
        self.players hash step table becomes O(P(k)), where P is the number of positions in PlayerPosition class and k is the length of teamstats key when hash 
        position is calculated in _hashy_probe method of HashStepTable class. Same reason applies for best case of setting hashysteptable team statistics
        to their appropriate values (in reset stats method), so the complexity for reset stats method becomes TS(k), where TS is the number of statistics in 
        TeamStats and k is len(teamstats key). The 'l' and 'p' are also added to complexity because length of TABLE_SIZES is required to initialise hashy step tables, and 'p'
        represents the number of players in ArrayR of players which is used by the second for loop in init here. The overall complexity then simplifies to whichever 
        of these variables is the greatest.

        The worst case scenario occurs when the _hashy_probe method in HashStepTable class cannot determine final position early, meaning it iterates for 
        the entire table_size from HashyStepTable class. Moreover, worst case also happens when setitem method in HashStepTable class calls the rehash method.
        The complexity for rehash method in HashyStepTable class is O(l + N), where l is TABLE_SIZES and N is table_size. This means, the complexity of the for loop 
        used to add linkedlists in the self.players hash step table becomes O(P(k + l + N)), where P is the number of positions in PlayerPosition class, k is the length of 
        key when hash position is calculated in _hashy_probe method of HashStepTable class and l is TABLE_SIZES from HashyStepTable class. Same reason applies for worst case of
        setting hashysteptable team statistics to their appropriate values (in reset stats method), so its complexity is TS(k + l + n). 'l' and 'p' variables are also added to 
        final worst case complexity expression for the same reason as mentioned for best case, and the variable taking the maximum value would be the simplified worst case
        complexity.
        """
        Team.count += 1
        self.number = Team.count 
        self.name = str(team_name)
        self.statistics = HashyStepTable()
        self.reset_stats()
        self.players = HashyStepTable()
        for pos in PlayerPosition:
            self.players[pos.value] = LinkedList()
        for p in players:
            self.add_player(p)
    
    @classmethod
    def reset_counter(cls):
        """
        Resets the count global variable of Team class.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        cls.count = 0

    def reset_stats(self) -> None:
        """
        Resets all the statistics of the team to the values they were during init.

        Complexity:
            Best Case Complexity: O(TS(k)), where TS is the number of statistics in TeamStats, and k is the len(key).
            Worst Case Complexity: O(TS(k + l + N)), where TS is the number of statistics in TeamStats, k is the len(key), 
            l is the length of TABLE_SIZES in HashyStepTable class and N is table_size from HashyStepTable class.
        
        Complexity analysis:
        The setitem method in HashyStepTable class causes a best case and worst case scenario. The best case scenario is when
        the _hashy_probe method called by setitem in HashStepTable class first calls hash method (O(k)), then determines final 
        hash position by terminating its for loop early, and the setitem method doesn't need to call the rehash method. Hence, 
        setting a key value tuple in self.statistics hash step table has complexity of O(k), where k is len(teamstats key). This is repeated
        for all TeamStats, so overall best case complexity becomes O(TS(k)) where TS is the number of statistics in TeamStats.

        The worst case scenario occurs when the _hashy_probe method in HashStepTable class cannot determine final position early, meaning it iterates for 
        the entire table_size from HashyStepTable class. Moreover, worst case also happens when setitem method in HashStepTable class calls the rehash method.
        The complexity for rehash method in HashyStepTable class is O(l+N), where l is TABLE_SIZES and N is table_size. This means, the complexity of setting
        a key value tuple in self.statistics hash step table is O(k + l + N), where k is len(teamstats key), l is the length of TABLE_SIZES in HashyStepTable class and N is 
        table_size from HashyStepTable class. This is repeated for all TeamStats, so overall best case complexity becomes O(TS(k+l+N)) where TS is the number of 
        statistics in TeamStats.

        """
        for stat in TeamStats:
            if stat.value == TeamStats(TeamStats.LAST_FIVE_RESULTS).value:
                self.statistics[stat.value] = LinkedQueue()
            else:
                self.statistics[stat.value] = 0

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            Best Case Complexity: O(k), where k is len(teamstats key)
            Worst Case Complexity: O(k + N), where k is the len(teamstats key) and N is table_size from HashyStepTable class.

        Complexity Analysis:
        The best case scenario and worst case scenario is distinguished by the getitem method of HashyStepTable which is
        called via 'self.players[player.position.value]'. The best case occurs when the getitem method calls the _hashy_probe
        method in HashyStepTable, and the _hashy_probe method first calls hash method to get initial position (which has complexity
        of O(k)). But a final position is obtained using a calculated step size in the _hashy_probe method, where the most ideal situation
        is when the loop to achieve this terminates early. Hence, the getitem complexity simplifies to O(k), where k is len(teamstats key). Note that
        the append method of linkedlists have complexity of O(1) (as player gets added to the end of linkedlist). Hence. best case complexity is
        expressed as O(k), where k is len(key).

        The worst case scenario occurs when obtaining the final position in _hashy_probe method using a calculated step size from the loop has to run N times, where N is
        table_size from HashyStepTable class. So in summary, the _hashy_probe method first calls hash method to get initial position (which has complexity
        of O(k)) and then runs the loop to obtain final position N times, so the worst case complexity can be expressed as O(k +  N), where k is len(teamstats key) and 
        N is table_size from HashyStepTable class.
        """
        self.players[player.position.value].append(player)


    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(L), where L is the number of players in the linkedlist.
        
        Complexity Analysis:
        The best case occurs when the item is at the beginning of the linkedlist (in this case item being player), when the 
        index method of linkedlist is called. This complexity is O(1). In delete_at_index linkedlist method, the best case
        is when its index argument is zero, allowing the method to run in constant time O(1). Overall, this makes best case
        complexity O(1).

        The worst case scenario occurs when the player item is at the end of the linkedlist, when index method of linkedlist is
        called. This means that the complexity is O(L), where L is the number of players in the linkedlist for a certain player position,
        because the index method iterates through all players to locate the player item being searched for. Moreover, the delete_at_index 
        linkedlist method would have worst case complexity of O(L) as well, since it would call get_node_at_index method, which has worst 
        case complexity if the index equalled to the number of players in the linkedlist. Overall, this makes worst case complexity as O(L).

        """
        i = self.players[player.position.value].index(player)
        self.players[player.position.value].delete_at_index(i)

    def get_number(self) -> int:
        """
        Returns the number of the team.

        Complexity: O(1)
            Analysis not required.
        """
        return self.number

    def get_name(self) -> str:
        """
        Returns the name of the team.

        Complexity: O(1)
            Analysis not required.
        """
        return self.name

    def get_players(self, position: Union[PlayerPosition, None] = None) -> Union[Collection[Player], None]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (Union[PlayerPosition, None]): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder this includes the ArrayR
            which was previously prohibited.

            None: When no players match the criteria / team has no players

        Complexity:
            Best Case Complexity: O(k), where k is len(teamstats key)
            Worst Case Complexity: O(G + D + M + S + N(k + N))), where G is number of players in self.players['GoalKeeper'],
            D is number of players in self.players['Defender'], M is number of players in self.players['Midfielder'], S is 
            number of players in self.players['Striker'], k is len(teamstats key) and N is table_size from HashyStepTable class.
        
        Complexity analysis:
        The best case scenario occurs when a position argument is provided, as it means that this method would only
        run the getitem method of HashStepTable class to return a value (linked list of players) to one PlayerPosition
        key in self.players HashStepTable. The best case complexity for getitem method is O(k), where k is len(key). This
        is because the getitem method calls the _hashy_probe method in HashyStepTable, and the _hashy_probe method first calls hash method to get initial position (which has complexity
        of O(k)). But a final position is obtained using a calculated step size in the _hashy_probe method, where the most ideal situation
        is when the loop to achieve this terminates early. Hence, the getitem complexity simplifies to O(k), where k is len(teamstats key). 

        The worst case scenario occurs when no position argument is provided, meaning that players across all possible playerpositions
        need to be returned. To do this, the first check is to see if there are no players in all possible player positions, which requires
        iterating over all keys in self.players hashsteptable (O(N), N is table_size in self.players). Then, there are individual checks
        to see if linkedlists for each value in self.players are not empty, which requires use of getitem method from HashyStepStable (this has worst 
        case complexity of O(N(k + N)), where k is len(teamstats key) and N is table_size from HashyStepTable class). The event that all position keys aren't empty, 
        a loop is used to add all players playing per position into a collective all_players linkedlist, hence the complexities being G when iterating over
        linkedlist for all GoalKeepers (where G is nunber of goalkeepers), D for linkedlist of Defenders (where D is number of defenders), M for linkedlist of
        Midfielders (where M is number of Midfielders), and S for linkedlist of Strikers (where S is number of Strikers). 
        """
        all_players = LinkedList()
        if position is None:
            f = 0
            for pos in self.players.keys():
                if self.players[pos].is_empty() == True:
                    f += 1
                    continue
            if f == len(self.players.keys()):
                return None
            if self.players[PlayerPosition(PlayerPosition.GOALKEEPER).value].is_empty() is False:
                for p in self.players[PlayerPosition(PlayerPosition.GOALKEEPER).value]:
                    all_players.append(p)
            if self.players[PlayerPosition(PlayerPosition.DEFENDER).value].is_empty() is False:
                for p in self.players[PlayerPosition(PlayerPosition.DEFENDER).value]:
                    all_players.append(p)
            if self.players[PlayerPosition(PlayerPosition.MIDFIELDER).value].is_empty() is False:
                for p in self.players[PlayerPosition(PlayerPosition.MIDFIELDER).value]:
                    all_players.append(p)
            if self.players[PlayerPosition(PlayerPosition.STRIKER).value].is_empty() is False:
                for p in self.players[PlayerPosition(PlayerPosition.STRIKER).value]:
                    all_players.append(p)
            return all_players
        else:
            if self.players[position.value].is_empty() == True:
                return None
            return self.players[position.value]

    
    def get_statistics(self):
        """
        Get the statistics of the team

        Returns:
            statistics: The teams' statistics

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.statistics

    def get_last_five_results(self) -> Union[Collection[GameResult], None]:
        """
        Returns the last five results of the team.
        If the team has played less than five games,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the array should be an array of size 4
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        **Important Note:**
        If this method is called before the team has played any games,
        return None the reason for this is explained in the specefication.

        Returns:
            Collection[GameResult]: The last five results of the team
            or
            None if the team has not played any games.

        Complexity:
            Best Case Complexity: O(k), where k is len(teamstats key)
            Worst Case Complexity: O(k + N), where k is len(teamstats key) and N is table_size from HashyStepTable class.
        
        Complexity analysis:
        Only getitem of self.statistics hashysteptable is called in this method. The best case for getitem of hashysteptable
        is O(k), where k is len(key), because the getitem method calls the _hashy_probe method in HashyStepTable, and the _hashy_probe
        method first calls hash method to get initial position (which has complexity of O(k)). But a final position is obtained using a 
        calculated step size in the _hashy_probe method, where the most ideal situation is when the loop to achieve this terminates early.

        The worst case scenario is when the _hashy_probe method called by getitem method cannot terminate the for loop early, so this makes
        the getitem worst case complexity as O(k + N), where k is len(teamstats key) and N is table_size from HashyStepTable class.
        """
        if self.statistics[TeamStats(TeamStats.GAMES_PLAYED).value] == 0:
            return None
        return self.statistics[TeamStats(TeamStats.LAST_FIVE_RESULTS).value]
        
    def get_top_x_players(self, player_stat: PlayerStats, num_players: int) -> list[tuple[int, str, Player]]:
        """
        Note: This method is only required for FIT1054 students only!

        Args:
            player_stat (PlayerStats): The player statistic to use to order the top players
            num_players (int): The number of players to return from this team

        Return:
            list[tuple[int, str, Player]]: The top x players from this team
        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError

    def __setitem__(self, statistic: TeamStats, value: int) -> None:
        """
        Updates the team's statistics.

        Args:
            statistic (TeamStats): The statistic to update
            value (int): The new value of the statistic

        Complexity:
            Best Case Complexity: O(k), where k is len(teamstats key)
            Worst Case Complexity: O(k + N + l + G + D + M + S + N(k+N)), where k is len(teamstats key), N is table_size from HashyStepTable class,
            l is the length of TABLE_SIZES in HashyStepTable class, G is number of players in self.players['GoalKeeper'],
            D is number of players in self.players['Defender'], M is number of players in self.players['Midfielder'], S is 
            number of players in self.players['Striker'].
        
        Complexity analysis:
        The best case scenario occurs when the TeamStats Goals Against or Teamstats Goals For is passed in the statistic argument of this method.
        This means the hash key for Goals Difference in self.statistics hashysteptable is updated, which requires use of hashysteptable's setitem
        method and getitem method, that has the best case complexity of O(k) (when final position determined by early termination of loop, and no rehashing needed).
        The getitem method's best case complexity is when _hashy_probe method runs in best case complexity (O(K)) and adding two of the same variables can
        be simplified to O(k).
        
        The worst case scenario occurs when the TeamStats Win, TeamStats Losses or TeamStats Draws is passed in the statistic argument of this method.
        Resetting the Games Played key in self.statistics hashysteptable requires use of setitem method and getitem method, and both have worst case 
        complexities of O(k + N + l) and O(k + N) respectively (hence when added, can be simplified to O(k + N + l). Then, the while loop used to
        iterate through all the players in linkedlist obtained from self.get_players() has complexity of O(G + D + M + S + N(k + N)), and inside this while
        loop resetting player statistics hashperfectiontable has O(1) complexity (and obtaining the player to reset games played for has worst complexity of
        the length of self.get_players() (G+D+M+S)). Hence, overall worst case complexity can be simplified to O(k + N + l + G + D + M + S + N(k+N)), 
        where k is len(teamstats key), N is table_size from HashyStepTable class, l is the length of TABLE_SIZES in HashyStepTable class, G is number of players in 
        self.players['GoalKeeper'], D is number of players in self.players['Defender'], M is number of players in self.players['Midfielder'], S is 
        number of players in self.players['Striker'].

        """
        self.statistics[statistic.value] = value

        if statistic.value == TeamStats(TeamStats.GOALS_AGAINST).value or statistic.value == TeamStats(TeamStats.GOALS_FOR).value:
            self.statistics[TeamStats.GOALS_DIFFERENCE.value] = self.statistics[TeamStats.GOALS_FOR.value] - self.statistics[TeamStats.GOALS_AGAINST.value]

        if statistic.value == TeamStats(TeamStats.WINS).value:
            self.statistics[TeamStats(TeamStats.GAMES_PLAYED).value] = self.statistics[TeamStats(TeamStats.GAMES_PLAYED).value] + 1
            p = 0
            while p < len(self.get_players()):
                self.get_players()[p][PlayerStats.GAMES_PLAYED] += 1
                p += 1
            self.statistics[TeamStats(TeamStats.POINTS).value] += GameResult(GameResult.WIN)
            if self.statistics[TeamStats(TeamStats.GAMES_PLAYED).value] <= 5:
                self.statistics[TeamStats.LAST_FIVE_RESULTS.value].append(GameResult.WIN)
            if self.statistics[TeamStats(TeamStats.GAMES_PLAYED).value] > 5:
                self.statistics[TeamStats(TeamStats.LAST_FIVE_RESULTS).value].serve()
                self.statistics[TeamStats(TeamStats.LAST_FIVE_RESULTS).value].append(GameResult.WIN)

        if statistic.value == TeamStats(TeamStats.LOSSES).value:
            self.statistics[TeamStats(TeamStats.GAMES_PLAYED).value] = self.statistics[TeamStats(TeamStats.GAMES_PLAYED).value] + 1
            p = 0
            while p < len(self.get_players()):
                self.get_players()[p][PlayerStats.GAMES_PLAYED] += 1
                p += 1
            self.statistics[TeamStats(TeamStats.POINTS).value] += GameResult(GameResult.LOSS)
            if self.statistics[TeamStats(TeamStats.GAMES_PLAYED).value] <= 5:
                self.statistics[TeamStats.LAST_FIVE_RESULTS.value].append(GameResult.LOSS)
            if self.statistics[TeamStats(TeamStats.GAMES_PLAYED).value] > 5:
                 self.statistics[TeamStats(TeamStats.LAST_FIVE_RESULTS).value].serve()
                 self.statistics[TeamStats(TeamStats.LAST_FIVE_RESULTS).value].append(GameResult.LOSS)

        if statistic.value == TeamStats(TeamStats.DRAWS).value:
            self.statistics[TeamStats(TeamStats.GAMES_PLAYED).value] = self.statistics[TeamStats(TeamStats.GAMES_PLAYED).value] + 1
            p = 0
            while p < len(self.get_players()):
                self.get_players()[p][PlayerStats.GAMES_PLAYED] += 1
                p += 1
            self.statistics[TeamStats(TeamStats.POINTS).value] += GameResult(GameResult.DRAW)
            if self.statistics[TeamStats(TeamStats.GAMES_PLAYED).value] <= 5:
                self.statistics[TeamStats.LAST_FIVE_RESULTS.value].append(GameResult.DRAW)
            if self.statistics[TeamStats(TeamStats.GAMES_PLAYED).value] > 5:
                 self.statistics[TeamStats(TeamStats.LAST_FIVE_RESULTS).value].serve()
                 self.statistics[TeamStats(TeamStats.LAST_FIVE_RESULTS).value].append(GameResult.DRAW)
        

    def __getitem__(self, statistic: TeamStats) -> int:
        """
        Returns the value of the specified statistic.

        Args:
            statistic (TeamStats): The statistic to return

        Returns:
            int: The value of the specified statistic

        Raises:
            ValueError: If the statistic is invalid

        Complexity:
            Best Case Complexity: O(k), where k is len(teamstats key)
            Worst Case Complexity: O(k + N), where k is len(teamstats key) and N is table_size from HashyStepTable class.
        
        Complexity analysis:
        The best case scenario occurs when the getitem method of hashysteptable calls _hashy_probe method, and _hashy_probe
        method runs in best time complexity. The _hashy_probe method runs in best time when it obtains initial position of key (O(k))
        and gets the key's final position using calculated step size quickly (by terminating the loop early). This simplifies the best
        case complexity to O(k), where k is len(teamstats key).

        The worst case scenario occurs when the getitem method of hashysteptable calls _hashy_probe method, and _hashy_probe
        method runs in worst time complexity. The _hashy_probe method runs in worst time when it obtains initial position of key (O(k))
        and gets the key's final position using calculated step size by iterating through N. This simplifies the worst case complexity to
        O(k + N), where k is len(teamstats key) and N is table_size from HashyStepTable class.
            
        """
        return self.statistics[statistic.value]

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Returns:
            int: The length of players in the team.

        Complexity:
            Best Case Complexity: O(N(k)), where N is table_size from HashyStepTable class, and k is len(teamstats key).
            Worst Case Complexity: O(N(k + N)), where N is table_size from HashyStepTable class, and k is len(teamstats key).
        
        Complexity Analysis:
        The best case scenario occurs when getitem of self.players hashysteptable operates in best time complexity. This would be
        O(k), because the getitem method of hashysteptable calls _hashy_probe method, and _hashy_probe method runs in best time complexity. The 
        _hashy_probe method runs in best time when it obtains initial position of key (O(k)) and gets the key's final position using calculated 
        step size quickly (by terminating the loop early). Because getitem of self.players hashysteptable is called for length of self.players.keys(),
        the overall best case complexity can be simplified to O(N(k)), where N is table_size from HashyStepTable class, and k is len(teamstats key).

        The worst case scenario occurs when getitem of self.players hashysteptable operates in worst time complexity. This would be O(k + N),
        because the getitem method of hashysteptable calls _hashy_probe method, and _hashy_probe method runs in worst time complexity.
        The _hashy_probe method runs in worst time when it obtains initial position of key (O(k)) and gets the key's final position using calculated step 
        size by iterating through N. Because getitem of self.players hashysteptable is called for length of self.players.keys(),
        the overall best case complexity can be simplified to O(N(k + N)), where N is table_size from HashyStepTable class, and k is len(teamstats key).
        """
        length = 0
        for p in self.players.keys():
            length += len(self.players[p])
        return length

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity:
            Analysis not required.
        """
        return ""

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure."""
        return str(self)
    
    def __lt__(self, other: Team) -> bool:
        """
        A comparison method to compare two Team class objects, in particular which one is less than the other.

        Args:
            other: The Team class object used for comparison.

        Returns:
            bool: True if other Team object is less than self Team object, False otherwise.

        Complexity:
            Best case complexity: O(k), where k is len(teamstats key).
            Worst case complexity: O(k + N), where k is len(teamstats key) and N is table_size from HashyStepTable class.
        
        Complexity analysis:
        The best case and worst case scenarios differentiate due to the getitem method of hashysteptable which is called
        when the points, goals difference, goals for and name of self team need to be compared with the other team. The best
        case scenario is when only the points comparison is made and true is returned, which would happen when getting the 
        points of self team and other team is done in best complexity of getitem (which is O(k)). Hence, best case complexity of 
        this method can be expressed as O(k), where k is len(teamstats key).

        The worst case scenario occurs when there is a tie in points, goals difference and goals for comparisons. All comparisons
        require the use of getitem method from self.statistics' hashysteptable, and to obtain worst case complexity this means getting
        the points, goals difference and goals for is done in worst complexity of getitem (which is O(k + N)). But because the getitem
        method is called twice per comparison (once for self team and once for other team), and there are three comparisons to make, the 
        overall worst case complexity can be simplified to O(k + N), where k is len(teamstats key) and N is table_size from HashyStepTable class.
        """
        if self.statistics[TeamStats(TeamStats.POINTS).value] > other.statistics[TeamStats(TeamStats.POINTS).value]:
            return True
        if self.statistics[TeamStats(TeamStats.POINTS).value] < other.statistics[TeamStats(TeamStats.POINTS).value]:
            return False
        if self.statistics[TeamStats(TeamStats.GOALS_DIFFERENCE).value] > other.statistics[TeamStats(TeamStats.GOALS_DIFFERENCE).value]:
            return True
        if self.statistics[TeamStats(TeamStats.GOALS_DIFFERENCE).value] < other.statistics[TeamStats(TeamStats.GOALS_DIFFERENCE).value]:
            return False
        if self.statistics[TeamStats(TeamStats.GOALS_FOR).value] > other.statistics[TeamStats(TeamStats.GOALS_FOR).value]:
            return True
        if self.statistics[TeamStats(TeamStats.GOALS_FOR).value] < other.statistics[TeamStats(TeamStats.GOALS_FOR).value]:
            return False
        return self.get_name() < other.get_name()
    
    def __eq__(self, other: Team) -> bool:
        """
        A comparison method to compare two Team class objects, in particular if both are equal.

        Args:
            other: The Team class object used for comparison.

        Returns:
            bool: True if other Team object is equal to self Team object, False otherwise.

        Complexity:
            Best case complexity: O(k), where k is len(teamstats key).
            Worst case complexity: O(k + N), where k is len(teamstats key) and N is table_size from HashyStepTable class.
        
        Complexity analysis:
        The best case and worst case scenarios differentiate due to the getitem method of hashysteptable which is called
        when the points, goals difference, goals for and name of self team need to be compared with the other team. The best
        case scenario is when only the points comparison is made and false is returned, which would happen when getting the 
        points of self team and other team is done in best complexity of getitem (which is O(k)). Hence, best case complexity of 
        this method can be expressed as O(k), where k is len(teamstats key).

        The worst case scenario occurs when there is a tie in points, goals difference and goals for comparisons. All comparisons
        require the use of getitem method from self.statistics' hashysteptable, and to obtain worst case complexity this means getting
        the points, goals difference and goals for is done in worst complexity of getitem (which is O(k + N)). But because the getitem
        method is called twice per comparison (once for self team and once for other team), and there are three comparisons to make, the 
        overall worst case complexity can be simplified to O(k + N), where k is len(teamstats key) and N is table_size from HashyStepTable class.
        """
        if self.statistics[TeamStats(TeamStats.POINTS).value] != other.statistics[TeamStats(TeamStats.POINTS).value]:
            return False
        if self.statistics[TeamStats(TeamStats.GOALS_DIFFERENCE).value] != other.statistics[TeamStats(TeamStats.GOALS_DIFFERENCE).value]:
            return False
        if self.statistics[TeamStats(TeamStats.GOALS_FOR).value] != other.statistics[TeamStats(TeamStats.GOALS_FOR).value]:
            return False
        if self.get_name() != other.get_name():
            return False
        return True
