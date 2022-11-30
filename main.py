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
            bet_x = UserBet.create(owner=user, match=x, left_bet=bets[user][x][0], right_bet=bets[user][x][1])


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
        left_win_value = EndedMatch.get(EndedMatch.name == choose_out.get()).left_score + EndedMatch.get(
            EndedMatch.name == choose_out.get()).right_score
        print("left")
    if EndedMatch.get(EndedMatch.name == choose_out.get()).left_score < EndedMatch.get(
            EndedMatch.name == choose_out.get()).right_score:
        right_win = True
        right_win_value = EndedMatch.get(EndedMatch.name == choose_out.get()).left_score + EndedMatch.get(
            EndedMatch.name == choose_out.get()).right_score
        print("right")
    if EndedMatch.get(EndedMatch.name == choose_out.get()).left_score == EndedMatch.get(
            EndedMatch.name == choose_out.get()).right_score:
        draw = True
        draw_value = EndedMatch.get(EndedMatch.name == choose_out.get()).left_score + EndedMatch.get(
            EndedMatch.name == choose_out.get()).right_score
        print("draw")
    # ADDING POINTS
    for user_bet in UserBet.get(UserBet.match == choose_out.get()).owner:
        print(user_bet)
        # if user_bet.left_score > user_bet.right_score == left_win:  # czy trafiona strona, lewa
        #
        #     score_for_user = (User
        #                       .update(score=+1)
        #                       .where(User.name == user_bet.owner)
        #                       .execute())
        #     if user_bet.left_score + user_bet.right_score == left_win_value:  # czy trafiony dokładny wynik
        #         score_for_user = (User
        #                           .update(score=+2)
        #                           .where(User.name == user_bet.owner)
        #                           .execute())
        # if user_bet.left_score < user_bet.right_score == right_win:  # czy trafiona strona, prawa
        #     score_for_user = (User
        #                       .update(score=+1)
        #                       .where(User.name == user_bet.owner)
        #                       .execute())
        #     if user_bet.left_score + user_bet.right_score == right_win_value:  # czy trafiony dokładny wynik
        #         score_for_user = (User
        #                           .update(score=+2)
        #                           .where(User.name == user_bet.owner)
        #                           .execute())
        # if user_bet.left_score == user_bet.right_score == draw:  # czy trafiony remis
        #     score_for_user = (User
        #                       .update(score=+1)
        #                       .where(User.name == user_bet.owner)
        #                       .execute())
        #     if user_bet.left_score + user_bet.right_score == draw_value:  # czy trafiony dokładny wynik
        #         score_for_user = (User
        #                           .update(score=+2)
        #                           .where(User.name == user_bet.owner)
        #                           .execute())
        #

# rebuild_db()  # IF STH HAPPEN WITH DB, RUN THIS !!!

#
#
# CTK PART
#
#

# CTK BASIC SETTINGS
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
root = customtkinter.CTk()
root.title('Obstawki')
root.geometry("600x400")


# LABELS ENTRY
def score_label_refresh():
    scoring = ""
    for namex in User.select():
        scoring += namex.name + ": " + str(namex.score) + "\n"
    score_label = customtkinter.CTkLabel(text=scoring, text_font='Tahoma', justify='right')
    score_label.grid(column=0, row=0, padx=25, pady=25)


def match_label_refresh():
    matches = ""
    for matchesx in EndedMatch.select():
        matches += matchesx.name + ": " + str(matchesx.left_score) + " : " + str(matchesx.right_score) + "\n"
    matches_label = customtkinter.CTkLabel(text=matches, text_font='Tahoma', justify='right')
    matches_label.grid(column=2, row=0, padx=25, pady=25)


match_label_refresh()
score_label_refresh()

# SHOW MATCHES LIST
value = ""
matches_for_list = []
choose = customtkinter.StringVar()

# MATCH LIST IN CTK COMBOBOX WITH POINTS (WITHOUT SCORING)
for matchesxx in EndedMatch.select():
    matches_for_list.append(matchesxx.name)
list_of_matches = customtkinter.CTkComboBox(width=200, values=matches_for_list, variable=choose)
list_of_matches.grid(column=2, row=1)

# CTK SCORE INPUT
score_input = customtkinter.CTkEntry(width=40, placeholder_text="0:0")
score_input.grid(column=0, row=1, padx=0, pady=25)


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
    print(User.get(User.name == "Grzegorz").score)


input_button = customtkinter.CTkButton(text='OK', text_font='Tahoma', command=change_input)
input_button.grid(column=1, row=1, padx=0, pady=25)

# SCORE LOGIC
# SOON KEKW


root.mainloop()
