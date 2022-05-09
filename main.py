import random
import csv
import time
#import mysql.connector as SQL


# To shuffle a new deck of cards
def shuffle(deck):
    output = []
    while len(deck) > 0:
        output.append(deck.pop(random.randint(0, len(deck) - 1)))
    return output

# To pull a card from the deck
def pull(deck, hand):
    hand.append(deck[0])
    return deck.pop(0)

# To  give optio to take card or stand
def offerChoice(deck, dealer_hand, player_hand):
    if value(player_hand) == 21:
        end(deck, dealer_hand, player_hand)
    choice = input("Do you want to hit or stand (h/s)?")
    if choice == "h":
        print(pull(deck, player_hand))
        print("Your hand is now: ", value(player_hand))
        if checkBust(player_hand):
            end(deck, dealer_hand, player_hand)
        else:
            offerChoice(deck, dealer_hand, player_hand)
    elif choice == "s":
        end(deck, dealer_hand, player_hand)
    else:
        print("Invalid choice")
        offerChoice(deck, dealer_hand, player_hand)

# To check if the player has busted
def checkBust(hand):
    if value(hand) > 21:
        return True
    else:
        return False

# To count the value of the hand
def value(hand):
    total = 0
    countAce = 0
    for card in hand:
        if card[0].isnumeric():
            if card[1].isnumeric():
                total += 10
            else:
                total += int(card[0])
        elif card[0] != "A":
            total += 10
        else:
            countAce += 1
            total += 11
    if total > 21:
        while countAce > 0 and total > 21:
            total -= 10
            countAce -= 1
    return total


# To play for the dealer and declare the winner
def dealerPickup(deck, dealer_hand, player_hand):
    print("Player's hand:", *player_hand)
    print("Player's Total", value(player_hand))
    print("Dealer's hand:", *dealer_hand)
    print("Dealer's Total", value(dealer_hand))
    if value(dealer_hand) <= value(player_hand):
        if value(dealer_hand) < 17:
            print(pull(deck, dealer_hand))
            dealerPickup(deck, dealer_hand, player_hand)
        elif value(dealer_hand) == value(player_hand):
            print("Player's hand:", *player_hand)
            print("Dealer's hand:", *dealer_hand)
            print("It's a tie!")
            modify("tie")
        else:
            print("Player's hand:", *player_hand)
            print("Dealer's hand:", *dealer_hand)
            print("Player wins!")
            modify("win")
    elif value(dealer_hand) == value(player_hand):
        print("It's a tie!")
        modify("tie")
    else:
        if value(dealer_hand) > 21:
            print("Dealer Bust")
            print("Player wins!")
            modify("win")
        else:
            print("Player Losses!")
            modify("loss")


# To modify the csv file
def modify(result):
    list=[]
    file = open("stats.csv", "r", newline="")
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if row[0] == name:
            if result == "win":
                list.append([row[0], row[1], int(row[2]) + 1, row[3], row[4]])
            elif result == "loss":
                list.append([row[0], row[1], row[2], int(row[3]) + 1, row[4]])
            else:
                list.append([row[0], row[1], row[2], row[3], int(row[4]) + 1])
        else:
            list.append(row)
    file.close()

    outFile = open("stats.csv", "w", newline="")
    csv_writer = csv.writer(outFile)
    for row in list:
        csv_writer.writerow(row)

    outFile.close()


# To end the game
def end(deck, dealer_hand, player_hand):
    if checkBust(player_hand):
        print("Player Bust!")
        modify("loss")
    elif value(player_hand) == 21:
        print("BlackJack!")
        modify("win")
    else:
        dealerPickup(deck, dealer_hand, player_hand)


# Game Function
def game(deck, dealer_hand, player_hand):
    pull(deck, player_hand)
    pull(deck, dealer_hand)
    pull(deck, player_hand)
    pull(deck, dealer_hand)
    print("Player's hand:", *player_hand)
    print("Dealer's hand:", dealer_hand[0], "🂠")
    print("Player's Total", value(player_hand))
    if value(player_hand) == 21:
        end(deck, dealer_hand, player_hand)
    offerChoice(deck, dealer_hand, player_hand)


# To start the game
def start():
    print("Let's Play!")
    time.sleep(2)
    dealer = []
    player = []

    deck = ["A♠  ", "2♠  ", "3♠  ", "4♠  ", "5♠  ", "6♠  ",
            "7♠  ", "8♠  ", "9♠  ", "10♠  ", "J♠  ", "Q♠  ", "K♠  ",
            "A♣  ", "2♣  ", "3♣  ", "4♣  ", "5♣  ", "6♣  ",
            "7♣  ", "8♣  ", "9♣  ", "10♣  ", "J♣  ", "Q♣  ", "K♣  ",
            "A♥  ", "2♥  ", "3♥  ", "4♥  ", "5♥  ", "6♥  ",
            "7♥  ", "8♥  ", "9♥  ", "10♥  ", "J♥  ", "Q♥  ", "K♥  ",
            "A♦  ", "2♦  ", "3♦  ", "4♦  ", "5♦  ", "6♦  ",
            "7♦  ", "8♦  ", "9♦  ", "10♦  ", "J♦  ", "Q♦  ", "K♦  "]
    
    game(shuffle(deck), dealer, player)
    x = input("Do you want to play again? (y/n)\n")
    if x == "y":
        start()

# To create stats.csv file if it doesn't exist
print("Welcome to BlackJack!")
print("Does the stats.csv file exist? (y/n)")
x = input()
if x == "y":
    print("Great! Let's play!")
else:
    file = open("stats.csv", "w", newline="")
    csv_writer = csv.writer(file)
    csv_writer.writerow(["Name", "Password", "Wins", "Losses", "Ties"])
    file.close()
    print("stats.csv file created!")

while True:
    print("Do you want to login, register, show stats, or quit (l/r/s/q)?")
    choice = input()
    if choice == "r":
        print("Enter your name:")
        name = input()
        print("Enter your password:")
        password = input()
        file = open("stats.csv", "a", newline="")
        csv_writer = csv.writer(file)
        csv_writer.writerow([name, password, 0, 0, 0])
        file.close()
        print("Account created!")
        start()
    elif choice == "l":
        found = 0
        file = open("stats.csv", "r", newline="")
        csv_reader = csv.reader(file)
        print("Enter your name:")
        name = input()
        for row in csv_reader:
            if name == row[0]:
                found = 1
                print("Enter your password:")
                password = input()
                if password == row[1]:
                    print("Welcome back", name)
                    file.close()
                    start()
                    break
                else:
                    print("Incorrect password!")
                    file.close()
                    break
        if found == 0:
            print("Account not found!")
            file.close()
            break
        break
    elif choice == "s":
        file = open("stats.csv", "r", newline="")
        csv_reader = csv.reader(file)
        for row in csv_reader:
            print(row[0], "|", row[2], "|", row[3], "|", row[4])
    else:
        break



#Code for SQL-Connectivity_implementation
'''
Create Table

MyDB=SQL.connect(host='localhost',user='root',password='',database='blackjack')
if MyDB.is_connected():
    print("MySQL successfully connected !")
    print("Your Connection ID is: ",MyDB.connection_id)
    MyCursor=MyDB.cursor()
    MyCursor.execute("CREATE TABLE Balance (ID varchar(20),pass VARCHAR(20), bal);")


Insert Data

if MyDB.is_connected():
    MyCursor=MyDB.cursor()
    Command="INSERT INTO Balance VALUES (%s, %s, %s)"
    print("Enter the details of the new row:")
    
    PID=input("Person's ID:")
    NAME=input("Person's Password:")
    PHONE=input("Balance:")
    Values=(ID,pass,balance)
    
    MyCursor.execute(Command,Values)
    MyDB.commit();
    print("One ROW has been added intot the table balance.")

if MyDB.is_connected():
    NAME=input("\n\nEnter the name to be updated : ")
    bal=input("Enter the new bal: ")
    MyCursor=MyDB.cursor()
    Command="UPDATE Balance SET bal=%s WHERE NAME=%s;"
    Value=(bal,NAME)
    MyCursor.execute(Command,Value)
    MyDB.commit()
'''