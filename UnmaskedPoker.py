# SPL log script

import tkinter as tk
from tkinter import filedialog
import re


def extract_players(lines):

    player_names = []
    start_capturing = False

    for line in lines:
        if 'start of hand #1' in line:
            start_capturing = True
        elif start_capturing:
            if '--- pre-flop' in line:
                break
            match = re.match(r'\d+:\s([^()]+)', line)
            # regex to match an integer fol lowed by a colon and then a space capturing everything except parantheses
            if match:
                # player name is obtained from above "match"
                # removing any whitespaces 
                player_name = match.group(1).strip()
                if player_name not in player_names:
                    # only getting unique player names - if name is already found, ignore, else append
                    player_names.append(player_name)

    return player_names

def analyze_poker_stats(file_path, game_stats):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # list of player names
    player_names = extract_players(lines)
    # initializing a dictionary for each player name found above ^
    player_stats = {
        name: {
            'hands_won': 0,
            'times_folded': 0,
            'times_raised': 0,
            'total_bets': 0,
            'bet_counts': 0,
            'largest_win': 0 
        } for name in player_names
    }

    for line in lines:
        if 'Total pot:' in line:
            pot_amount_match = re.search(r'Total pot: (\d+)', line)
            if pot_amount_match:
                pot_amount = int(pot_amount_match.group(1))
                game_stats['total_pot'] += pot_amount
                
        for player in player_names:
            if player in line:
                if 'folds' in line:
                    player_stats[player]['times_folded'] += 1

                # Handling both win scenarios
                win_match = re.search(r'wins pot \((\d+)\)|wins (\d+)', line)
                if win_match:
                    win_amount = int(win_match.group(1) or win_match.group(2))
                    player_stats[player]['hands_won'] += 1
                    if win_amount > player_stats[player]['largest_win']:
                        player_stats[player]['largest_win'] = win_amount

                # RAISES ----------------------------------------------------
                if 'raises' in line:
                    # if player raises, times_raised += 1, bet_count += 1 
                    bet_amount = int(re.search(r'raises (\d+)', line).group(1))
                    player_stats[player]['times_raised'] += 1
                    player_stats[player]['bet_counts'] += 1

                    # AND total bet amount increases
                    player_stats[player]['total_bets'] += bet_amount
                
                # CALLS -----------------------------------------------------
                if 'calls' in line or 'bets' in line:
                    # if player calls, bet_count += 1 
                    bet_amount = int(re.search(r'(calls|bets) (\d+)', line).group(2))
                    player_stats[player]['bet_counts'] += 1

                    # AND player total bet amount increases
                    player_stats[player]['total_bets'] += bet_amount

    # calculate averages
    for player in player_stats:
        if player_stats[player]['bet_counts'] > 0:
            player_stats[player]['average_bet'] = player_stats[player]['total_bets'] / player_stats[player]['bet_counts']
        else:
            player_stats[player]['average_bet'] = 0

    return player_stats

def get_final_payouts(file_path, hand_number):
    final_payouts = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Form the search string to match the desired hand number.
    search_str = f"start of hand #{hand_number}"
    start_collecting = False

    for line in lines:
        if search_str in line:
            start_collecting = True
        elif "start of hand #" in line and start_collecting:
            # If another hand start is found after the desired hand, stop collecting.
            break
        elif '--- pre-flop' in line and start_collecting:
            break
        elif start_collecting:
            if ')' in line:  # Ensure the line contains player chip info
                parts = line.split(':')
                if len(parts) > 1:
                    name_part = parts[1].strip()
                    try:
                        name = name_part.split(' (')[0].strip()
                        chips = int(name_part.split(' (')[1].split(')')[0].strip())
                        final_payouts[name] = chips / 1000  # Convert chips to dollars
                    except (IndexError, ValueError):
                        print(f"Failed to parse chips from line: {line.strip()}")
                        continue
    
    return final_payouts


def main():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Open File",
        initialdir="/",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    if file_path:
        hands_played = int(input("Enter the number of hands played: "))
        game_stats = {'total_pot': 0, 'hands_played': hands_played}
        stats = analyze_poker_stats(file_path, game_stats)

        for player, data in stats.items():
            print()
            print(f"{player}: Wins: {data['hands_won']}, Folded: {data['times_folded']}, Raised: {data['times_raised']}, "
                  f"Average Bet: {data['average_bet']:.2f} chips, Largest Win: {data['largest_win']} chips")
        
        # Calculate and print average pot size
        if game_stats['hands_played'] > 0:
            average_pot = game_stats['total_pot'] / game_stats['hands_played']
        else:
            average_pot = 0
        print()
        print(f"Average Pot Size for the game: {average_pot:.2f}")

        final_payouts = get_final_payouts(file_path, hands_played + 1)
        print("\nFinal Payouts (in $):")
        for player, payout in final_payouts.items():
            print(f"{player}: ${payout:.2f}")


    else:
        print("No file selected")

    root.destroy()

if __name__ == "__main__":
    main()

