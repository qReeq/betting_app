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


# LABELS ENTRY
def score_label_refresh():
    users_with_score = ""

    for names in User.select():
        score_us = 0
        for score in UserBet.select().where(UserBet.owner_id == names.name):
            score_us += score.score_bet
        users_with_score += names.name + ": " + str(score_us) + "\n"
    users_with_score_label = customtkinter.CTkLabel(score_tab, text=users_with_score, font=('Tahoma', 15),
                                                    justify='right')
    users_with_score_label.grid(column=2, row=0, padx=25, pady=25)


def match_label_refresh():
    matches_list_with_score = ""
    for matches_db in EndedMatch.select():
        matches_list_with_score += matches_db.name + ": " + str(matches_db.left_score) + " : " + str(
            matches_db.right_score) + "\n"
    matches_label_with_score = customtkinter.CTkLabel(score_tab, text=matches_list_with_score, font=('Tahoma', 15),
                                                      justify='right')
    matches_label_with_score.grid(column=0, row=0, padx=25, pady=25)


match_label_refresh()
score_label_refresh()

# SHOW MATCHES LIST
value = ""
matches_for_list = []
choose = customtkinter.StringVar()

# MATCH LIST IN CTK COMBOBOX WITH POINTS (WITHOUT SCORING)
for matches in EndedMatch.select():
    matches_for_list.append(matches.name)
list_of_matches = customtkinter.CTkOptionMenu(score_tab, width=200, values=matches_for_list, variable=choose)
list_of_matches.grid(column=1, row=1)

# CTK SCORE INPUT
score_input = customtkinter.CTkEntry(score_tab, width=40, placeholder_text="0:0")
score_input.grid(column=0, row=1)


# BUTTON TO CHANGE THE ACTUAL SCORE IN DB
def change_input():
    insert = score_input.get()
    (EndedMatch
     .update(left_score=insert[0])
     .where(EndedMatch.name == choose.get())
     .execute())
    (EndedMatch
     .update(right_score=insert[2])
     .where(EndedMatch.name == choose.get())
     .execute())
    checking_score(choose_out=choose)
    match_label_refresh()
    score_label_refresh()


#
# ADDING USER TAB
#
choosed_user = customtkinter.StringVar()
add_user_entry = customtkinter.CTkEntry(user_tab, width=100, placeholder_text='George')
add_user_entry.grid(column=0, row=0, padx=50, pady=50)


def add_refresh_users():
    User.create(name=add_user_entry.get(), score=0)
    users = []
    for user in User.select():
        users.append(user.name)
    list_of_users = customtkinter.CTkOptionMenu(user_tab, width=200, values=users, variable=choosed_user, fg_color="gray")
    list_of_users.grid(column=0, row=1, padx=60, pady=60)


def delete_refresh_users():
    User.delete().where(User.name == choosed_user.get()).execute()
    users = []
    for user in User.select():
        users.append(user.name)
    list_of_users = customtkinter.CTkOptionMenu(user_tab, width=200, values=users, variable=choosed_user, fg_color="gray")
    list_of_users.grid(column=0, row=1, padx=60, pady=60)


users_base = []
for user in User.select():
    users_base.append(user.name)
list_of_users = customtkinter.CTkOptionMenu(user_tab, width=200, values=users_base, variable=choosed_user, fg_color="gray")
list_of_users.grid(column=0, row=1, padx=60, pady=60)
add_user_button = customtkinter.CTkButton(user_tab, text='Add User', command=add_refresh_users)
add_user_button.grid(column=1, row=0, padx=60, pady=0)

delete_user_button = customtkinter.CTkButton(user_tab, text='Delete User', command=delete_refresh_users, fg_color="red")
delete_user_button.grid(column=1, row=1, padx=60, pady=0)

input_match_button = customtkinter.CTkButton(score_tab, text='OK', font=('Tahoma', 15), command=change_input)
input_match_button.grid(column=2, row=1, padx=60, pady=60)


#
# ADDING MATCH TAB
#
choosed_match = customtkinter.StringVar()
add_match_entry = customtkinter.CTkEntry(match_tab, width=100, placeholder_text='Poland - Germany')
add_match_entry.grid(column=0, row=0, padx=50, pady=50)


def add_refresh_matches():
    EndedMatch.create(name=add_match_entry.get(), left_score=0, right_score=0)
    matches = []
    for match in EndedMatch.select():
        matches.append(match.name)
    list_of_matches = customtkinter.CTkOptionMenu(match_tab, width=200, values=matches, variable=choosed_user, fg_color="gray")
    list_of_matches.grid(column=0, row=1, padx=60, pady=60)


def delete_refresh_matches():
    EndedMatch.delete().where(EndedMatch.name == choosed_match.get()).execute()
    matches = []
    for match in EndedMatch.select():
        matches.append(match.name)
    list_of_matches = customtkinter.CTkOptionMenu(match_tab, width=200, values=matches, variable=choosed_match, fg_color="gray")
    list_of_matches.grid(column=0, row=1, padx=60, pady=60)


match_base = []
for match in EndedMatch.select():
    match_base.append(match.name)
list_of_match = customtkinter.CTkOptionMenu(match_tab, width=200, values=match_base, variable=choosed_match, fg_color="gray")
list_of_match.grid(column=0, row=1, padx=60, pady=60)
add_match_button = customtkinter.CTkButton(match_tab, text='Add Match', command=add_refresh_matches)
add_match_button.grid(column=1, row=0, padx=60, pady=0)

delete_match_button = customtkinter.CTkButton(match_tab, text='Delete Match', command=delete_refresh_matches, fg_color="red")
delete_match_button.grid(column=1, row=1, padx=60, pady=0)


# SCORE LOGIC
# SOON KEK


root.mainloop()
