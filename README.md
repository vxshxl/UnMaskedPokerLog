# UnMasked Poker log analysis tool

## Project Description
This tool analyzes UnMasked poker game logs to extract and compute various statistics including player behaviors, wins, and final payouts. It helps users gain insights into game dynamics and player performances through detailed statistical outputs.

## How to Run
To run this tool, you need Python installed on your system. The script is executed in a graphical user interface environment where you can select a poker game log file in text format.

### Steps:
  1. Ensure Python and Tkinter are installed on your system. If Tkinter is not installed, you can install it using pip:
     ```
     pip install tk
     ```
  2. clone or download the project to your local machine.
  3. Navigate to the directory containing the script.
  4. Run the script using Python: <br />
    ```
    python3 UnMaskedPoker.py
    ```
  5. A file dialog will appear. Select the poker game log file you want to analyze.
  6. Input the number of hands played when prompted in the console.
  7. View the output directly in the console.

## Dependencies 
  - Python 3.x
  - Tkinter

## Example Output

  Enter the number of hands played: 40
  
  BigUzi: Wins: 0, Folded: 13, Raised: 2, Average Bet: 167.86, Largest Win: 0<br />
  vidit: Wins: 4, Folded: 21, Raised: 3, Average Bet: 186.93, Largest Win: 6237<br />
  the.trij: Wins: 5, Folded: 28, Raised: 2, Average Bet: 152.11, Largest Win: 3118<br />
  youngdesi: Wins: 6, Folded: 28, Raised: 5, Average Bet: 146.15, Largest Win: 4822<br />
  vxshxl: Wins: 5, Folded: 22, Raised: 9, Average Bet: 153.13, Largest Win: 2304<br />
  Zigenheimer: Wins: 5, Folded: 26, Raised: 1, Average Bet: 149.93, Largest Win: 3820<br />
  jay: Wins: 6, Folded: 25, Raised: 6, Average Bet: 164.58, Largest Win: 4067<br />
  
  Final Payouts (in $):<br />
  vidit: $6.62<br />
  the.trij: $3.37<br />
  youngdesi: $9.51<br />
  vxshxl: $3.24<br />
  Zigenheimer: $2.05<br />
  jay: $10.21<br />
  
  Average Pot Size for the game: $1676.47
