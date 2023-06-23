#import tkinter to project
import tkinter as tk
from tkinter import ttk, messagebox

class Player:
    def __init__(self, name, scores):
        self.name = name
        self.handicap = sum(scores) - 72  # Calculate the handicap by subtracting 72 from the sum of scores
        self.scores = scores  # Store the individual scores
        self.total_score = sum(scores)  # Calculate the total score by summing the scores
        self.final_score = self.total_score - self.handicap  # Calculate the final score by subtracting the handicap

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.players = {}  #store player objects
        #UI of Golf handicap calc
        self.geometry('800x1600')
        self.title("Golf Handicap and Score Calculator")

        # Create buttons...Add player, load player, and calculate score
        self.add_players_button = tk.Button(self, text="Add Players", command=self.add_player)
        self.add_players_button.pack(pady=10)

        self.load_player_button = tk.Button(self, text="Load Player", command=self.load_player)
        self.load_player_button.pack(pady=10)

        self.calculate_score_button = tk.Button(self, text="Calculate Score", state='disabled', command=self.calculate_score)
        self.calculate_score_button.pack(pady=10)

    def add_player(self):
        #Create a new window for adding players
        self.add_player_window = tk.Toplevel(self)
        #add player UI
        self.add_player_window.geometry('800x800')
        self.add_player_window.title("Add Players")

        #creat grid to allow player to enter in information
        self.entries = []
        for i in range(4):
            row_entries = []
            for j in range(4):
                string_var = tk.StringVar()
                entry = tk.Entry(self.add_player_window, textvariable=string_var)
                entry.grid(row=i, column=j, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)

        self.complete_button = tk.Button(self.add_player_window, text="Complete", state='disabled', command=self.complete_add_player)
        self.complete_button.grid(row=4, column=0, columnspan=4, pady=10)

        #instructions to user adding player infor
        tk.Label(self.add_player_window, text="Write your name in the first column and input your last three scores on a par 72 on the remaining three columns.").grid(row=5, column=0, columnspan=4)

        #allows complete button to be clicked if all fields are filled out
        for row_entries in self.entries:
            for entry in row_entries:
                entry.bind("<KeyRelease>", lambda event: self.update_complete_button_state())

    def update_complete_button_state(self):
        #Enable/disable  "Complete" button based on  all fields being filled
        if all(entry.get() for row_entries in self.entries for entry in row_entries):
            self.complete_button['state'] = 'normal'
        else:
            self.complete_button['state'] = 'disabled'

    def complete_add_player(self):
        #Create Player  and store them
        for row_entries in self.entries:
            name = row_entries[0].get() #get player name from first column
            scores = [int(entry.get()) for entry in row_entries[1:]] #get player scores from next 3 columns
            player = Player(name, scores) #create player with name and scores
            self.players[name] = player

        self.add_player_window.destroy() #close window
        self.calculate_score_button['state'] = 'normal' #enable calculate score button

    def load_player(self):
        #Create a load player window
        self.load_player_window = tk.Toplevel(self)
        #load player UI
        self.load_player_window.geometry('400x200')
        self.load_player_window.title("Load Player")

        #display Select a player to user
        tk.Label(self.load_player_window, text="Select a player:").pack()

        #get list of players that can be selected
        player_names = list(self.players.keys())
        #store selected player name
        self.selected_player = tk.StringVar()
        self.selected_player.set(player_names[0] if player_names else "")

        #dropdown meny with player names
        player_dropdown = ttk.Combobox(self.load_player_window, textvariable=self.selected_player, values=player_names)
        player_dropdown.pack(pady=10)
        #button to load the player that is selected
        load_button = tk.Button(self.load_player_window, text="Load", command=self.complete_load_player)
        load_button.pack()

    def complete_load_player(self):
        #Load player information into the score entries based on the selected player
        selected_player = self.selected_player.get()

        if selected_player:
            player = self.players[selected_player]
            for i, entry in enumerate(self.entries[0][1:]):
                entry.delete(0, tk.END)
                entry.insert(0, str(player.scores[i]))
        #CLOSE add player window
        self.load_player_window.destroy()

#Define how to calculate score
    def calculate_score(self):
        #Create window for entering scores
        self.score_window = tk.Toplevel(self)
        #UI of calculate score
        self.score_window.geometry('700x700')
        self.score_window.title("Enter Scores")

        self.score_entries = []#store score
        self.name_entries = []#store name
        for i in range(19):
            tk.Label(self.score_window, text=f"Hole {i if i > 0 else ''}").grid(row=i, column=0, padx=5, pady=5)
        for j in range(4):
            entry = tk.Entry(self.score_window)
            entry.grid(row=0, column=j+1, padx=5, pady=5)
            self.name_entries.append(entry)
        for i, player in enumerate(self.players.values()): #fill in player names top row
            self.name_entries[i].insert(0, player.name)
        for i in range(1, 19):
            row_entries = []
            for j in range(4):
                entry = tk.Entry(self.score_window)
                entry.grid(row=i, column=j+1)
                row_entries.append(entry)
            self.score_entries.append(row_entries)
        #button to calculate score....disabled at start
        self.calculate_button = tk.Button(self.score_window, text="Calculate", state='disabled', command=self.complete_calculate_score)
        self.calculate_button.grid(row=19, column=0, columnspan=5, pady=10)
        #if all fields are met, caclulate button will be enabled
        for row_entries in self.score_entries:
            for entry in row_entries:
                entry.bind("<KeyRelease>", lambda event: self.update_calculate_button_state())

    def update_calculate_button_state(self):
        #Enable/disable "Calculate" if all fields are filled or not
        if all(entry.get() for row_entries in self.score_entries for entry in row_entries):
            self.calculate_button['state'] = 'normal'
        else:
            self.calculate_button['state'] = 'disabled'

#calculate final and handicap score and dispaly them
    def complete_calculate_score(self):
        #Calculate the score and display the results...if not all rows are filled dispaly warning message
        if not all(entry.get() for row_entries in self.score_entries for entry in row_entries):
            messagebox.showwarning("Warning", "Please fill all fields before calculating the score.")
            return

        for row_entries in self.score_entries:
            for i, entry in enumerate(row_entries):
                #retirece name and score of player
                player = self.players[self.name_entries[i].get()]
                score = int(entry.get())
                #add score to players list of scores
                player.scores.append(score)

        player_results = ""
        for player in self.players.values():
            #add each players anme and total and hadndicapc score to results
            player_results += f"{player.name}: {self.total_score}/{self.final_score}\n"
        #dispaly message with results
        messagebox.showinfo("Golf Score Calculation Complete", player_results)
        self.score_window.destroy() #close window
#end program
if __name__ == "__main__":
    app = Application()
    app.mainloop()
