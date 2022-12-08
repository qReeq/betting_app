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


def checking_score():
    left_win = False
    right_win = False
    draw = False
    # CHECKING ACTUAL UPDATED SCORE, LEFT, RIGHT OR DRAW
    left_score_match = EndedMatch.get(EndedMatch.name == choose.get()).left_score
    right_score_match = EndedMatch.get(EndedMatch.name == choose.get()).right_score
    if left_score_match > right_score_match:
        left_win = True
    elif left_score_match < right_score_match:
        right_win = True
    else:
        draw = True

    # ADDING POINTS
    for user_bet in UserBet.select().where(UserBet.match == choose.get()):
        if (user_bet.left_bet > user_bet.right_bet) == left_win and \
                (user_bet.left_bet < user_bet.right_bet) == right_win and \
                (user_bet.left_bet == user_bet.right_bet) == draw:
            (UserBet
             .update(score_bet=1)
             .where((UserBet.match == user_bet.match) &
                    (UserBet.owner == user_bet.owner_id))
             .execute())
            if user_bet.right_bet == EndedMatch.get(EndedMatch.name == choose.get()).right_score and \
                    user_bet.left_bet == EndedMatch.get(EndedMatch.name == choose.get()).left_score:
                (UserBet
                 .update(score_bet=3)
                 .where((UserBet.match == user_bet.match) &
                        (UserBet.owner == user_bet.owner_id))
                 .execute())
        else:
            (UserBet
             .update(score_bet=0)
             .where((UserBet.match == user_bet.match) &
                    (UserBet.owner == user_bet.owner_id))
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
root.geometry("690x450")
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

for matches_db in EndedMatch.select():  # Receiving string of matches with score for CTk label.
    matches_with_score += matches_db.name + ": " + str(matches_db.left_score) + " : " + str(
        matches_db.right_score) + "\n"
    matches.append(matches_db.name)
for names in User.select().order_by(-User.score):  # Receiving string of users with total score for CTk label.
    score_us = 0
    for score in UserBet.select().where(UserBet.owner_id == names.name):
        score_us += score.score_bet
    users_with_score += names.name + ": " + str(score_us) + "\n"
    users.append(names.name)
for matches_selected_user in UserBet.select().where(
        UserBet.owner_id == choosed_user.get()):  # Receiving string of all of (selected user) bets CTk label
    user_matches += matches_selected_user.match + ": " + str(matches_selected_user.left_bet) + " : " + str(
        matches_selected_user.right_bet) + "\n"

# ADDING ALL LABELS/LISTS/ENTRIES WITH INPUTS TO PROG.
matches_label_with_score = customtkinter.CTkLabel(score_tab,
                                                  text=matches_with_score,
                                                  font=('Tahoma', 15),
                                                  justify='right')
matches_label_with_score.grid(column=0, row=0, padx=60, pady=30)
users_with_score_label = customtkinter.CTkLabel(score_tab,
                                                text=users_with_score,
                                                font=('Tahoma', 15),
                                                justify='right')
users_with_score_label.grid(column=3, row=0, padx=60, pady=30)
list_of_matches_for_final_tab = customtkinter.CTkOptionMenu(score_tab,
                                                            width=200,
                                                            values=matches,
                                                            variable=choose)
list_of_matches_for_final_tab.grid(column=0, row=1, padx=60, pady=0)
score_input_first = customtkinter.CTkEntry(score_tab,
                                           width=30,
                                           placeholder_text="0")
score_input_first.grid(column=1, row=1)
score_input_second = customtkinter.CTkEntry(score_tab,
                                            width=30,
                                            placeholder_text="0")
score_input_second.grid(column=2, row=1)

list_of_users = customtkinter.CTkOptionMenu(user_tab,
                                            width=200,
                                            values=users,
                                            variable=choosed_user,
                                            fg_color="gray")
list_of_users.grid(column=0, row=1, padx=60, pady=60)
add_user_entry = customtkinter.CTkEntry(user_tab,
                                        width=100,
                                        placeholder_text='George')
add_user_entry.grid(column=0, row=0, padx=50, pady=50)

list_of_matches = customtkinter.CTkOptionMenu(match_tab,
                                              width=200,
                                              values=matches,
                                              variable=choosed_match,
                                              fg_color="gray")
list_of_matches.grid(column=0, row=1, padx=60, pady=60)
add_match_entry = customtkinter.CTkEntry(match_tab,
                                         width=200,
                                         placeholder_text='Poland - Germany')
add_match_entry.grid(column=0, row=0, padx=50, pady=50)

list_of_matches_for_bets = customtkinter.CTkOptionMenu(match_bet_tab,
                                                       width=200,
                                                       values=matches,
                                                       variable=choosed_match,
                                                       fg_color="gray")
list_of_matches_for_bets.grid(column=0, row=1, padx=60, pady=60)
list_of_users_for_bets = customtkinter.CTkOptionMenu(match_bet_tab,
                                                     width=200,
                                                     values=users,
                                                     variable=choosed_user,
                                                     fg_color="gray")
list_of_users_for_bets.grid(column=0, row=0, padx=60, pady=60)
matches_label_with_score_for_bets = customtkinter.CTkLabel(match_bet_tab,
                                                           text=user_matches,
                                                           font=('Tahoma', 15),
                                                           justify='right')
matches_label_with_score_for_bets.grid(column=3, row=0, padx=40)

score_entry_1 = customtkinter.CTkEntry(match_bet_tab,
                                       width=30,
                                       placeholder_text="0")
score_entry_1.grid(column=1, row=1)
score_entry_2 = customtkinter.CTkEntry(match_bet_tab,
                                       width=30,
                                       placeholder_text="0")
score_entry_2.grid(column=2, row=1)


def update_label():  # Gathering all new information and updating all content
    matches_with_score_up = ""
    users_with_score_up = ""
    matches_up = []
    users_up = []
    user_matches_up = f"{choosed_user.get()} bets:\n"
    for matches_d in EndedMatch.select():
        matches_with_score_up += matches_d.name + ": " + str(matches_d.left_score) + " : " + str(
            matches_d.right_score) + "\n"
        matches_up.append(matches_d.name)
    for all_users in User.select().order_by(-User.score):
        user_score = 0
        for score_for_user in UserBet.select().where(UserBet.owner_id == all_users.name):
            user_score += score_for_user.score_bet
        users_with_score_up += all_users.name + ": " + str(user_score) + "\n"
        users_up.append(all_users.name)
    for matches_dbn in UserBet.select().where(UserBet.owner_id == choosed_user.get()):
        user_matches_up += matches_dbn.match + ": " + str(matches_dbn.left_bet) + " : " + str(
            matches_dbn.right_bet) + "\n"
    matches_label_with_score.configure(text=matches_with_score_up)
    users_with_score_label.configure(text=users_with_score_up)
    list_of_matches.configure(values=matches_up)
    list_of_users.configure(values=users_up)
    list_of_matches_for_bets.configure(values=matches_up)
    list_of_users_for_bets.configure(values=users_up)
    matches_label_with_score_for_bets.configure(text=user_matches_up)
    list_of_matches_for_final_tab.configure(values=matches_up)


def update_bet_score():  # Change values in (user selected) bets.
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


def add_bet_score():  # Adding bet for (selected match) and (selected user)
    exist_check = UserBet.get_or_none(match=choosed_match.get(), owner=choosed_user.get())
    if exist_check is None:
        (UserBet.insert({
            UserBet.owner: str(choosed_user.get()),
            UserBet.match: str(choosed_match.get()),
            UserBet.score_bet: 0,
            UserBet.left_bet: int(score_entry_1.get()),
            UserBet.right_bet: int(score_entry_2.get())}).execute())
        update_label()
    else:
        print("This match already have user bet.")


def change_input():  # Change the final match score
    (EndedMatch
     .update(left_score=score_input_first.get())
     .where(EndedMatch.name == choose.get())
     .execute())
    (EndedMatch
     .update(right_score=score_input_second.get())
     .where(EndedMatch.name == choose.get())
     .execute())
    checking_score()
    update_label()


def add_users():  # Adding user to DB
    too_much_users = User.get_or_none(id=12)
    exist_check = User.get_or_none(name=add_user_entry.get())
    if too_much_users is None:  # That's 12th user?
        if exist_check is None:  # User already exist?
            User.create(name=add_user_entry.get(), score=0)
            update_label()
        else:
            print("Already existing.")
    else:
        print("You've added to much users.")


def delete_users():  # Deleting user from DB
    exist_check = User.get_or_none(name=choosed_user.get())
    if exist_check is not None:  # User already deleted?
        User.delete().where(User.name == choosed_user.get()).execute()
        UserBet.delete().where(UserBet.owner == choosed_user.get()).execute()
        update_label()
    else:
        print("User already deleted.")


def add_matches():
    too_much_matches = EndedMatch.get_or_none(id=12)
    exist_check = EndedMatch.get_or_none(name=add_match_entry.get())
    if too_much_matches is None:
        if exist_check is None:
            EndedMatch.create(name=add_match_entry.get(), left_score=0, right_score=0)
            update_label()
        else:
            print("Match is already added.")
    else:
        print("You've added too much matches.")


def delete_matches():
    exist_check = EndedMatch.get_or_none(name=choosed_match.get())
    if exist_check is not None:
        EndedMatch.delete().where(EndedMatch.name == choosed_match.get()).execute()
        update_label()
    else:
        print("Match already deleted")


# Adding buttons with entries which working commands from the upper section.
add_user_button = customtkinter.CTkButton(user_tab,
                                          text='Add User',
                                          command=add_users)  # Add user button
add_user_button.grid(column=1, row=0, padx=60, pady=0)

delete_user_button = customtkinter.CTkButton(user_tab,
                                             text='Delete User',
                                             command=delete_users,   # Delete user button
                                             fg_color="red")
delete_user_button.grid(column=1, row=1, padx=60, pady=0)

add_match_button = customtkinter.CTkButton(match_tab,
                                           text='Add Match',
                                           command=add_matches)  # Add match button
add_match_button.grid(column=1, row=0, padx=60, pady=0)

delete_match_button = customtkinter.CTkButton(match_tab,
                                              text='Delete Match',
                                              command=delete_matches,
                                              fg_color="red")  # Delete match button
delete_match_button.grid(column=1, row=1, padx=60, pady=0)

update_user_score_button = customtkinter.CTkButton(match_bet_tab,
                                                   text='Add Bet',
                                                   command=add_bet_score)  # Add user bet button
update_user_score_button.grid(column=3, row=1, padx=60, pady=0)

input_match_button = customtkinter.CTkButton(score_tab,
                                             text='Update Score',
                                             font=('Tahoma', 12),
                                             command=change_input)
input_match_button.grid(column=3, row=1, padx=60, pady=0)

root.mainloop()
