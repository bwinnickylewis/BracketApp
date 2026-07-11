import numpy as np
# from tabulate import tabulate

class Team:
    def __init__(self,name):
        self.name = name
        # self.games_played = 0
        self.record = [] # Win = 'W', Loss = 'L', Draw = 'D'
        self.teams_played = []
        self.scores = [] # Scores are stored as [[Team score, opponent score]]
        self.game_ids = []
    def add_game(self,opponent,score,game_id):
        self.teams_played.append(opponent.get_name())
        self.game_ids.append(game_id)
        self.scores.append(score)
        if score[0]==score[1]:
            self.record.append('D')
        if score[0]>=score[1]:
            self.record.append('W')
        if score[0]<=score[1]:
            self.record.append('L')
    def remove_game(self,game_id):
        ind = np.arange(len(self.game_ids))[np.array([ids==game_id for ids in self.game_ids])][0]
        del self.record[ind]
        del self.teams_played[ind]
        del self.scores[ind]
        del self.game_ids[ind]

    def get_name(self):
        return self.name
    def change_name(self,new_name):
        self.name = new_name
    def get_games_played(self):
        return len(self.record)
    def get_teams_played(self):
        return self.teams_played
    def get_scores(self):
        return self.scores
    def get_record(self):
        return self.record
    def get_points_for(self):
        try:
            return np.sum(self.get_scores(),axis=0)[0]
        except:
            return 0
    def get_points_against(self):
        try:
            return np.sum(self.get_scores(),axis=0)[1]
        except:
            return 0
    def get_point_diff(self):
        return self.get_points_for() - self.get_points_against()
    def get_record_list(self):
        record_list = np.zeros(3)
        for result in self.get_record():
            if result=="W":
                record_list[0]+=1
            if result=="L":
                record_list[1]+=1
            if result=="D":
                record_list[2]+=1
        return record_list
    def record_string(self):
        record = self.get_record_list()
        return f'{record[0]:.0f}-{record[1]:.0f}-{record[2]:.0f}'
    def return_game_score(self,game_id):
        ind = np.arange(len(self.game_ids))[np.array([ids==game_id for ids in self.game_ids])][0]
        return [self.name,self.teams_played[ind],self.get_scores()[ind][0],self.get_scores()[ind][1]]
    


class Tournament():
    def __init__(self,name):
        self.name = name
        self.num_rr_games = 0
        self.team_names = []
        self.teams = []
        self.point_dist = [2,0,1] # Default
        self.game_id = 1
        self.id_list = []
        self.num_knockout_teams = 8
    def add_team(self,team_name):
        team = Team(team_name)
        self.team_names.append(team_name)
        self.teams.append(team)
    

    def return_team(self,team_name):
        ind = np.arange(len(self.team_names))[np.array([names==team_name for names in self.team_names])]
        if len(ind)>1:
            print(f"There is more than 1 team named {team_name}")
        elif len(ind)<1:
            print(f"There is no team named {team_name}")
        else:
        # print(ind)
            return self.teams[ind[0]]

    def add_game(self,team_1_name, team_2_name, team_1_score, team_2_score,game_id=-1):
        # Add something that will check if the game id has already been used
        if game_id in np.array(self.id_list).T:
            print(f"A game with the game id {game_id} already exists")
            return None
        default_id = False
        if game_id==-1:
            game_id = self.game_id
            default_id=True
        team_1 = self.return_team(team_1_name)
        team_2 = self.return_team(team_2_name)
        team_1.add_game(team_2,[team_1_score,team_2_score],game_id)
        team_2.add_game(team_1,[team_2_score,team_1_score],game_id)
        self.id_list.append([game_id,team_1.get_name(),team_2.get_name()])
        if default_id:
            self.game_id+=1

    def remove_game(self,game_id=1):
        ind = np.arange(len(self.id_list))[np.array([id==game_id for id in np.array(np.array(self.id_list).T[0],dtype=int)])][0]
        team_1 = self.return_team(self.id_list[ind][1])
        team_2 = self.return_team(self.id_list[ind][2])
        del self.id_list[ind]
        team_1.remove_game(game_id); team_2.remove_game(game_id)
        # del self.id_list[ind]
    def change_tourn_name(self,new_tourn_name):
        self.name = new_tourn_name
    def change_team_name(self,old_name,new_name):
        team = self.return_team(old_name)
        team.change_name(new_name)
        ind = np.arange(len(self.team_names))[np.array([name==old_name for name in self.team_names])][0]
        self.team_names[ind] = new_name
        for game in self.id_list:
            if old_name in game:
                name_ind = np.arange(len(game))[np.array(game)==old_name][0]
                game[name_ind]=new_name

    def remove_team(self,team_name):
        for game in self.id_list:
            if team_name in game:
                self.remove_game(game[0])
        ind = np.arange(len(self.team_names))[np.array([name==team_name for name in self.team_names])][0]
        del self.team_names[ind]
        del self.teams[ind]
    def return_game_stats(self):
        game_stats = []
        for game in self.id_list:
            team = self.return_team(game[1])
            stats = team.return_game_score(game[0])
            game_stats.append([game[0],stats[0],stats[2],stats[1],stats[3]])
        return game_stats
    def change_point_dist(self,new_dist):
        self.point_dist = new_dist
    def get_points(self,team):
        return np.sum(np.array(team.get_record_list())*np.array(self.point_dist))
    def get_standings(self):
        points = np.array([self.get_points(team) for team in self.teams])
        point_diff = np.array([team.get_point_diff() for team in self.teams])
        point_order = points+(point_diff/(np.max(point_diff)+1)) # Adding a tie breaker based on the point differential
        order = [x for _, x in sorted(zip(point_order, np.arange(len(self.teams))))]
        return order[::-1]
    def return_standings_array(self):
        points = np.array([self.get_points(team) for team in self.teams])
        points_for = np.array([team.get_points_for() for team in self.teams])
        points_against = np.array([team.get_points_against() for team in self.teams])

        point_diff = np.array([team.get_point_diff() for team in self.teams])
        records = np.array([team.get_record_list() for team in self.teams])
        order = self.get_standings()
        rank = np.arange(1,len(self.team_names)+1,1)
        table = [[rank[i],self.team_names[order[i]],
                  int(points[order[i]]),
                  int(np.sum(records[order[i]])),
                  int(records[order[i]][0]),
                  int(records[order[i]][1]),
                  int(records[order[i]][2]),
                  points_for[order[i]],
                  points_against[order[i]],
                  point_diff[order[i]]] for i in range(len(order))]
        return table
    def export_tournament(self,filename):
        # filename = self.name+'.csv'
        game_stats = np.array(self.return_game_stats(),dtype=str)
        np.savetxt(filename,game_stats,header='Game ID, Team 1, Team 1 Score, Team 2, Team 2 Score',delimiter=',',fmt='%s')
    def import_tournament(self,filename):
        game_stats = np.loadtxt(filename,dtype=str,delimiter=',')
        if len(self.id_list)>0:
            for id in np.array(self.id_list).T[0]:
                self.remove_game(id)
        for name in self.team_names:
            self.remove_team(name)
        for game in game_stats:
            id = int(game[0])
            team_1 = game[1]
            team_1_score = int(game[2])
            if team_1 not in self.team_names:
                self.add_team(team_1)
            team_2 = game[3]
            team_2_score = int(game[4])

            if team_2 not in self.team_names:
                self.add_team(team_2)
            self.add_game(team_1,team_2,team_1_score,team_2_score)
    # def print_table(self):
    #     points = np.array([self.get_points(team) for team in self.teams])
    #     points_for = np.array([team.get_points_for() for team in self.teams])
    #     points_against = np.array([team.get_points_against() for team in self.teams])

    #     point_diff = np.array([team.get_point_diff() for team in self.teams])
    #     records = np.array([team.get_record_list() for team in self.teams])
    #     order = self.get_standings()
    #     rank = np.arange(1,len(self.team_names)+1,1)
    #     table = [[rank[i],self.team_names[order[i]],
    #               points[order[i]],
    #               np.sum(records[order[i]]),
    #               records[order[i]][0],
    #               records[order[i]][1],
    #               records[order[i]][2],
    #               points_for[order[i]],
    #               points_against[order[i]],
    #               point_diff[order[i]]] for i in range(len(order))]
    #     print(tabulate(table, headers=['Rank', 'Team', 'Points','Games Played', 'Wins', 'Losses', 'Draws', 'Points For', 'Points Against', 'Point Diff']))
    # def print_games(self):
    #     print(tabulate(self.return_game_stats(),headers=['Game ID', 'Home Team', 'Home Team Score','Away Team', 'Away Team Score']))

