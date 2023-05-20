import sqlite3
from datetime import date

today = date.today()
Date = today.strftime("%y/%m/%d")
money=[]
count = 0
value = 0
ans =[]
u_id = 0

db = sqlite3.connect("atm.db")
cr = db.cursor()


#                                      add money at ATM
#                                    ========================

def adding_money():
    print("Enter count of coins and its value:")
    print("Enter 0 in any place if you finished.")
    count=int(input('conunt: '))
    value=int(input('value: '))
    while(count > 0 and value > 0):
        for i in range (1,count+1):
            money.append(value)
        print('DONE')
        count=int(input('conunt: '))
        value=int(input('value: '))

    print("\n===================================================================\n\n")

#                                       deposit function
#                                   ========================

def Deposit():
     # all availiable coins 
        coin=[5,10,20,50,100,200]
      # star from 200
        i = len(coin)-1
        deposit = int(input("Enter your money: "))
        x=deposit
        
        if(deposit%5==0):
            
        # list start by 0
            while ( i >= 0 ):
            
                # subtract coins from user's value to know how many coins it have and add to main money.
                while (x >= coin[i] ):
                    x -= coin[i]
                    money.append(coin[i])

                i-=1
            money.sort(reverse=True)
            # Set new value in DATABASE
            cr.execute(f"UPDATE atm SET balance = balance + {deposit}, last_deposit = '{Date}' WHERE user_id = {u_id}")

            print("DONE")

        else:
            print("Please, Enter an avaliable coins")

#                                    withdrawal function
#                                 ==============================


def Withdrawal():
    withdrawal = int(input("Enter the value you want to withdrawal: "))
    cr.execute(f"select balance from atm WHERE user_id = {u_id}")
    w = withdrawal
    # user_balance is tuple with an element and we need to access first item which it has user balance
    user_balance = cr.fetchone()

    # to access the user balance
    user_balance = user_balance[0]


    if (withdrawal > sum(money) ):
        print("money is not enough in ATM")

    elif(user_balance < withdrawal):
        print("your balance is not enough")

    else: 

        i = 0
        while ( i < len(money) ):

            while (withdrawal >= money[i] ):
                ans.append(money[i])
                withdrawal -= money[i]
                money.remove(money[i])
            if withdrawal == 0:
                break
            i+=1

        remainder = w - withdrawal

        if withdrawal > 0:
            print( "====================================")
            print( "|                                  |")
            print(f"|SORRY, we have not {withdrawal}             | ")
            print( "|                                  |")
            print( "====================================")


        tens = twenties = fifties = hundreds = Two_hundreds= 0

        tens =ans.count(10)
        twenties=ans.count(20)
        fifties=ans.count(50)
        hundreds=ans.count(100)
        Two_hundreds=ans.count(200)
        if (len(ans) <= 40 ):
            cr.execute(f"UPDATE atm SET balance = balance - {remainder}, last_withdrawal = '{Date}'  WHERE user_id = {u_id}")
            print(f"""
            {tens} from 10
            {twenties} from 20 
            {fifties} from 50
            {hundreds} from 100
            {Two_hundreds} from 200""")
        else:
            print(" more than 40 coins ")


#                                    information function
#                                  ==============================

def info():
    cr.execute(f"select * from atm where user_id = {u_id}")

    results = cr.fetchall()

    print("\t\t\t=================================")
    print(f"id => {results[0][0]} ,", end="\t")
    print(f"balance => {results[0][1]} ,",end ="\t")
    print(f"last deposit => {results[0][2]} ,",end ="\t")
    print(f"last withdrawal => {results[0][3]} ")
    print("\t\t\t=================================")




#                                           main
#       ======================================================================================

#BANK


adding_money()
money.sort(reverse=True)
#print(money)

#USER
u_id=int(input('Enter your ID: '))

cr.execute(f"select user_id from atm where user_id = {u_id}")
result = cr.fetchone()


#                               check if ID is exsist or not
#                           ======================================

if type(result) is tuple:
    if result[0] == u_id:
        
#                           check if PASSWOED is true or not
#                     ==============================================
        password = int(input("Enter password (4 digit): "))

        cr.execute(f"select password from atm where user_id = {u_id}")
        user_pass = cr.fetchone()

        if user_pass[0] == password:
            print("==================================")
            print("|                                |")
            print("|           AVAILABLE            |")
            print("|                                |")
            print("==================================")

#                     CODE if user id is available and password is true
#               ====================================================================
            act=int(input(""" What do you want: 
                  1) deposit
                  2) withdrawal
                  3) info about your account: 
                  """))

#                                       deposit الايداع
#                                  =========================

            if act == 1:
                Deposit()

#                                     withdrawal السحب
#                               ============================

            elif act == 2:
                Withdrawal()

#                               info about your account معلومات حول الحساب
#                           ==================================================

            elif act == 3:
                info()

            else:
                print('ERROR, try again with true value.')
        
        else:
            print("\t\t\t=======================")
            print("\t\t\t| enter true password |")
            print("\t\t\t=======================")

           

else:
        print("\t\t\t=================")
        print("\t\t\t| not available |")
        print("\t\t\t=================")

#Save (Commit) Changes
db.commit()

#Close Database
db.close()