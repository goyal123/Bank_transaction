from flask import Flask,render_template,request
import random
import pandas as pd
import os
import io
import webbrowser
import json
from datetime import datetime 
app = Flask(__name__)


@app.route("/transactions/<user_date>",methods=['GET']) 
def fun(user_date):
    df = pd.read_json("bankAccountdde24ad.json")
    account_no=df["Account No"].tolist()
    #print(account_no[0])
    account=[]
    Transaction_Details=df["Transaction Details"].tolist()
    transaction=[]
    #print(Transaction_Details[0])
    Deposit_AMT=df["Deposit AMT"].tolist()
    deposit=[]               
    date_no=df["Date"].tolist()
    #print(ldate_no))
    date=[]
    Withdrawal_AMT=df["Withdrawal AMT"].tolist()
    withdraw=[]
    Balance_AMT=df["Balance AMT"].tolist()
    balance=[]
    
    
    message=''
    user_guess=user_date
    #months = ["Jan", "Feb", "March", "April", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
    res = user_guess.split("-")
        #print(type(res[0]))
    day=res[0]
    month=res[1]
        #print(type(month))
    year='20'+res[2]

    isValidDate = True
    try:
        datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False

    if(isValidDate):
        print("Input date is valid ..")
    else:
        return 'Please Enter correct date format'
        
    final_date=year+'-'+res[1]+'-'+res[0]
    print(final_date)
    #print(user_guess)
    
    j=0

    for i in range(len(date_no)):
        if str(date_no[i].date())==final_date:
            account.append(account_no[i])
            date.append(date_no[i].date())
            deposit.append(Deposit_AMT[i])
            withdraw.append(Withdrawal_AMT[i])
            transaction.append(Transaction_Details[i])
            balance.append(Balance_AMT[i])
                

    return render_template("game_over.html",len = len(account),account=account,date=date,transaction=transaction,withdraw=withdraw,deposit=deposit,balance=balance)
                
            
@app.route("/balance/<user_date>",methods=['GET']) 
def balance(user_date):
    df = pd.read_json("bankAccountdde24ad.json")
    print(type(df))
    account_no=df["Account No"].tolist()
    #print(account_no[0])
    account=[]
    Transaction_Details=df["Transaction Details"].tolist()
    transaction=[]
    #print(Transaction_Details[0])
    Deposit_AMT=df["Deposit AMT"].tolist()
    deposit=[]               
    date_no=df["Date"].tolist()
    #print(len(date_no))
    date=[]
    Withdrawal_AMT=df["Withdrawal AMT"].tolist()
    withdraw=[]
    Balance_AMT=df["Balance AMT"].tolist()
    balance=[]
    
    
    message=''
    user_guess=user_date
    #print(user_guess)
    res = user_guess.split("-")
    day=res[0]
    month=res[1]
    year='20'+res[2]
    final_date=year+'-'+res[1]+'-'+res[0]
    j=0

    isValidDate = True
    try:
        datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False

    if(isValidDate):
        print("Input date is valid ..")
    else:
        return 'Please Enter correct date format'

    for i in range(len(date_no)):
        if str(date_no[i].date())==final_date:
            account.append(account_no[i])
            date.append(date_no[i].date())
            deposit.append(Deposit_AMT[i])
            withdraw.append(Withdrawal_AMT[i])
            transaction.append(Transaction_Details[i])
            balance.append(Balance_AMT[i])

    b_acc=account[len(account)-1]
    b_date=date[len(date)-1]
    b_deposit=deposit[len(deposit)-1]
    b_withdraw=withdraw[len(withdraw)-1]
    b_transaction=transaction[len(transaction)-1]
    b_balance=balance[len(balance)-1]
                

    return render_template("balance.html",len = len(account),account=b_acc,date=b_date,transaction=b_transaction,withdraw=b_withdraw,deposit=b_deposit,balance=b_balance)
                       

@app.route("/add",methods=['GET','POST'])
def add():
    message=''
    df = pd.read_json("bankAccountdde24ad.json")
    date_no=df["Date"].tolist()
    if request.method=='POST':
        form=request.form
        account=form['acnt']
        trans_det=str(form['t_det'])
        deposit=form['credit']
        withdraw=int(str(form['withdraw']))
        credit=int(str(form['credit']))
        user_guess=form['fname']
        print(user_guess)
        months = ["Jan", "Feb", "March", "April", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        res = user_guess.split("-")
        #print(type(res[0]))
        day=int(res[2])
        month=months[int(res[1])-1]
        #print(type(month))
        year=int(res[0])
        final_date=res[2]+' '+month+' '+res[0][2::]
        print(final_date)

        if(withdraw==0 and credit==0):
            return render_template("add.html",message='Please Enter Deposit/Withdrawl value')
        

        
        with open("bankAccountdde24ad.json", "r+") as file:
            data = json.load(file)
            #date_no=data["Date"].tolist()
            
            #print(type(data))
            data=sorted(data,key=lambda k: datetime.strptime(k['Date'],'%d %b %y'))
            flag=0
            for i in reversed(range(len(data))):
                if str(date_no[i].date())==user_guess:
                    print("yes")
                    balance=data[i]['Balance AMT']
                    print("bal:",balance)
                    flag=1
                    break
            if flag==0:
                balance=data[-1]['Balance AMT']
            if ".00" in balance:
                sum1=balance.replace(".00","")
            else:
                sum1=balance
            if "," in sum1:
                sum2=sum1.replace(",","")
            else:
                sum2=sum1
            
            net_balance=int(sum2)+credit-withdraw
            print(net_balance)
            #print(type(data[-1]['Balance AMT']))
            y={"Account No":account,"Date":final_date,"Transaction Details":trans_det,"Value Date":final_date,"Withdrawal AMT":withdraw,"Deposit AMT":credit,"Balance AMT":str(net_balance)}
#,"Balance AMT":balance
            data.append(y)
            data=sorted(data,key=lambda k: datetime.strptime(k['Date'],'%d %b %y'))
            file.close()
        with open("bankAccountdde24ad.json", "w") as file:
            #data=sorted(data,key=lambda k: k['Date'],reverse=True)
            json.dump(data,file)
            #print(data)
            file.close()
    return render_template("add.html")
  

@app.route("/")
def index():
    if request.method=='POST':
        form=request.form
        user_guess=form['fbut']
        print(user_guess)
        
    return render_template("guess.html")


if __name__ == "__main__":
    app.run()
    
