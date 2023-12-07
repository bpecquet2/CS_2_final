import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class VotingSystemGUI:
    MAX_CANDIDATES: int = 5

    def __init__(self) -> None:
        """Initialize the VotingSystemGUI."""
        self.root = tk.Tk()
        self.root.title("Voting System")

        self.candidates: dict[str, int] = {}
        self.voter_candidates: dict[str, str] = {}  # Maps voters to the candidates they voted for
        self.voter_votes: dict[str, str] = {}  # Maps voters to the candidates they voted for with the count
        self.voted_users = set()  # Keep track of users who have voted

        self.setup_gui()

    def setup_gui(self) -> None:
        """Create GUI widgets for the voting system."""
        # Voting menu
        vote_label = tk.Label(self.root, text="Select an option:")
        vote_label.pack()
        # make vote button
        vote_button = tk.Button(self.root, text="Vote", command=self.vote_menu, width=20, height=2)
        vote_button.pack(pady=10)
        # make exit button
        exit_button = tk.Button(self.root, text="Save/Exit", command=self.exit_program, width=20, height=2)
        exit_button.pack()
        # make pie chart button
        show_pie_chart_button = tk.Button(self.root, text="Show Pie Chart", command=self.show_pie_chart, width=20, height=2)
        show_pie_chart_button.pack(pady=10)
        # make show scores button
        show_scores_button = tk.Button(self.root, text="Show Overall Scores", command=self.show_overall_scores,
                                       width=20, height=2)
        show_scores_button.pack()

        # Frame for candidate buttons
        self.candidate_frame = tk.Frame(self.root)

        # Create buttons for each candidate
        for candidate in self.candidates:
            self.create_candidate_button(candidate)

        # Write-in option
        write_in_button = tk.Button(self.candidate_frame, text="Write-In", command=self.write_in_candidate, width=20, height=2)
        write_in_button.pack(pady=5)

        # Vote tally
        tally_label = tk.Label(self.root, text="Vote Menu:")
        tally_label.pack()

        self.tally_var = tk.StringVar()
        self.update_tally()
        tally_display = tk.Label(self.root, textvariable=self.tally_var, font=("Helvetica", 14))
        tally_display.pack()

    def save_votes_to_excel(self) -> None:
        """Save the votes to an Excel file."""
        data = {"Voter": [], "Candidate": [], "Votes": []}

        for voter, candidate in self.voter_candidates.items():
            data["Voter"].append(voter)
            data["Candidate"].append(candidate)
            data["Votes"].append(self.voter_votes.get(voter, ""))

        df = pd.DataFrame(data)
        df.to_excel("voting_results.xlsx", index=False)

    def get_chosen_candidate(self, user_first_name: str, user_last_name: str) -> str:
        """Get the candidate chosen by the user."""
        user_id = f"{user_first_name.upper()}_{user_last_name.upper()}"
        return simpledialog.askstring("Choose Candidate", f"{user_first_name}, choose a candidate:")

    def create_candidate_button(self, candidate: str) -> None:
        """Create a button for a candidate.

        Args:
            candidate (str): The name of the candidate.
        """
        candidate_button = tk.Button(self.candidate_frame, text=candidate.upper(), command=lambda c=candidate: self.vote_candidate(c), width=20, height=2)
        candidate_button.pack(pady=5)

    def vote_menu(self) -> None:
        """Display candidate buttons when "Vote" button is clicked."""
        # Display candidate buttons when "Vote" button is clicked
        self.candidate_frame.pack()

    def vote_candidate(self, candidate: str) -> None:
        """Vote for a candidate.

        Args:
            candidate (str): The name of the candidate.
        """
        user_first_name, user_last_name = self.get_user_name()

        # Check if both first_name and last_name are empty (user canceled multiple times)
        if not user_first_name and not user_last_name:
            return

        user_id = f"{user_first_name.upper()}_{user_last_name.upper()}"

        if user_id in self.voted_users:
            messagebox.showinfo("Info", "You have already voted. Cannot vote again.")
            return

        # Ensure the candidate is initialized with an integer value
        if candidate not in self.candidates:
            self.candidates[candidate] = 0

        self.voted_users.add(user_id)
        self.voter_candidates[user_id] = candidate  # Track the candidate chosen by the voter
        self.candidates[candidate] += 1  # Increment the vote count

        # Track the vote count for each candidate voted for by the user
        self.voter_votes[user_id] = self.voter_votes.get(user_id, "")
        self.voter_votes[user_id] += f"{candidate}:{self.candidates[candidate]} "

        self.update_tally()

    def write_in_candidate(self) -> None:
        """Handle the write-in candidate option."""
        if len(self.candidates) >= self.MAX_CANDIDATES:
            messagebox.showerror("Error", f"Cannot write in more than {self.MAX_CANDIDATES} candidates.")
            return

        write_in_name = simpledialog.askstring("Write-In Candidate", "Enter the name of your candidate:")
        if not write_in_name:
            messagebox.showerror("Error", "Please enter a name for the write-in candidate.")
            return

        write_in_name_upper = write_in_name.upper()

        if write_in_name_upper in self.candidates:
            messagebox.showerror("Error", f"{write_in_name} already exists. Enter a different name.")
        else:
            # Add the write-in candidate with zero initial votes
            self.candidates[write_in_name_upper] = self.candidates.get(write_in_name_upper, 0)
            # Create a new button for the write-in candidate
            self.create_candidate_button(write_in_name_upper)
            self.update_tally()

    def show_pie_chart(self) -> None:
        """Display a pie chart of the votes in a separate window."""
        # error message if no candidates
        if not any(self.candidates.values()):
            messagebox.showinfo("Info", "Votes must be entered before displaying the pie chart.")
            return

        # Print for debugging
        print("Candidates:", self.candidates)

        # Convert candidate names to uppercase for display labels
        labels = list(self.candidates.keys())  # Use the keys of vote_counts as labels

        # Use the number of votes as values for the pie chart
        values = list(self.candidates.values())

        # make Pie window
        pie_chart_window = tk.Toplevel(self.root)
        pie_chart_window.title("Pie Chart")

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        canvas = FigureCanvasTkAgg(fig, master=pie_chart_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

        canvas.draw()  # Use canvas.draw() instead of plt.show() to display the pie chart in the Tkinter window

    def exit_program(self) -> None:
        """
        Exit the program and display a thank you message.
        """
        total_votes_message = "Thank you for voting! The votes have been recorded."
        messagebox.showinfo("Voting Completed", total_votes_message)

        self.save_votes_to_file()
        self.save_votes_to_excel()
        self.root.destroy()

    def show_overall_scores(self) -> None:
        """Display a window with the overall scores."""
        overall_scores_window = tk.Toplevel(self.root)
        overall_scores_window.title("Overall Scores")

        overall_scores_label = tk.Label(overall_scores_window, text=self.get_current_scores(), font=("Helvetica", 14))
        overall_scores_label.pack()

    def get_current_scores(self) -> str:
        """Get the current scores of each candidate.

        Returns:
            str: The current scores.
        """
        return "\n".join([f'{candidate}: {votes} vote(s)' for candidate, votes in self.candidates.items()])

    def update_tally(self) -> None:
        """Update the vote tally display."""
        self.get_current_tally()

    def get_current_tally(self) -> str:
        """Get the current vote tally.

        Returns:
            str: The current vote tally.
        """
        return "\n".join([f'{candidate}: {votes} votes' for candidate, votes in self.candidates.items()])

    def save_votes_to_file(self) -> None:
        """Save the votes to a file."""
        with open("votes.txt", "w") as file:
            for candidate, votes in self.candidates.items():
                file.write(f"{candidate}: {votes}\n")

    def get_user_name(self) -> tuple[str, str]:
        """Prompt the user for their first and last name."""
        first_name = simpledialog.askstring("Enter Your First Name", "Enter your first name:")

        # Check if first_name is None (Cancel was pressed)
        if first_name is None:
            messagebox.showinfo("Info", "User canceled the operation.")
            return "", ""

        last_name = simpledialog.askstring("Enter Your Last Name", "Enter your last name:")

        # Check if last_name is None (Cancel was pressed)
        if last_name is None:
            messagebox.showinfo("Info", "User canceled the operation.")
            return "", ""

        # Check if both first_name and last_name are non-empty
        if not first_name or not last_name:
            messagebox.showerror("Error", "Please enter both first and last names.")
            return self.get_user_name()
        return first_name, last_name

    def save_user_to_csv(self, first_name: str, last_name: str) -> None:
        """Save user information to a CSV file.

        Args:
            first_name (str): The user's first name.
            last_name (str): The user's last name.
        """
        with open("voter_data.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([first_name, last_name])

    def run(self) -> None:
        """Run the voting system GUI."""
        self.root.geometry("400x600")
        self.root.mainloop()


if __name__ == "__main__":
    voting_system_gui = VotingSystemGUI()
    voting_system_gui.run()

