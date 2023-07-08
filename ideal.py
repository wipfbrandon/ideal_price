# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 12:27:42 2023

@author: wipfb
"""
import streamlit as st
import pandas as pd

@st.cache_data
def ideal_price(listPrice=1, units=1, estRentUnit=1, squareFeet=1, tax=1, ins=1, rate=0.07, term=20, ni_th=2000, npm_th=5, pct_th=1, coc_th=5):
    df = pd.DataFrame()
    df['Price'] = 0
    df['IdealOffer'] = [x for x in range(listPrice, listPrice - 50_000, -2_000)]
    df['Price'] = listPrice
    df['Diff'] = df.IdealOffer - df.Price
    df['DiffPct'] = (round(df.Diff / df.Price, 3) * 100)
    df.DiffPct = round(df.DiffPct,2).astype(str) + '%'
    df['Rent'] = estRentUnit
    df['DownPay'] = (df.IdealOffer * 0.20).astype(int)
    df['Loan'] = df.IdealOffer - df.DownPay
    df['CloseCost'] = df.IdealOffer * 0.01
    df['CashToClose'] = (df.DownPay + df.CloseCost).astype(int)
    df['SquareFeet'] = squareFeet
    df['SquareFtUnit'] = df.SquareFeet / units
    df['OfferSqFt'] = round(df.IdealOffer / df.SquareFeet, 2)
    df['RentSqtFt'] = round(df.Rent / df.SquareFtUnit, 2)
    df['RentTotal'] = df.Rent * units
    df['GAR'] = df.RentTotal * 12
    df['LnPmt'] = round((rate/12) * (1/(1-(1+rate/12)**(-term*12))) * df.Loan, 0)

    if tax == 1:
        df['Tax'] = df.IdealOffer * 0.02 #Assuming 2% of List Offer
    else:
        df['Tax'] = tax

    if ins == 1:
        df['Ins'] = df.IdealOffer * 0.005 #Assuming 0.5% of List Offer
    else:
        df['Ins'] = ins

    df['FixedExp'] = (df.LnPmt * 12 + df.Tax + df.Ins).astype(int)
    df['VarExp'] = (df.GAR * 0.15).astype(int) #Assuming 15% of Gross Annual Rents
    df['TotalExp'] = (df.FixedExp + df.VarExp).astype(int)
    df['NetInc'] = (df.GAR - df.TotalExp).astype(int)
    df['NPM'] = round((df.NetInc / df.GAR) * 100, 2)
    df['OnePctTest'] = round((df.RentTotal / df.IdealOffer) * 100, 2)
    df['CoCROI'] = round((df.NetInc / df.CashToClose) * 100, 2)

    #Set Threshold flag for Measures meeting Min Requirements
    df['NetInc_TH'] = [1 if x > ni_th else 0 for x in df.NetInc]
    df['NPM_TH'] = [1 if x > npm_th else 0 for x in df.NPM]
    df['OnePctTest_TH'] = [1 if x >= pct_th else 0 for x in df.OnePctTest]
    df['CoCROI_TH'] = [1 if x > coc_th else 0 for x in df.CoCROI]
    df['TH_Total'] = df.NetInc_TH + df.NPM_TH + df.OnePctTest_TH + df.CoCROI_TH

    df['NetInc'] = [f'{str(x)}' if x > ni_th else f'{str(x)} (F)' for x in df.NetInc]
    df['NPM'] = [f'{str(x)}%' if x > npm_th else f'{str(x)}% (F)' for x in df.NPM]
    df['OnePctTest'] =  [f'{str(x)}%' if x >= pct_th else f'{str(x)}% (F)' for x in df.OnePctTest]
    df['CoCROI'] = [f'{str(x)}%' if x > coc_th else f'{str(x)}% (F)' for x in df.CoCROI]

    return df

@st.cache_data
def ideal_rent(listPrice=1, units=1, estRentUnit=1, squareFeet=1, tax=1, ins=1, rate=0.07,term=20, ni_th=2000, npm_th=5, pct_th=1, coc_th=5):
    df = pd.DataFrame()
    minRent = int(round(estRentUnit * 0.75, 0))
    df['Price'] = 1
    df['Rent'] = 1
    df['IdealRent'] = [x for x in range(minRent, estRentUnit, 10)]
    df.Rent = estRentUnit
    df.Price = int(listPrice)
    df['Diff'] = df.IdealRent - df.Rent
    df['DownPay'] = (df.Price * 0.20)
    df['Loan'] = df.Price - df.DownPay
    df['CloseCost'] = df.Price * 0.01
    df['CashToClose'] = (df.DownPay + df.CloseCost)
    df['SquareFeet'] = squareFeet
    df['SquareFtUnit'] = df.SquareFeet / units
    df['OfferSqFt'] = round(df.Price / df.SquareFeet, 2)
    df['RentSqtFt'] = round(df.IdealRent / df.SquareFtUnit, 2)
    df['RentTotal'] = df.IdealRent * units
    df['GAR'] = df.RentTotal * 12
    df['LnPmt'] = round((rate/12) * (1/(1-(1+rate/12)**(-term*12))) * df.Loan, 0)

    if tax == 1:
        df['Tax'] = df.Price * 0.02 #Assuming 2% of List Offer
    else:
        df['Tax'] = tax

    if ins == 1:
        df['Ins'] = df.Price * 0.005 #Assuming 0.5% of List Offer
    else:
        df['Ins'] = ins

    df['FixedExp'] = (df.LnPmt * 12 + df.Tax + df.Ins)
    df['VarExp'] = (df.GAR * 0.15) #Assuming 15% of Gross Annual Rents
    df['TotalExp'] = (df.FixedExp + df.VarExp)
    df['NetInc'] = (df.GAR - df.TotalExp)
    df['NPM'] = round((df.NetInc / df.GAR) * 100, 2)
    df['OnePctTest'] = round((df.RentTotal / df.Price) * 100, 2)
    df['CoCROI'] = round((df.NetInc / df.CashToClose) * 100, 2)

    #Set Threshold flag for Measures meeting Min Requirements
    df['NetInc_TH'] = [1 if x > ni_th else 0 for x in df.NetInc]
    df['NPM_TH'] = [1 if x > npm_th else 0 for x in df.NPM]
    df['OnePctTest_TH'] = [1 if x >= pct_th else 0 for x in df.OnePctTest]
    df['CoCROI_TH'] = [1 if x > coc_th else 0 for x in df.CoCROI]
    df['TH_Total'] = df.NetInc_TH + df.NPM_TH + df.OnePctTest_TH + df.CoCROI_TH

    df['NetInc'] = [f'{str(x)}' if x > ni_th else f'{str(x)} (F)' for x in df.NetInc]
    df['NPM'] = [f'{str(x)}%' if x > npm_th else f'{str(x)}% (F)' for x in df.NPM]
    df['OnePctTest'] =  [f'{str(x)}%' if x >= pct_th else f'{str(x)}% (F)' for x in df.OnePctTest]
    df['CoCROI'] = [f'{str(x)}%' if x > coc_th else f'{str(x)}% (F)' for x in df.CoCROI]

    return df


#%% STREAMLIT OUTPUT
listPrice = st.sidebar.number_input('Purchase Price',min_value=1, value=200000)
units = st.sidebar.number_input('Number of Units',min_value=1, value=2)
maxRents = st.sidebar.number_input('Maximum Rent / Unit',min_value=1, value=750)
squareFeet = st.sidebar.number_input('Square Feet (Total)',min_value=1, value=1000)
taxes = st.sidebar.number_input('Taxes',min_value=1, value=500)
insurance = st.sidebar.number_input('Insurance',min_value=1, value=500)


#%% CALCULATE
df_price = ideal_price(listPrice=listPrice, units=units, estRentUnit=maxRents, squareFeet=squareFeet, tax=taxes, ins=insurance, ni_th=2000, npm_th=5, pct_th=1, coc_th=5)
df_ideal_price = df_price[(df_price.TH_Total == df_price.TH_Total.max())]
df_second_price = df_price[(df_price.TH_Total == (df_price.TH_Total.max() - 1))].head(1)

price_final = df_ideal_price[['Price','IdealOffer','Diff','DiffPct','Rent','DownPay','CashToClose',
          'OfferSqFt','RentSqtFt','GAR','FixedExp','VarExp','TotalExp','NetInc',
          'NPM','OnePctTest','CoCROI','TH_Total'
          ]].head(1).reset_index()

price_final = price_final.rename(index={0:'IDEAL'})

df_rent = ideal_rent(listPrice=listPrice, units=units, estRentUnit=maxRents, squareFeet=squareFeet, tax=taxes, ins=insurance, ni_th=2000, npm_th=5, pct_th=1, coc_th=5)

df_first_rent = df_rent[(df_rent.TH_Total == df_rent.TH_Total.max())].head(1)
df_second_rent = df_rent[(df_rent.TH_Total == (df_rent.TH_Total.max() - 1))].head(1)

df_ideal_rent = pd.concat([df_first_rent, df_second_rent], axis=0, ignore_index=True)

rent_final = df_ideal_rent[['Price','IdealRent','Diff','DownPay','CashToClose',
         'OfferSqFt','RentSqtFt','GAR','FixedExp','VarExp','TotalExp','NetInc',
         'NPM','OnePctTest','CoCROI','TH_Total']].reset_index()

rent_final = rent_final.rename(index={0:'IDEAL', 1:'MAYBE'})

#%% BUILD PAGE

st.title('Ideal Price and Rents')

f'The Ideal Price is {df_ideal_price.head(1)["IdealOffer"].iloc[0]}... if Rents are actually {maxRents} per Unit.'
f'The Ideal Rent is ${df_first_rent.head(1)["IdealRent"].iloc[0]} per Unit... if the Purchase Price is actually {listPrice}.'


"""
---
Ideal Price:
"""
st.dataframe(price_final)
st.caption('_(F) denotes threshold was NOT met._')

'''
---
Ideal Rents
'''
st.dataframe(rent_final)
st.caption('_(F) denotes threshold was NOT met._')
