from peewee import *
import customtkinter

# DATABASE BASICS WITH CLASSES
db = SqliteDatabase('main.db')


class EndedMatch(Model):
    name = CharField()
    left_score = SmallIntegerField()
    right_score = SmallIntegerField()

    class Meta:
        database = db


class User(Model):
    name = CharField()
    score = SmallIntegerField()

    class Meta:
        database = db


class UserBet(Model):
    owner = ForeignKeyField(User, backref='user')
    match = CharField()
    left_bet = SmallIntegerField()
    right_bet = SmallIntegerField()
    score_bet = IntegerField()

    class Meta:
        database = db


db.connect()
db.create_tables([EndedMatch, UserBet, User])


def checking_score(choose_out):
    left_win = False
    right_win = False
    draw = False
    # CHECKING ACTUAL UPDATED SCORE, LEFT, RIGHT OR DRAW

    if EndedMatch.get(EndedMatch.name == choose_out.get()).left_score > EndedMatch.get(
            EndedMatch.name == choose_out.get()).right_score:
        left_win = True
    if EndedMatch.get(EndedMatch.name == choose_out.get()).right_score < EndedMatch.get(
            EndedMatch.name == choose_out.get()).right_score:
        right_win = True
    if EndedMatch.get(EndedMatch.name == choose_out.get()).left_score == EndedMatch.get(
            EndedMatch.name == choose_out.get()).right_score:
        draw = True
    # ADDING POINTS
    for user_bet in UserBet.select().where(UserBet.match == choose_out.get()):
        if (user_bet.left_bet > user_bet.right_bet) == left_win and \
                (user_bet.left_bet < user_bet.right_bet) == right_win and \
                (user_bet.left_bet == user_bet.right_bet) == draw:
            (UserBet
             .update(score_bet=10)
             .where(UserBet.match == user_bet.match)
             .execute())
            if user_bet.right_bet == EndedMatch.get(EndedMatch.name == choose_out.get()).right_score and \
                    user_bet.left_bet == EndedMatch.get(EndedMatch.name == choose_out.get()).left_score:
                print(user_bet.left_bet, user_bet.right_bet)
                print("yay")

                (UserBet
                 .update(score_bet=30)
                 .where(UserBet.match == user_bet.match)
                 .execute())
                print("yay2")
        else:
            (UserBet
             .update(score_bet=0)
             .where(UserBet.owner_id == user_bet.owner_id)
             .execute())


#
#
# CTK PART
#
# CTK BASIC SETTINGS
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
root = customtkinter.CTk()
root.title('Bet_app')
root.geometry("660x450")
frame = customtkinter.CTkFrame(root, corner_radius=10)
tabview = customtkinter.CTkTabview(root, width=620, height=400)
tabview.grid(padx=20, pady=20)
user_tab = tabview.add("User input")
match_tab = tabview.add("Match input")
match_bet_tab = tabview.add("User bets for matches")
score_tab = tabview.add("Scores and match update")
tabview.set("Scores and match update")
choose = customtkinter.StringVar()
choosed_match = customtkinter.StringVar()
choosed_user = customtkinter.StringVar()
matches_with_score = ""
users_with_score = ""
matches = []
users = []
user_matches = f"{choosed_user.get()} bets:\n"

for matches_db in EndedMatch.select():
    matches_with_score += matches_db.name + ": " + str(matches_db.left_score) + " : " + str(
        matches_db.right_score) + "\n"
for names in User.select():
    score_us = 0
    for score in UserBet.select().where(UserBet.owner_id == names.name):
        score_us += score.score_bet
    users_with_score += names.name + ": " + str(score_us) + "\n"
for user in User.select():
    users.append(user.name)
for match in EndedMatch.select():
    matches.append(match.name)
for matches_db in UserBet.select().where(UserBet.owner_id == choosed_user.get()):
    user_matches += matches_db.match + ": " + str(matches_db.left_bet) + " : " + str(
        matches_db.right_bet) + "\n"

matches_label_with_score = customtkinter.CTkLabel(score_tab,
                                                  text=matches_with_score,
                                                  font=('Tahoma', 15),
                                                  justify='right')
matches_label_with_score.grid(column=0, row=0, padx=25, pady=25)

users_with_score_label = customtkinter.CTkLabel(score_tab,
                                                text=users_with_score,
                                                font=('Tahoma', 15),
                                                justify='right')
users_with_score_label.grid(column=3, row=0, padx=25, pady=25)

# USER TAB
list_of_matches_for_final_tab = customtkinter.CTkOptionMenu(score_tab,
                                                            width=200,
                                                            values=matches,
                                                            variable=choose)
list_of_matches_for_final_tab.grid(column=0, row=1, padx=20)

list_of_users = customtkinter.CTkOptionMenu(user_tab,
                                            width=200,
                                            values=users,
                                            variable=choosed_user,
                                            fg_color="gray")
list_of_users.grid(column=0, row=1, padx=60, pady=60)

# MATCH TAB
list_of_matches = customtkinter.CTkOptionMenu(match_tab,
                                              width=200,
                                              values=matches,
                                              variable=choosed_match,
                                              fg_color="gray")
list_of_matches.grid(column=0, row=1, padx=60, pady=60)

# BET TAB
list_of_matches_for_bets = customtkinter.CTkOptionMenu(match_bet_tab,
                                                       width=200,
                                                       values=matches,
                                                       variable=choosed_match,
                                                       fg_color="gray")
list_of_matches_for_bets.grid(column=0, row=1, padx=20, pady=60)

list_of_users_for_bets = customtkinter.CTkOptionMenu(match_bet_tab,
                                                     width=200,
                                                     values=users,
                                                     variable=choosed_user,
                                                     fg_color="gray")
list_of_users_for_bets.grid(column=0, row=0, padx=20, pady=60)

matches_label_with_score_for_bets = customtkinter.CTkLabel(match_bet_tab,
                                                           text=user_matches,
                                                           font=('Tahoma', 15),
                                                           justify='right')
matches_label_with_score_for_bets.grid(column=3, row=0, padx=40)


def update_label():
    matches_with_score_up = ""
    users_with_score_up = ""
    matches_up = []
    users_up = []
    user_matches_up = f"{choosed_user.get()} bets:\n"
    print(matches_up)
    for matches_db in EndedMatch.select():
        matches_with_score_up += matches_db.name + ": " + str(matches_db.left_score) + " : " + str(
            matches_db.right_score) + "\n"
    for names in User.select():
        score_us = 0
        for score in UserBet.select().where(UserBet.owner_id == names.name):
            score_us += score.score_bet
        users_with_score_up += names.name + ": " + str(score_us) + "\n"
    for user in User.select():
        users_up.append(user.name)
    for match in EndedMatch.select():
        matches_up.append(match.name)
    for matches_db in UserBet.select().where(UserBet.owner_id == choosed_user.get()):
        user_matches_up += matches_db.match + ": " + str(matches_db.left_bet) + " : " + str(
            matches_db.right_bet) + "\n"
    matches_label_with_score.configure(text=matches_with_score_up)
    users_with_score_label.configure(text=users_with_score_up)
    list_of_matches.configure(values=matches_up)
    list_of_users.configure(values=users_up)
    list_of_matches_for_bets.configure(values=matches_up)
    list_of_users_for_bets.configure(values=users_up)
    matches_label_with_score_for_bets.configure(text=user_matches_up)
    list_of_matches_for_final_tab.configure(values=matches_up)


def update_bet_score():
    (UserBet
     .update(left_bet=score_entry_1.get())
     .where((UserBet.match == choosed_match.get()) &
            UserBet.owner == choosed_user.get())
     .execute())
    (UserBet
     .update(right_bet=score_entry_2.get())
     .where((UserBet.match == choosed_match.get()) &
            UserBet.owner == choosed_user.get())
     .execute())
    update_label()


def add_bet_score():
    (UserBet.insert({
        UserBet.owner: str(choosed_user.get()),
        UserBet.match: str(choosed_match.get()),
        UserBet.score_bet: 0,
        UserBet.left_bet: int(score_entry_1.get()),
        UserBet.right_bet: int(score_entry_2.get())}).execute())
    update_label()


# CTK SCORE INPUT
score_input_first = customtkinter.CTkEntry(score_tab,
                                           width=30,
                                           placeholder_text="0")
score_input_first.grid(column=1, row=1)
score_input_second = customtkinter.CTkEntry(score_tab,
                                            width=30,
                                            placeholder_text="0")
score_input_second.grid(column=2, row=1)


# BUTTON TO CHANGE THE ACTUAL SCORE IN DB
def change_input():
    (EndedMatch
     .update(left_score=score_input_first.get())
     .where(EndedMatch.name == choose.get())
     .execute())
    (EndedMatch
     .update(right_score=score_input_second.get())
     .where(EndedMatch.name == choose.get())
     .execute())
    checking_score(choose_out=choose)
    update_label()


input_match_button = customtkinter.CTkButton(score_tab,
                                             text='Update Score',
                                             font=('Tahoma', 12),
                                             command=change_input)
input_match_button.grid(column=3, row=1, padx=60, pady=60)
#
# ADDING USER TAB
#

add_user_entry = customtkinter.CTkEntry(user_tab,
                                        width=100,
                                        placeholder_text='George')
add_user_entry.grid(column=0, row=0, padx=50, pady=50)


def add_users():
    User.create(name=add_user_entry.get(), score=0)
    update_label()


def delete_users():
    User.delete().where(User.name == choosed_user.get()).execute()
    update_label()


add_user_button = customtkinter.CTkButton(user_tab,
                                          text='Add User',
                                          command=add_users)
add_user_button.grid(column=1, row=0, padx=60, pady=0)

delete_user_button = customtkinter.CTkButton(user_tab,
                                             text='Delete User',
                                             command=delete_users,
                                             fg_color="red")
delete_user_button.grid(column=1, row=1, padx=60, pady=0)

#
# ADDING MATCH TAB
#

add_match_entry = customtkinter.CTkEntry(match_tab,
                                         width=200,
                                         placeholder_text='Poland - Germany')
add_match_entry.grid(column=0, row=0, padx=50, pady=50)


def add_matches():
    EndedMatch.create(name=add_match_entry.get(), left_score=0, right_score=0)
    update_label()


def delete_matches():
    EndedMatch.delete().where(EndedMatch.name == choosed_match.get()).execute()
    update_label()


add_match_button = customtkinter.CTkButton(match_tab,
                                           text='Add Match',
                                           command=add_matches)
add_match_button.grid(column=1, row=0, padx=60, pady=0)

delete_match_button = customtkinter.CTkButton(match_tab,
                                              text='Delete Match',
                                              command=delete_matches,
                                              fg_color="red")
delete_match_button.grid(column=1, row=1, padx=60, pady=0)

#
#   USERS BETS
#
score_entry_1 = customtkinter.CTkEntry(match_bet_tab,
                                       width=30,
                                       placeholder_text="0")
score_entry_1.grid(column=1, row=1)

score_entry_2 = customtkinter.CTkEntry(match_bet_tab,
                                       width=30,
                                       placeholder_text="0")
score_entry_2.grid(column=2, row=1)

update_user_score_button = customtkinter.CTkButton(match_bet_tab,
                                                   text='Add Bet',
                                                   command=add_bet_score)
update_user_score_button.grid(column=3, row=1, padx=60, pady=0)

root.mainloop()
