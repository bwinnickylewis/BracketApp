import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from BracketTools import Team, Tournament


class Application(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        import tkinter as tk

        self.iconbitmap("logo.ico")
        self.title('BracketApp')
        self.geometry("1200x500")
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.tourn_name = ''
        self.start_page = StartPage(self)
        self.start_page.grid(row=0,column=0)

        self.tournament = Tournament(self.tourn_name)
    
    def new_frame(self,old_frame,new_frame):
        self.clear_frame(old_frame)

        self.display_frame = new_frame(self)
        self.display_frame.grid(row=0,column=0)
    def name_tourn(self,_event=None):
        self.tournament.change_tourn_name(self.tourn_name)
    def enter_teams(self,_event=None):
        self.teams = EnterTeams(self)




class StartPage(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        # self.button_bonus = ttk.Button(self, text="Bonuses", command=popup_bonus)
        self.parent = parent
        self.grid(column=0,row=0)
        self.label = ttk.Label(self,text="Welcome to the BracketApp",font=("Helvetica", 20))
        self.label.configure(anchor="center")
        self.label.grid(column=0,row=0)

        self.sublabel = ttk.Label(self,text="Please choose an option below",font=("Helvetica", 15))
        self.sublabel.configure(anchor="center")
        self.sublabel.grid(column=0,row=1)
        self.new_button = ttk.Button(self, text="New Tournament", command=self.new_tournament)
        self.new_button.grid(column=0,row=2)

        self.load_button = ttk.Button(self, text="Load Tournament", command=self.load_tournament)
        self.load_button.grid(column=0,row=3)

        self.empty = ttk.Label(self,text=" ",font=("Helvetica", 15))
        self.empty.grid(column=0,row=5)

        self.credit = ttk.Label(self,text="Created by Bennett Winnicky-Lewis, produced for KMSC Law LLP",font=("Helvetica", 15))
        self.credit.grid(column=0,row=6)

    def new_tournament(self):
        self.clear_frame()
        new_page = NewTournament(self.master)


    def load_tournament(self):
        self.clear_frame()
        load_page = LoadTournament(self.master)
    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    

class NewTournament(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        # self.button_bonus = ttk.Button(self, text="Bonuses", command=popup_bonus)
        self.grid(column=0,row=0)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)

        self.label = ttk.Label(self,text="Set Tournament Name",font=("Helvetica", 20))
        self.label.configure(anchor="center")

        self.label.grid(column=1,row=0)



        self.entry = ttk.Entry(self)
        self.entry.grid(row=1,column=1,sticky='ew')
        # self.entry.rowconfigure(0,weight=1)

        self.next_button = ttk.Button(self, text="Next", command=self.read_entry)
        self.next_button.grid(column=2,row=1)

        self.entry.bind("<Return>",self.read_entry)

        self.back_button = tk.Button(self,text="Back",command=self.go_back,font=("Helvetica",15))
        self.back_button.grid(column=0,row=0,sticky='nw')
        self.back_button.configure(anchor="nw")

    def go_back(self):
        self.clear_frame()
        name_frame = StartPage(self.master)
    def read_entry(self,_event=None):
        text = self.entry.get()
        if text:
            self.entry.delete(0,tk.END)
            self.master.tourn_name = text
            self.master.name_tourn()
            self.clear_frame()
            self.master.title(text)
            enter_team_page = EnterTeams(self.master)


    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


class LoadTournament(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.grid(column=0,row=0)
        self.label = ttk.Label(self,text="Select Tournament File",font=("Helvetica", 20))
        self.label.configure(anchor="center")
        self.label.grid(column=1,row=0)

        # self.sublabel = ttk.Label(self,text="Default save is what you named the tournament",font=("Helvetica", 15))
        # self.sublabel.configure(anchor="center")
        # self.sublabel.grid(column=0,row=1)

        # self.filename = tk.file.askopenfilename()


        self.open_button = ttk.Button(
        self,
        text='Open a File',
        command=self.file_select)
        self.open_button.grid(row=2,column=1)
       
        self.back_button = tk.Button(self,text="Back",command=self.go_back,font=("Helvetica",15))
        self.back_button.grid(column=0,row=0,sticky='nw')
        self.back_button.configure(anchor="nw")

    def go_back(self):
        self.clear_frame()
        name_frame = StartPage(self.master)

    def file_select(self):
        filetypes = filetypes=(("CSV Files", "*.csv"), ("All files", "*.*")
    )

        filename = fd.askopenfilename(
        title='Open a file',
        initialdir='./',
        filetypes=filetypes)
        self.loading_tourn = self.load_tourn(filename)
        
    def load_tourn(self,filename):
        if filename:
            file = filename.split('/')[-1]
            name = file[:-4]
            try:
                self.master.tourn_name = name
                self.master.name_tourn()
                self.master.tournament.change_tourn_name(name)
                self.master.tournament.import_tournament(filename)
                self.clear_frame()
                round_robin_page = RoundRobin(self.master)

            except:
                error_label = tk.Label(self,text="PLEASE SELECT A VALID FILE",font=("Helvetica", 12),foreground='red')
                error_label.configure(anchor="center")
                error_label.grid(column=1,row=2)
                
                self.after(2000, error_label.destroy)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


class EnterTeams(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.grid(column=0,row=0)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.label = ttk.Label(self,text="Enter Team Names",font=("Helvetica", 20))
        self.label.configure(anchor="center")

        self.label.grid(column=1,row=0)

        self.entry = ttk.Entry(self)
        self.entry.grid(row=1,column=1,sticky='ew')
        self.entry.bind("<Return>",self.add_team)

        # self.entry.rowconfigure(0,weight=1)

        self.enter_button = ttk.Button(self, text="Add Team", command=self.add_team)
        # self.enter_button.grid(column=1,row=1)
        self.enter_button.grid(column=1,row=2)
        
        # self.frame_2 = tk.Frame(parent)
        # self.frame_2.grid(column=1,row=0)

        
        self.team_label = ttk.Label(self,text="Teams",font=("Helvetica", 20))
        self.team_label.grid(row=0, column=3, sticky="nsew")
        self.team_label.configure(anchor="center")
        self.team_label.columnconfigure(3,weight=1)


        self.text_list = tk.Listbox(self)
        self.text_list.grid(row=1, column=3, sticky="nsew",rowspan=4)
        self.text_list.rowconfigure(2,weight=1)
        self.text_list.columnconfigure(3,weight=1)

        # initializing the text list with team names if they exist
        if len(self.master.tournament.team_names)>0:
            for name in self.master.tournament.team_names:
                self.text_list.insert(tk.END,name)
        # Create vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text_list.yview)
        self.scrollbar.grid(row=1, column=4, sticky="ns",rowspan=4)

        self.text_list.config(yscrollcommand=self.scrollbar.set)

        self.remove_button = tk.Button(self,text="Remove Selected Team",command=self.remove_team)
        self.remove_button.grid(row=6,column=3)

        self.next_button = tk.Button(self,text="Make\nTournament",command=self.create_round_robin,height = 5, width = 10,font=("Helvetica",15),highlightbackground='blue')
        self.next_button.grid(column=1,row=4)

        self.back_button = tk.Button(self,text="Back",command=self.go_back,font=("Helvetica",15))
        self.back_button.grid(column=0,row=0,sticky='nw')
        self.back_button.configure(anchor="nw")

        self.empty_label=tk.Label(self,text="",font=("Helvetica", 15))
        self.empty_label.configure(anchor="center")
        self.empty_label.grid(column=1,row=3)
    def go_back(self):
        self.clear_frame()
        name_frame = NewTournament(self.master)
    def add_team(self,_event=None):
        text = self.entry.get()
        if text:
            if text in self.master.tournament.team_names:
                error_label = tk.Label(self,text="THIS TEAM ALREADY EXISTS",font=("Helvetica", 12),foreground='red')
                error_label.configure(anchor="center")
                error_label.grid(column=1,row=3)
                self.entry.delete(0,tk.END)
                
                self.after(2000, error_label.destroy)

            else:
                self.text_list.insert(tk.END,text)
                self.entry.delete(0,tk.END)
                self.master.tournament.add_team(text)
                # error_label.grid(column=0,row=2)
    def remove_team(self,_event=None):
        SelectList = self.text_list.curselection()
        for i in SelectList:
            self.master.tournament.remove_team(self.text_list.get(i))
            self.text_list.delete(i)
    def create_round_robin(self,_event=None):
        self.clear_frame()
        round_robin_page = RoundRobin(self.master)

    def remove_label(self,label):
        label.destroy()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


class RoundRobin(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.master.geometry("1200x500")
        # Reconfiguring columns and rows
        self.master.columnconfigure(0,weight=1)
        self.master.columnconfigure(1,weight=1)

        self.master.rowconfigure(0,weight=1)
        self.master.rowconfigure(1,weight=1)

        # Making 4 differnt frames to add to    
        
        self.button_frame = ttk.Frame(parent)
        self.button_frame.grid(column=0,row=0)
        # self.button_frame.columnconfigure(0,weight=1)
        # self.button_frame.rowconfigure(0,weight=1)


        self.table_frame = ttk.Frame(parent)
        self.table_frame.grid(column=0,row=1,columnspan=2,sticky='nsew')

        self.table_frame.columnconfigure(0,weight=1)
        self.table_frame.columnconfigure(1,weight=1)

        self.table_frame.rowconfigure(0,weight=0)
        self.table_frame.rowconfigure(1,weight=1)


        self.games_frame = ttk.Frame(parent)
        self.games_frame.grid(column=1,row=0,sticky='ew')
        self.games_frame.columnconfigure(0,weight=1)
        self.games_frame.rowconfigure(0,weight=1)
        self.games_frame.columnconfigure(1,weight=1)
        self.games_frame.rowconfigure(1,weight=1)

        # self.modify_frame = ttk.Frame(parent)
        # self.modify_frame.grid(column=0,row=1)
        # self.modify_frame.columnconfigure(1,weight=1)
        # self.modify_frame.rowconfigure(1,weight=1)

        # self.all_frames = [self.button_frame,self.table_frame,self.games_frame,self,self.modify_frame]

        # Adding buttons to the button frames
        self.add_game_button = tk.Button(self.button_frame,text='Add Game',font=("Helvetica", 25),command=self.add_game)
        self.add_game_button.grid(row=0,column=0)

        self.create_bracket_button = tk.Button(self.button_frame,text='Continue to knockout round',font=("Helvetica", 25),command=self.create_bracket)
        self.create_bracket_button.grid(row=0,column=1)

        # Adding the buttons to modify the tournament
        self.add_remove_team_button = tk.Button(self.button_frame,text='Add/Remove Teams',command=self.modify_team,font=("Helvetica", 15))
        self.add_remove_team_button.grid(row=1,column=0)

        self.remove_game = tk.Button(self.button_frame,text='Remove Games',command=self.remove_game_command,font=("Helvetica", 15))
        self.remove_game.grid(row=1,column=1)

        self.save_tourn_button = tk.Button(self.button_frame,text='Save Tournament',command=self.save_tourn,font=("Helvetica", 12))
        self.save_tourn_button.grid(row=2,column=0)

        self.change_point_dist_button = tk.Button(self.button_frame,text='Change Point Distribution',command=self.change_point_dist,font=("Helvetica", 12))
        self.change_point_dist_button.grid(row=2,column=1)

        # self.load_tourn_button = tk.Button(self.button_frame,text='Load Tournament',command=self.load_tourn,font=("Helvetica", 10))
        # self.load_tourn_button.grid(row=3,column=0)

        # Adding the rank table
        self.ranks = self.add_rank_table()

        self.games = self.add_games_table(self.games_frame)
        # Adding the games table
    # def load_tourn(self):
    #     self.clear_rr()

    #     load_tourn = LoadTournament(self.master)
    def remove_game_command(self):
        self.popup = tk.Toplevel()
        self.popup.title("Remove Game")
        self.popup.geometry("700x350")
        self.popup.columnconfigure(0,weight=1)

        self.popup.rowconfigure(0,weight=1)

        self.pop_frame_1 = ttk.Frame(self.popup)
        self.pop_frame_1.grid(row=0,column=0)
        self.pop_frame_1.columnconfigure(0,weight=1)
        self.pop_frame_1.rowconfigure(0,weight=1)

        self.pop_frame_2 = ttk.Frame(self.popup)
        self.pop_frame_2.grid(row=0,column=1)
        self.pop_frame_2.columnconfigure(0,weight=1)
        self.pop_frame_2.rowconfigure(0,weight=1)

        label = tk.Label(self.pop_frame_1,text='Select a Game',font=('Times New Roman',25))
        label.grid(row=0,column=0)
        self.remove_button = tk.Button(self.pop_frame_1,command=self.take_out_game,text='Remove Game',font=('Times New Roman',15))
        self.remove_button.grid(row=1,column=0)

        self.game_table_pop = self.add_games_table(self.pop_frame_2)
    def take_out_game(self,_event=None):
        t = self.game_table_pop.selection()
        if len(t)>0:
            for point in t:
                id = self.game_table_pop.item(point)['values'][0]
                try:
                    self.master.tournament.remove_game(id)
                except:
                    print("Error")
            self.update_tables()
            self.popup.destroy()
            

    def change_point_dist(self):
        self.popup = tk.Toplevel()
        self.popup.title("Add Game")
        
        self.pop_frame = ttk.Frame(self.popup)
        self.pop_frame.grid(row=0,column=0)
        self.pop_frame.columnconfigure(0,weight=1)
        self.pop_frame.rowconfigure(0,weight=1)
        ttk.Label(self.pop_frame, text = f"Change Point Distribution of {self.master.tourn_name}", 
          font = ("Times New Roman", 20)).grid(row = 0, column = 1)

        # Labels
        label_1 = ttk.Label(self.pop_frame, text = "Points for a Win (default=2)",
                font = ("Times New Roman", 15)).grid(column = 0,
                row = 1, padx = 10, pady = 5)
        label_2 = ttk.Label(self.pop_frame, text = "Points for a Loss (default=0)",
                font = ("Times New Roman", 15)).grid(column = 1,
                row = 1, padx = 10, pady = 5)
        label_1_score = ttk.Label(self.pop_frame, text = "Points for a Draw (default=1)",
                font = ("Times New Roman", 15)).grid(column = 2,
                row = 1, padx = 10, pady = 5)
        
        # Creating score field 1
        self.entry_win = tk.Entry(self.pop_frame,width=3)
        self.entry_win.grid(row=2,column=0)
        # Creating score field 2
        self.entry_loss = tk.Entry(self.pop_frame,width=3)
        self.entry_loss.grid(row=2,column=1)

        # Creating score field 3
        self.entry_draw = tk.Entry(self.pop_frame,width=3)
        self.entry_draw.grid(row=2,column=2)
        # Add Game button
        self.change_button = tk.Button(self.pop_frame,text='Done',command=self.done_point_dist,font = ("Times New Roman", 15))
        self.change_button.grid(row=3,column=1)
    def done_point_dist(self):
        try:
            point_dist = [float(self.entry_win.get()),float(self.entry_loss.get()),float(self.entry_draw.get())]
            self.master.tournament.change_point_dist(point_dist)
            self.update_tables()
            self.popup.destroy()
        except:
            error_label = ttk.Label(self.pop_frame,text='PLEASE ENTER VALID NUMBERS',font=("Helvetica", 12),foreground='red')
            error_label.configure(anchor="center")
            error_label.grid(column=1,row=4)
            self.pop_frame.after(2000, error_label.destroy)
    def add_rank_table(self):
        label = tk.Label(self.table_frame,text='Team Ranking',font =("Helvetica", 15) )
        label.grid(row=0,column=0)
        rank_list = self.master.tournament.return_standings_array()
        widths = [50,150,50,100,50,50,50,50,50,50]
        
        header_names = ('Rank', 'Team', 'Points','Games Played', 'Wins', 'Losses', 'Draws', 'Points For', 'Points Against', 'Point Diff')
        self.rank_table = ttk.Treeview(self.table_frame,columns=header_names)
        self.rank_table.grid(row=1,column=0,sticky='nsew')
        self.rank_table['show'] = 'headings'
        
        for name in header_names:
            self.rank_table.heading(name, text=name)
        self.vscrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.rank_table.yview)
        self.vscrollbar.grid(row=1, column=1, sticky="nsw")

        self.hscrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.rank_table.xview)
        self.hscrollbar.grid(row=2, column=0, sticky="new")

        self.rank_table.configure(yscrollcommand=self.vscrollbar.set,xscrollcommand=self.hscrollbar)
        self.rank_table.rowconfigure(0,weight=1)
        self.rank_table.columnconfigure(1,weight=1)
        self.rank_table.rowconfigure(1,weight=1)
        self.rank_table.columnconfigure(2,weight=0)
        self.rank_table.rowconfigure(2,weight=0)
        for i,width in list(enumerate(widths)):
            self.rank_table.column(str(i), width = width, anchor ='c') 
        for team_stats in rank_list:
            self.rank_table.insert("", tk.END, values=(team_stats))
    def add_games_table(self,parent):
        label = tk.Label(self.games_frame,text='Games List',font =("Helvetica", 15) )
        label.grid(row=0,column=0)

        game_list = self.master.tournament.return_game_stats()[::-1]
        if len(game_list)==0:
            game_list = [['No','Games','Have','Been','Played']]
        widths = [50,150,75,150,75]
        
        header_names =('Game ID','Team 1','Team 1 Score','Team 2','Team 2 Score')
        self.game_table = ttk.Treeview(parent,columns=header_names)
        self.game_table.grid(row=1,column=0,sticky='nsew')
        for name in header_names:
            self.game_table.heading(name, text=name)

        self.game_table['show'] = 'headings'
        self.vscrollbar_game = ttk.Scrollbar(parent, orient="vertical", command=self.game_table.yview)
        self.vscrollbar_game.grid(row=1, column=1, sticky="nsw")

        self.hscrollbar_game = ttk.Scrollbar(parent, orient="horizontal", command=self.game_table.xview)
        self.hscrollbar_game.grid(row=2, column=0, sticky="new")

        self.game_table.configure(yscrollcommand=self.vscrollbar_game.set,xscrollcommand=self.hscrollbar_game)

        for i,width in list(enumerate(widths)):
            self.game_table.column(str(i), width = width, anchor ='c') 
        for stats in game_list:
            self.game_table.insert("", tk.END, values=(stats))
        return self.game_table
    def update_tables(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.add_rank_table()
        for widget in self.games_frame.winfo_children():
            widget.destroy()
        self.add_games_table(self.games_frame)
    def modify_team(self,_event=None):
        self.clear_rr()
        self.modify_team_frame = EnterTeams(self.master)
    def save_tourn(self):
        filetypes = filetypes=(("CSV Files", "*.csv"), ("All files", "*.*"))

        filename = fd.asksaveasfilename(
        title='Save as a CSV file',
        initialdir='./',
        filetypes=filetypes)
        if filename:
            print(filename)
            # error_label = ttk.Label(self.button_frame,text='PLEASE SAVE AS .CSV',font=("Helvetica", 12),foreground='red')
            # error_label.configure(anchor="center")
            # error_label.grid(column=0,row=3)
            # self.button_frame.after(2000, error_label.destroy)
            # else:
            try:
                self.master.tournament.export_tournament(filename)
                good_label = ttk.Label(self.button_frame,text='Saved Tournament',font=("Helvetica", 12),foreground='green')
                good_label.configure(anchor="center")
                good_label.grid(column=0,row=3)
                self.button_frame.after(2000, good_label.destroy)
            except:
                error_label = ttk.Label(self.button_frame,text='Error saving tournament.\nPlease try again.',font=("Helvetica", 12),foreground='red')
                error_label.configure(anchor="center")
                error_label.grid(column=0,row=3)
                self.button_frame.after(2000, error_label.destroy)
    def add_game(self,_event=None):
        self.popup = tk.Toplevel()
        self.popup.title("Add Game")
        
        self.pop_frame = ttk.Frame(self.popup)
        self.pop_frame.grid(row=0,column=0)
        self.pop_frame.columnconfigure(0,weight=1)
        self.pop_frame.rowconfigure(0,weight=1)
        ttk.Label(self.pop_frame, text = f"Add Game to {self.master.tourn_name}", 
        #   background = 'green', foreground ="white", 
          font = ("Times New Roman", 20)).grid(row = 0, column = 2)

        # Labels
        label_1 = ttk.Label(self.pop_frame, text = "Select Team 1:",
                font = ("Times New Roman", 15)).grid(column = 0,
                row = 2, padx = 10, pady = 5)
        label_2 = ttk.Label(self.pop_frame, text = "Select Team 2:",
                font = ("Times New Roman", 15)).grid(column = 3,
                row = 2, padx = 10, pady = 5)
        label_1_score = ttk.Label(self.pop_frame, text = "Team 1 Score:",
                font = ("Times New Roman", 15)).grid(column = 0,
                row = 3, padx = 10, pady = 5)
        label_2_score = ttk.Label(self.pop_frame, text = "Team 2 Score:",
                font = ("Times New Roman", 15)).grid(column = 3,
                row = 3, padx = 10, pady = 5)
        # Creating dropdown 1
        self.n_1 = tk.StringVar()
        self.team_1_choice = ttk.Combobox(self.pop_frame, width = 10, textvariable = self.n_1)
        self.team_1_choice['values'] = self.master.tournament.team_names
        self.team_1_choice.grid(column = 1, row = 2)
        self.team_1_choice.columnconfigure(1,weight=1)

        self.team_1_choice.current()
        # Creating dropdown 2
        self.n_2 = tk.StringVar()
        self.team_2_choice = ttk.Combobox(self.pop_frame, width = 10, textvariable = self.n_2)
        self.team_2_choice['values'] = self.master.tournament.team_names
        self.team_2_choice.grid(column = 4, row = 2)
        self.team_2_choice.columnconfigure(4,weight=1)
        self.team_2_choice.current()
        # Creating score field 1
        self.entry_1 = tk.Entry(self.pop_frame,width=3)
        self.entry_1.grid(row=3,column=1)
        # Creating score field 2
        self.entry_2 = tk.Entry(self.pop_frame,width=3)
        self.entry_2.grid(row=3,column=4)

        # Add Game button
        self.add_button = ttk.Button(self.pop_frame,text='Add Game',command=self.execute_game)
        self.add_button.grid(row=4,column=2)
    def execute_game(self,_execute=None):
        if self.team_1_choice.get()==self.team_2_choice.get():
            error_label = tk.Label(self.pop_frame,text="TEAMS CANNOT \nPLAY THEMSELVES",font=("Helvetica", 12),foreground='red')
            error_label.configure(anchor="center")
            error_label.grid(column=2,row=2)
            self.pop_frame.after(2000, error_label.destroy)
        else:
            try:
                self.master.tournament.add_game(self.n_1.get(),self.n_2.get(),int(self.entry_1.get()),int(self.entry_2.get()))
                for widget in self.popup.winfo_children():
                    widget.destroy()
                self.update_tables()
                self.popup.destroy()
            except:
                error_label = tk.Label(self.pop_frame,text="Please put a whole number\nfor the scores",font=("Helvetica", 12),foreground='red')
                error_label.configure(anchor="center")
                error_label.grid(column=2,row=2)
                self.pop_frame.after(2000, error_label.destroy)
    
    def change_team_name(self,_event=None):
        self.popup = tk.Toplevel()
        self.popup.title = "Change Team Name"


    def create_bracket(self,event=None):
        self.popup = tk.Toplevel()
        self.popup.title = "Choose Number of rounds"

        self.pop_frame_1 = tk.Frame(self.popup)
        self.pop_frame_1.grid(row=0,column=0)

        self.pop_frame_2 = tk.Frame(self.popup)
        self.pop_frame_2.grid(row=1,column=0)

        label = tk.Label(self.pop_frame_1,text='Select the number\nof rounds to create',font=('Helvetica',20))
        label.grid(row=0,column=2)
        
        button1 = tk.Button(self.pop_frame_2,text='1',font=('Helvetica',15),command=self.make_1)
        button1.grid(row=1,column=0)

        button2 = tk.Button(self.pop_frame_2,text='2',font=('Helvetica',15),command=self.make_2)
        button2.grid(row=1,column=1)

        button3 = tk.Button(self.pop_frame_2,text='3',font=('Helvetica',15),command=self.make_3)
        button3.grid(row=1,column=2)

        button4 = tk.Button(self.pop_frame_2,text='4',font=('Helvetica',15),command=self.make_4)
        button4.grid(row=1,column=3)


    def make_1(self):
        self.make_brack(1)        
    def make_2(self):
        self.make_brack(2)
    def make_3(self):
        self.make_brack(3)
    def make_4(self):
        self.make_brack(4)

    def make_brack(self,num_rounds):
        num_teams = 2**num_rounds
        if num_teams>len(self.master.tournament.team_names):
            error_label = tk.Label(self.pop_frame_2,text="Not enough teams for this selection",font=("Helvetica", 12),foreground='red')
            error_label.configure(anchor="center")
            error_label.grid(column=2,row=2)
            self.pop_frame_2.after(2000, error_label.destroy)
        else:
            self.clear_rr()
            self.bracket =Bracket(self.master,num_rounds)

    def clear_rr(self):
        for widget in self.master.winfo_children():
            widget.destroy()


class Bracket(ttk.Frame):
    def __init__(self,parent,num_rounds=1):
        super().__init__(parent)
        self.master.geometry("1200x650")
        button_width=15
        button_height=3
        self.frame_1 = ttk.Frame(parent)
        self.frame_1.grid(row=0,column=0)

        self.header = tk.Label(self.frame_1,text=f'Knockout Rounds for {self.master.tournament.name}',font=('Helvetica',25))
        self.header.grid(row=0,column=1)
        self.empty = tk.Label(self.frame_1,text='')
        self.empty.grid(row=0,column=2)
        self.back_button = tk.Button(self.frame_1,text='Back to Round Robin',command=self.back_to_rr,font=('Helvetica',15))
        self.back_button.grid(row=0,column=0)
        self.back_button = tk.Button(self.frame_1,text='Reset Bracket',command=self.reset,font=('Helvetica',15))
        self.back_button.grid(row=1,column=0)

        self.brack_tournament = Tournament(self.master.tournament.name+' Bracket')
        for name in self.master.tournament.team_names:
            self.brack_tournament.add_team(name)
        self.num_rounds = num_rounds

        self.grid(column=0,row=1)
 
        self.max_col = 2*(num_rounds)-1
        for i in range(self.max_col):
            self.columnconfigure(i,weight=1)
            self.rowconfigure(i,weight=1)

        self.mid_col = int(self.max_col/2)+1
        if self.num_rounds<3:
            self.mid_rows=2
            if self.num_rounds==1:
                self.empty_1 = tk.Label(self,text=' ',width =button_width,height=button_height)
                self.empty_1.grid(row=self.mid_rows+1,column=self.mid_col)
                self.empty_2 = tk.Label(self,text=' ',width =button_width,height=button_height)
                self.empty_2.grid(row=self.mid_rows+2,column=self.mid_col)
        else:
            self.mid_rows = int(self.max_col/2)+1

        self.table = self.master.tournament.return_standings_array()
        self.rank = [self.table[i][0] for i in range(len(self.table))]
        self.teams = [self.table[i][1] for i in range(len(self.table))]
        self.teams_rank = [self.table[i][1]+f' ({self.rank[i]})' for i in range(len(self.table))]
        config_brack = self.configure_bracket()
    def configure_bracket(self):
        fonts = ('Helvetica', 20)
        button_width=15
        button_height=3
        if self.num_rounds>3:
        # Round of 16
            self.match_1_1 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_1_1,self.match_2_1,add_top=True))
            self.match_1_1.grid(row=self.mid_rows-3,column=self.mid_col-3)
            self.match_1_2 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_1_2,self.match_2_1,add_top=False))
            self.match_1_2.grid(row=self.mid_rows-1,column=self.mid_col-3)
            self.match_1_3 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_1_3,self.match_2_2,add_top=True))
            self.match_1_3.grid(row=self.mid_rows+1,column=self.mid_col-3)
            self.match_1_4 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_1_4,self.match_2_2,add_top=False))
            self.match_1_4.grid(row=self.mid_rows+3,column=self.mid_col-3)
            self.match_1_5 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_1_5,self.match_2_3,add_top=True))
            self.match_1_5.grid(row=self.mid_rows-3,column=self.mid_col+3)
            self.match_1_6 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_1_6,self.match_2_3,add_top=False))
            self.match_1_6.grid(row=self.mid_rows-1,column=self.mid_col+3)
            self.match_1_7 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_1_7,self.match_2_4,add_top=True))
            self.match_1_7.grid(row=self.mid_rows+1,column=self.mid_col+3)
            self.match_1_8 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_1_8,self.match_2_4,add_top=False))
            self.match_1_8.grid(row=self.mid_rows+3,column=self.mid_col+3)
        # Quarter Finals
        if self.num_rounds>2:
            self.match_2_1 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_2_1,self.match_3_1,add_top=True))
            self.match_2_1.grid(row=self.mid_rows-2,column=self.mid_col-2)
            self.match_2_2 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_2_2,self.match_3_1,add_top=False))
            self.match_2_2.grid(row=self.mid_rows+2,column=self.mid_col-2)
            self.match_2_3 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_2_3,self.match_3_2,add_top=True))
            self.match_2_3.grid(row=self.mid_rows-2,column=self.mid_col+2)
            self.match_2_4 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_2_4,self.match_3_2,add_top=False))
            self.match_2_4.grid(row=self.mid_rows+2,column=self.mid_col+2)
        # Semi Finals
        if self.num_rounds>1:
            self.match_3_1 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_3_1,self.match_4_1,add_top=True,semis=True))
            self.match_3_1.grid(row=self.mid_rows,column=self.mid_col-1)
            self.match_3_2 = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_3_2,self.match_4_1,add_top=False,semis=True))
            self.match_3_2.grid(row=self.mid_rows,column=self.mid_col+1)
            # 3rd place
            self.match_3rd = tk.Button(self,text="\nvs\n",width=button_width,height=button_height,font=fonts,command=lambda: self.add_knockout_game(self.match_3rd,self.match_3rd,add_top=False,third_place=True))
            self.match_3rd.grid(row=self.mid_rows+1,column=self.mid_col)
            self.third_place_label = tk.Label(self,text="Third Place:\n",width=button_width,height=button_height,font=('Helvetica', 20))
            self.third_place_label.grid(row=self.mid_rows+2,column=self.mid_col)
        # Finals
        self.winner_label = tk.Label(self,text="Winner:\n",font=('Helvetica', 25),width=button_width,height=button_height)
        self.winner_label.grid(row=self.mid_rows-2,column=self.mid_col)
        self.second_place_label = tk.Label(self,text="Second Place:\n",width=button_width,height=button_height,font=('Helvetica', 20))
        self.second_place_label.grid(row=self.mid_rows-1,column=self.mid_col)

        self.match_4_1 = tk.Button(self,text="\nvs\n",font=fonts,width=button_width,height=button_height,command=lambda: self.add_knockout_game(self.match_4_1,self.match_4_1,add_top=False,finals=True))
        self.match_4_1.grid(row=self.mid_rows,column=self.mid_col)
        if self.num_rounds==4:
            self.match_1_1.config(text=self.teams_rank[0]+self.match_1_1.cget('text')+self.teams_rank[15])
            self.match_1_2.config(text=self.teams_rank[7]+self.match_1_2.cget('text')+self.teams_rank[8])
            self.match_1_3.config(text=self.teams_rank[4]+self.match_1_3.cget('text')+self.teams_rank[11])
            self.match_1_4.config(text=self.teams_rank[3]+self.match_1_4.cget('text')+self.teams_rank[12])

            self.match_1_5.config(text=self.teams_rank[1]+self.match_1_5.cget('text')+self.teams_rank[14])
            self.match_1_6.config(text=self.teams_rank[6]+self.match_1_6.cget('text')+self.teams_rank[9])
            self.match_1_7.config(text=self.teams_rank[5]+self.match_1_7.cget('text')+self.teams_rank[10])
            self.match_1_8.config(text=self.teams_rank[2]+self.match_1_8.cget('text')+self.teams_rank[13])

        if self.num_rounds==3:
            self.match_2_1.config(text=self.teams_rank[0]+self.match_2_1.cget('text')+self.teams_rank[7])
            self.match_2_2.config(text=self.teams_rank[3]+self.match_2_2.cget('text')+self.teams_rank[4])
            self.match_2_3.config(text=self.teams_rank[1]+self.match_2_3.cget('text')+self.teams_rank[6])
            self.match_2_4.config(text=self.teams_rank[2]+self.match_2_4.cget('text')+self.teams_rank[5])

        if self.num_rounds==2:
            self.match_3_1.config(text=self.teams_rank[0]+self.match_3_1.cget('text')+self.teams_rank[3])
            self.match_3_2.config(text=self.teams_rank[1]+self.match_3_2.cget('text')+self.teams_rank[2])

        if self.num_rounds==1:
            self.match_4_1.config(text=self.teams_rank[0]+self.match_4_1.cget('text')+self.teams_rank[1])
        
    def add_knockout_game(self,start_widget,win_widget,add_top,semis=False,finals=False,third_place=False):
        try:
            widget_text = start_widget.cget('text').split('\n')
            ranks = [self.get_rank(widget_text[0]),self.get_rank(widget_text[-1])]
            fonts = ("Times New Roman", 15)
            self.team_1_choice = self.teams[ranks[0]-1]
            self.team_2_choice = self.teams[ranks[1]-1]

            self.popup = tk.Toplevel()
            self.popup.title("Knockout Game")
            
            self.pop_frame = ttk.Frame(self.popup)
            self.pop_frame.grid(row=0,column=0)
            self.pop_frame.columnconfigure(0,weight=1)
            self.pop_frame.rowconfigure(0,weight=1)
            ttk.Label(self.pop_frame, text = f"Add Knockout Game to {self.master.tourn_name}", 
            #   background = 'green', foreground ="white", 
            font = ("Times New Roman", 20)).grid(row = 0, column = 2)

            # Labels
            label_1 = ttk.Label(self.pop_frame, text = self.teams_rank[ranks[0]-1],
                    font = fonts).grid(column = 0,
                    row = 2, padx = 10, pady = 5)
            label_2 = ttk.Label(self.pop_frame, text = self.teams_rank[ranks[1]-1],
                    font = fonts).grid(column = 3,
                    row = 2, padx = 10, pady = 5)
            label_1_score = ttk.Label(self.pop_frame, text = "Score:",
                    font = fonts).grid(column = 0,
                    row = 3, padx = 10, pady = 5)
            label_2_score = ttk.Label(self.pop_frame, text = "Score:",
                    font = fonts).grid(column = 3,
                    row = 3, padx = 10, pady = 5)

            # Creating score field 1
            self.entry_1 = tk.Entry(self.pop_frame,width=3)
            self.entry_1.grid(row=3,column=1)
            # Creating score field 2
            self.entry_2 = tk.Entry(self.pop_frame,width=3)
            self.entry_2.grid(row=3,column=4)

            # Add Game button
            self.add_button = tk.Button(self.pop_frame,text='Add Game',command=lambda: self.add_match(ranks,start_widget,win_widget,add_top,semis=semis,finals=finals,third_place=third_place),font=fonts)
            self.add_button.grid(row=4,column=2)            
        except:
            error_label = tk.Label(self,text="Not enough teams have \nqualified for this game",font=("Helvetica", 15),foreground='red')
            error_label.configure(anchor="center")
            error_label.grid(column=self.mid_col,row=self.mid_rows)
            self.after(2000, error_label.destroy) 

    def add_match(self,ranks,start_widget,win_widget,add_top,semis=False,finals=False,third_place=False):
        team_1 = self.teams[ranks[0]-1]; team_2 = self.teams[ranks[1]-1]
        try:
            score_1 = int(self.entry_1.get()); score_2 = int(self.entry_2.get())
            if score_1>score_2:
                win_team = ranks[0]
                lose_team = ranks[1]
            elif score_1<score_2:
                win_team = ranks[1]
                lose_team = ranks[0]
            elif score_1==score_2:
                error_label = tk.Label(self.pop_frame,text="NO TIES ALLOWED IN KNOCKOUTS",font=("Helvetica", 12),foreground='red')
                error_label.configure(anchor="center")
                error_label.grid(column=2,row=2)
                self.pop_frame.after(2000, error_label.destroy)
            if score_1!=score_2:
                try:
                    start_widget.configure(command=self.game_played)
                    self.add_scores([score_1,score_2],start_widget)
                    if not finals or third_place:
                        self.brack_tournament.add_game(team_1,team_2,score_1,score_2)
                        self.popup.destroy()
                        if add_top:
                            self.add_top(self.teams_rank[win_team-1],win_widget)
                        else:
                            self.add_bot(self.teams_rank[win_team-1],win_widget)
                    else:
                        if finals:
                            self.add_bot(self.teams_rank[win_team-1],self.winner_label)
                            self.add_bot(self.teams_rank[lose_team-1],self.second_place_label)
                        if third_place:
                            self.add_bot(self.teams_rank[win_team-1],self.third_place_label)
                            self.popup.destroy()

                except:
                    error_label = tk.Label(self.pop_frame,text="ERROR",font=("Helvetica", 12),foreground='red')
                    error_label.configure(anchor="center")
                    error_label.grid(column=2,row=2)
                    self.pop_frame.after(2000, error_label.destroy)
            if semis:
                if add_top:
                    self.add_top(self.teams_rank[lose_team-1],self.match_3rd)
                else:
                    self.add_bot(self.teams_rank[lose_team-1],self.match_3rd)

        except:
            error_label = tk.Label(self.pop_frame,text="PLEASE INSERT VALID SCORES",font=("Helvetica", 12),foreground='red')
            error_label.configure(anchor="center")
            error_label.grid(column=2,row=2)
            self.pop_frame.after(2000, error_label.destroy)

    def game_played(self):
        error_label = tk.Label(self,text="This game has \nalready been played",font=("Helvetica", 15),foreground='red')
        error_label.configure(anchor="center")
        error_label.grid(column=self.mid_col,row=self.mid_rows)
        self.after(2000, error_label.destroy) 
    def add_top(self,add_text,widget):
        old_text = widget.cget('text')
        widget.config(text =add_text+old_text)
    def add_bot(self,add_text,widget):
        old_text = widget.cget('text')
        widget.config(text = old_text+add_text)
    def add_scores(self,scores,widget):
        old_text = widget.cget('text')
        split_text = old_text.split('\n')
        new_text = split_text[0] + f" - {scores[0]}\n"+split_text[1]+'\n'+split_text[2]+f" - {scores[1]}"
        widget.config(text=new_text)

    def get_rank(self,team_rank):
        return int(team_rank.split(')')[-2].split(('('))[-1])
    def get_name(self,team_rank):
        return team_rank.split('(')[-2][:-1]
    def back_to_rr(self):
        self.clear_bracket()
        rr=RoundRobin(self.master)
    def reset(self):
        self.clear_bracket()
        brack = Bracket(self.master,num_rounds=self.num_rounds)
    def clear_bracket(self):
        self.frame_1.destroy()
        for frame in self.winfo_children():
            frame.destroy()

app = Application()

# frame = AddFrame(app)

# test = StartPage(frame)
# test = StartPage()


app.mainloop()

# frm = ttk.Frame(app)
# frm.grid(row=0,column=0,sticky='nsew')

# lbl = ttk.Label(frm,text="Test")
# lbl.grid(row=0,column=1)
# app.mainloop()

# def on_click():
#     lbl.config(text='This is new label')
# root.title('Bracket App')
# lbl = tk.Label(root,text='Label 1')
# lbl.grid(row=0,column=0)

# btn = tk.Button(root,text='Button 1',command=on_click)
# btn.grid(row=0,column=1)

# root.columnconfigure(0,weight=1)
# root.rowconfigure(0,weight=1)




# def add_to_list(event=None):
#     text = entry.get()
#     if text:
#         text_list.insert(tk.END,text)
#         entry.delete(0,tk.END)


# frm = ttk.Frame(root)
# frm.grid(row=0,column=0,sticky='nsew')
# frm.columnconfigure(0,weight=1)
# frm.rowconfigure(1,weight=1)

# entry = ttk.Entry(frm)
# entry.grid(row=0,column=0,sticky='ew')
# entry.rowconfigure(0,weight=1)

# entry.bind("<Return>",add_to_list)

# entry_btn = ttk.Button(frm, text='Add',command=add_to_list)
# entry_btn.grid(row=0,column=1)

# text_list = tk.Listbox(frm)
# text_list.grid(row=1,column=0,columnspan=2,sticky='nsew')
# text_list.rowconfigure(1,weight=1)
# text_list.columnconfigure(0,weight=1)

# root.mainloop()