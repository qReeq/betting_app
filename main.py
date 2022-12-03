from peewee import *
from mecze import user_score
from scores import final_score_matches
from bets import bets
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
    score_bet = SmallIntegerField()

    class Meta:
        database = db


db.connect()
db.create_tables([EndedMatch, UserBet, User])

users_list = []
for n in user_score:
    users_list.append(n)


# ADDING ALL VALUES TO DB
def rebuild_db():
    #   USER LISTS WITH POINTS
    for user in user_score:
        user = User.create(name=user, score=user_score[user])
    # ENDED MATCHES WITH RESULTS
    for score in final_score_matches:
        score = EndedMatch.create(name=score, left_score=final_score_matches[score][0],
                                  right_score=final_score_matches[score][1])
    # MATCH BETS FOR EACH USER
    for user in bets:
        for x in bets[user]:
            bet_x = UserBet.create(owner=user, match=x, left_bet=bets[user][x][0], right_bet=bets[user][x][1],
                                   score_bet=bets[user][x][2])


def checking_score(choose_out):
    left_win = False
    right_win = False
    draw = False
    draw_value = 0
    left_win_value = 0
    right_win_value = 0
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
            score_for_user = (UserBet
                              .update(score_bet=10)
                              .where(UserBet.match == user_bet.match)
                              .execute())
            if user_bet.right_bet == EndedMatch.get(EndedMatch.name == choose_out.get()).right_score and \
                    user_bet.left_bet == EndedMatch.get(EndedMatch.name == choose_out.get()).left_score:
                print(user_bet.left_bet, user_bet.right_bet)
                print("yay")

                score_for_user3 = (UserBet
                                   .update(score_bet=30)
                                   .where(UserBet.match == user_bet.match)
                                   .execute())
                print("yay2")
        else:
            score_for_user = (UserBet
                              .update(score_bet=0)
                              .where(UserBet.owner_id == user_bet.owner_id)
                              .execute())


# rebuild_db()  # IF STH HAPPEN WITH DB, RUN THIS !!!
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
user_tab = tabview.add("User input")  # add tab at the end
match_tab = tabview.add("User match input")  # add tab at the end
score_tab = tabview.add("Scores and match update")  # add tab at the end
tabview.set("Scores and match update")  # set currently visible tab


# LABELS ENTRY
def score_label_refresh():
    scoring = ""

    for namex in User.select():
        score_us = 0
        for score in UserBet.select().where(UserBet.owner_id == namex.name):
            score_us += score.score_bet
        scoring += namex.name + ": " + str(score_us) + "\n"
    score_label = customtkinter.CTkLabel(score_tab, text=scoring, font=('Tahoma', 15), justify='right')
    score_label.grid(column=2, row=0, padx=25, pady=25, )


def match_label_refresh():
    matches = ""
    for matchesx in EndedMatch.select():
        matches += matchesx.name + ": " + str(matchesx.left_score) + " : " + str(matchesx.right_score) + "\n"
    matches_label = customtkinter.CTkLabel(score_tab, text=matches, font=('Tahoma', 15), justify='right')
    matches_label.grid(column=0, row=0, padx=25, pady=25)


match_label_refresh()
score_label_refresh()

# SHOW MATCHES LIST
value = ""
matches_for_list = []
choose = customtkinter.StringVar()

# MATCH LIST IN CTK COMBOBOX WITH POINTS (WITHOUT SCORING)
for matchesxx in EndedMatch.select():
    matches_for_list.append(matchesxx.name)
list_of_matches = customtkinter.CTkComboBox(score_tab, width=200, values=matches_for_list, variable=choose)
list_of_matches.grid(column=1, row=1)

# CTK SCORE INPUT
score_input = customtkinter.CTkEntry(score_tab, width=40, placeholder_text="0:0")
score_input.grid(column=0, row=1)


# BUTTON TO CHANGE THE ACTUAL SCORE IN DB
def change_input():
    insert = score_input.get()
    ls = (EndedMatch
          .update(left_score=insert[0])
          .where(EndedMatch.name == choose.get())
          .execute())
    rs = (EndedMatch
          .update(right_score=insert[2])
          .where(EndedMatch.name == choose.get())
          .execute())
    match_label_refresh()
    checking_score(choose_out=choose)
    score_label_refresh()


input_button = customtkinter.CTkButton(score_tab, text='OK', font=('Tahoma', 15), command=change_input)
input_button.grid(column=2, row=1)

# SCORE LOGIC
# SOON KEK


root.mainloop()
