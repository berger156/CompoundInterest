# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 06:43:34 2019

@author: Andy
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

class account:
    _registry = []
    
    @classmethod
    def listAccounts(cls):
        for acct in cls._registry:
            print(acct.name)
            
    @classmethod
    def plotAccounts(cls, noYears, *acctType):
        t = np.linspace(0, noYears)
        
        fig, ax = plt.subplots()
        fmt = '${x:,.0f}'
        tick = mtick.StrMethodFormatter(fmt)
        ax.yaxis.set_major_formatter(tick)
        ax.set_xlabel("Years")
        ax.set_ylabel("Balance") 
        
        if len(acctType):
            matchingType = acctType[0]
            for acct in cls._registry:
                if acct.accountType == matchingType:
                    plt.plot(t, acct.calcBalance(t))
        else: # plot all account types
            for acct in cls._registry:
                plt.plot(t, acct.calcBalance(t))
                
        plt.show()
        
    @classmethod
    def stackAccounts(cls, noYears):
        t = np.linspace(0, noYears)
        
        fig, ax = plt.subplots()
        fmt = '${x:,.0f}'
        tick = mtick.StrMethodFormatter(fmt)
        ax.yaxis.set_major_formatter(tick)
        ax.set_xlabel("Years")
        ax.set_ylabel("Balance") 
        
        # create a dummy account that always holds zero balance, being sure to avoid divide-by-zeros
        prev_acct = account("zeros", "savings", 0, 1, 0, 12, 0, 0) 
        for acct in cls._registry:
            ax.fill_between(t, acct.calcBalance(t) + prev_acct.calcBalance(t), prev_acct.calcBalance(t))
            prev_acct = acct

        del prev_acct
        plt.show()
            
    numberOfAccounts = 0
    
    acctTypes = ('savings','investment')
    
    def __init__(self, name, accountType, principal, APR, APRvar, compPerYear, contribution, contPerYear):
        
        self.name = name
        self.accountType = accountType
        self.principal = principal
        self.APR = APR
        self.APRvar = APRvar
        self.compPerYear = compPerYear #number of compounding periods per year
        self.contribution = contribution
        self.contPerYear = contPerYear #number of contributions per year
        
        if accountType not in self.acctTypes:
            raise ValueError("%s is not a valid account type." % accountType)
        
        if (principal < 0):
            raise ValueError("Principal must be a positive number")
        
        self._registry.append(self)
        type(self).numberOfAccounts += 1
    
    def __del__(self):
        self._registry.insert(0,self)
        if type(self).numberOfAccounts > 0:
            type(self).numberOfAccounts -= 1
        
    def calcBalance(self,noYears,variance=0):
        P = self.principal
        r = (self.APR + variance)/100
        n = self.compPerYear
        t = noYears
        c = self.contribution*self.contPerYear/self.compPerYear
        
        balance = P*(1 + r/n)**(n*t) + c*((1 + r/n)**(n*t + 1) - (1 + r/n))/(r/n)
        
        return balance
    
    def plotAccount(self,noYears):
        t = np.linspace(0, noYears)
        
        #accountGraph = plt.figure()
        
        fig, ax = plt.subplots()
        fmt = '${x:,.0f}'
        tick = mtick.StrMethodFormatter(fmt)
        ax.yaxis.set_major_formatter(tick)
        ax.plot(t, self.calcBalance(t))
        ax.set_xlabel("Years")
        ax.set_ylabel("Balance")   
        
        if(self.APRvar != 0):
            ax.plot(t, self.calcBalance(t, self.APRvar),linestyle='dashed')
            ax.plot(t, self.calcBalance(t, -self.APRvar),linestyle='dashed')
            ax.legend(('nominal','best case','worst case'))
         
        plt.show()
        #return ax