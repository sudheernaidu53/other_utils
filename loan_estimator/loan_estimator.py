# This file is to get a rough estimation of how much you need to pay or how many months you need to pay for a loan

import pandas as pd
import numpy as np
from IPython.display import display

def group(number):
    """show money in laks and crores (indian way of presenting money)"""
    s = '%d' % number
    groups = []
    groups.append(s[-3:])
    s = s[:-3]
    while s and s[-1].isdigit():
        groups.append(s[-2:])
        s = s[:-2]
    return s + ','.join(reversed(groups))


class loan:
    def __init__(self, R=8.1, principal=30, years=5):
        """R is yearly interest
        principal is principal amount in lakhs
        years = number of years
        """
        self.R = R * 0.01
        self.r = R * 0.01 * (1 / 12)
        self.principal = principal * 100000
        self.years = years
        self.num_months = self.years * 12
        self.months = {"Jan": 31, "Feb": 28, "Mar": 31, "Apr": 30, "May": 31, "June": 30, "Jul": 31, "Aug": 31,
                       "Sep": 30, "Oct": 31, "Nov": 30, "Dec": 31}

    def find_monthly_emi_flat(self, print_=True):
        """ find how much emi need to be paid given some principal, interest, and number of months when the interest scheme is flat"""

        total = self.principal * (1 + self.R * (self.num_months / 12))
        if print_:
            print("------------- flat interest -------------------")
            print("total amount you are paying over full period:", total)
            print("monthly installment/emi : {}".format(total / self.num_months))
        return total, total / self.num_months

    def num_months_emi_diminishing(self, emi, principal=0, interest=0, print_=True):
        """find the number of months you need to pay for, if you are paying emi every month"""
        """emi is in rupees, principal is in lakhs, interest is yearly interest"""
        """n = np.log((E/r)/(E/r -P))/np.log(1+r) """

        if not principal:
            principal = self.principal
        if not interest:
            interest = self.r
        num_months = np.log((emi / interest) / (emi / interest - principal)) / np.log(1 + interest)
        if print_:
            print("------------- diminishing interest -------------------")
            print("you need to pay {} monthly, for {} months".format(emi, num_months))
        return num_months

    def find_monthly_emi_diminishing(self, num_months=0, principal=0, print_=True):
        """ find how much emi need to be paid given some principal, interest, and number of months when the interest scheme is flat"""
        """P*r*(1 + 1/(np.power(1+r,60)-1))"""

        if not num_months:
            num_months = self.num_months
        if not principal:
            principal = self.principal
        else:
            principal *= 100000
        monthly_emi = principal * self.r * (1 + 1 / (np.power(1 + self.r, num_months) - 1))
        if print_:
            print("------------- diminishing interest -------------------")
            print(" you need to pay {} monthly, for {} months".format(monthly_emi, num_months))
            print("total amount you will pay over full period is roughly {}".format(monthly_emi * num_months))
        return monthly_emi

    def confirm_diminishing(self, emi, print_=False):
        """ function to confirm if the interest scheme is dimishing"""
        principal = self.principal
        i = 1
        while principal > 0:
            principal += ((self.r) * principal - emi)
            if print_:
                print(i, principal)
            i += 1
        if abs(principal / self.principal) < 0.001:
            print("final net amount is {} after {} months".format(principal, i - 1))
        return principal, i


## Usage
R = 10.5 #10.5 % monthly interest rate
principal = 30 # principal is 30 lakhs
years = 4.5 # loan term period is 4.5 years
loan1 = loan(R,principal,years) # initialize a loan instance

loan1.find_monthly_emi_flat()
loan1.num_months_emi_diminishing(35000)
loan1.find_monthly_emi_diminishing()

#-----------output-----------------------
# ------------- flat interest -------------------
# total amount you are paying over full period: 4417500.0
# monthly installment/emi : 81805.55555555556
# ------------- diminishing interest -------------------
# you need to pay 35000 monthly, for 159.1257820098328 months
# ------------- diminishing interest -------------------
#  you need to pay 69948.58010333449 monthly, for 54.0 months
# total amount you will pay over full period is roughly 3777223.3255800623

def get_df():
    # make a table to find how much emi to be paid for different principals over different tenure/periods

    loan1 = loan(10.5,principal = 30, years =5)
    # print(loan1.find_monthly_emi_diminishing())

    years = [2,3,4,5]
    amounts = [15,20,25]
    yearss = [str(x)+'y' for x in years]
    df = pd.DataFrame(columns=yearss)
    total = pd.DataFrame(columns = yearss)
    for amount in amounts:
        arr=[]
        arr1 = []
        for year in years:
            temp = loan1.find_monthly_emi_diminishing(num_months=year*12, principal=amount,print_ = False)
            arr.append(group(round(int(temp),-2))) # rounding to closest hundred
            arr1.append(group(round(int(temp*year*12),-2)))
        df.loc[str(amount)+'Lks']=arr
        total.loc[str(amount)+'Lks']=arr1

    print("--------------------- emi ------------------")
    display(df)

    print("---------------------- total ---------------------")
    display(total)

# get_df()