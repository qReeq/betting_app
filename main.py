from peewee import *
from mecze import user_score
from scores import final_score_matches
from bets import bets
import customtkinter

# DATABASE

db = SqliteDatabase('main.db')


class EndedMatch(Model):
    name = CharField()
    left_score = DateField()
    right_score = DateField()

    class Meta:
        database = db


class User(Model):
    name = CharField()
    score = DateField()

    class Meta:
        database = db


class User1Bet(Model):
    owner = ForeignKeyField(User, backref='user')
    match = CharField()
    left_bet = DateField()
    right_bet = DateField()

    class Meta:
        database = db


class User2Bet(Model):
    owner = ForeignKeyField(User, backref='user')
    match = CharField()
    left_bet = DateField()
    right_bet = DateField()

    class Meta:
        database = db


class User3Bet(Model):
    owner = ForeignKeyField(User, backref='user')
    match = CharField()
    left_bet = DateField()
    right_bet = DateField()

    class Meta:
        database = db


class User4Bet(Model):
    owner = ForeignKeyField(User, backref='user')
    match = CharField()
    left_bet = DateField()
    right_bet = DateField()

    class Meta:
        database = db


class User5Bet(Model):
    owner = ForeignKeyField(User, backref='user')
    match = CharField()
    left_bet = DateField()
    right_bet = DateField()

    class Meta:
        database = db


class User6Bet(Model):
    owner = ForeignKeyField(User, backref='user')
    match = CharField()
    left_bet = DateField()
    right_bet = DateField()

    class Meta:
        database = db


class User7Bet(Model):
    owner = ForeignKeyField(User, backref='user')
    match = CharField()
    left_bet = DateField()
    right_bet = DateField()

    class Meta:
        database = db


class User8Bet(Model):
    owner = ForeignKeyField(User, backref='user')
    match = CharField()
    left_bet = DateField()
    right_bet = DateField()

    class Meta:
        database = db


class User9Bet(Model):
    owner = ForeignKeyField(User, backref='user')
    match = CharField()
    left_bet = DateField()
    right_bet = DateField()

    class Meta:
        database = db


class User10Bet(Model):
    owner = ForeignKeyField(User, backref='user')
    match = CharField()
    left_bet = DateField()
    right_bet = DateField()

    class Meta:
        database = db


class User11Bet(Model):
    owner = ForeignKeyField(User, backref='user')
    match = CharField()
    left_bet = DateField()
    right_bet = DateField()

    class Meta:
        database = db


db.connect()
db.create_tables([EndedMatch, User1Bet, User2Bet, User3Bet, User4Bet, User5Bet, User6Bet, User7Bet, User8Bet, User9Bet,
                  User10Bet, User11Bet, User])


def rebuild_db():
    for matches in bets['Grzegorz']:
        grzegorzbet = User1Bet.create(owner='Grzegorz', match=matches, left_bet=bets['Grzegorz'][matches][0],
                                      right_bet=bets['Grzegorz'][matches][1])

    for matches in bets['Michał K.']:
        michalbet = User2Bet.create(owner='Michał K.', match=matches, left_bet=bets['Grzegorz'][matches][0],
                                    right_bet=bets['Michał K.'][matches][1])
    for user in user_score:
        user = User.create(name=user, score=user_score[user])

    for score in final_score_matches:
        score = EndedMatch.create(name=score, left_score=final_score_matches[score][0],
                                  right_score=final_score_matches[score][1])


# rebuild_db()

# print(User1Bet.get(User1Bet.match == 'Walia-Iran').right_bet)


# VISUAL
scoring = ""
for namex in User.select():
    scoring += namex.name + ": " + str(namex.score) + "\n"

matches = ""
for matchesx in EndedMatch.select():
    matches += matchesx.name + ": " + str(matchesx.left_score) + " : " + str(matchesx.right_score) + "\n"

# OKNO PROGRAMU
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()

root.title('Obstawki')
root.geometry("600x400")

score_label = customtkinter.CTkLabel(text=scoring, text_font='Tahoma', justify='right')
score_label.grid(column=0, row=0, padx=25, pady=25)

matches_label = customtkinter.CTkLabel(text=matches, text_font='Tahoma', justify='right')
matches_label.grid(column=2, row=0, padx=25, pady=25)

# SHOW MATCHES LIST

value = ""
matches_for_list = []


def selecto(choice):
    return choice


choose = customtkinter.StringVar()

for matchesxx in EndedMatch.select():
    matches_for_list.append(matchesxx.name)

list_of_matches = customtkinter.CTkComboBox(width=200, values=matches_for_list, variable=choose, command=selecto)
list_of_matches.grid(column=2, row=1)
list_of_matches.bind("<<ListboxSelect>>", selecto)



# SCORE INPUT
score_input = customtkinter.CTkEntry(width=40, placeholder_text="0:0")
score_input.grid(column=0, row=1, padx=0, pady=25)


def change_input():
    insert = score_input.get()
    fir = (EndedMatch.update({EndedMatch.left_score: insert[0]}).where(EndedMatch.name == choose).execute())
    # print(EndedMatch.get(EndedMatch.name == choose).left_bet)


# print(User1Bet.get(User1Bet.match == 'Walia-Iran').right_bet)
input_button = customtkinter.CTkButton(text='OK', text_font='Tahoma', command=change_input)
input_button.grid(column=1, row=1, padx=0, pady=25)

root.mainloop()
