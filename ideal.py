# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 12:27:42 2023

@author: wipfb
"""
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Ideal Rents",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Author': 'Brandon Wipf',
    }
)

@st.cache_data
def ideal_price(listPrice=1, units=1, estRentUnit=1, squareFeet=1, tax=1, ins=1, rate=0.07, term=20, varExpPct=15.0, ni_th=2000, npm_th=5, pct_th=1, coc_th=5):
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
    df['LnPmt'] = round(((rate/100)/12) * (1/(1-(1+(rate/100)/12)**(-term*12))) * df.Loan, 0)

    if tax == 1:
        df['Tax'] = df.IdealOffer * 0.02 #Assuming 2% of List Offer
    else:
        df['Tax'] = tax

    if ins == 1:
        df['Ins'] = df.IdealOffer * 0.005 #Assuming 0.5% of List Offer
    else:
        df['Ins'] = ins

    df['FixedExp'] = (df.LnPmt * 12 + df.Tax + df.Ins).astype(int)
    df['VarExp'] = (df.GAR * (varExpPct/100)).astype(int) #Assuming 15% of Gross Annual Rents
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
def ideal_rent(listPrice=1, units=1, estRentUnit=1, squareFeet=1, tax=1, ins=1, rate=0.07,term=20, varExpPct=15.0, ni_th=2000, npm_th=5, pct_th=1, coc_th=5):
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
    df['LnPmt'] = round(((rate/100)/12) * (1/(1-(1+(rate/100)/12)**(-term*12))) * df.Loan, 0)

    if tax == 1:
        df['Tax'] = df.Price * 0.02 #Assuming 2% of List Offer
    else:
        df['Tax'] = tax

    if ins == 1:
        df['Ins'] = df.Price * 0.005 #Assuming 0.5% of List Offer
    else:
        df['Ins'] = ins

    df['FixedExp'] = (df.LnPmt * 12 + df.Tax + df.Ins)
    df['VarExp'] = (df.GAR * (varExpPct/100)) #Assuming 15% of Gross Annual Rents
    df['TotalExp'] = (df.FixedExp + df.VarExp)
    df['NetInc'] = (df.GAR - df.TotalExp).astype(int)
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
st.sidebar.write('PROPERTY DETAILS')
listPrice = st.sidebar.number_input('Purchase Price',min_value=1, value=200000, step=10000, help='Enter what you would pay, not the List Price')
units = st.sidebar.number_input('Number of Units',min_value=1, value=2, step=1)
maxRents = st.sidebar.number_input('Maximum Rent / Unit',min_value=1, value=750, step=50, help='If Units differ, enter Average')
squareFeet = st.sidebar.number_input('Square Feet (Total)',min_value=1, value=1000, step=100, help='Total Square Footage of Property')
taxes = st.sidebar.number_input('Taxes',min_value=1, value=500, step=100)
insurance = st.sidebar.number_input('Insurance',min_value=1, value=500, step=500, help='Best Guess')
st.sidebar.write('---')
st.sidebar.write('ASSUMPTIONS')
rate = st.sidebar.number_input('Interest Rate %', min_value=0.1, value=7.0, step=0.1, help='Interest Rate as whole number')
term = st.sidebar.number_input('Loan Term',min_value=1, max_value=30, value=20, step=5, help='Loan Term in Years')
var_exp_rt = st.sidebar.number_input('Variable Expense Rate %', min_value=0.1, value=15.0, step=0.1, help='Percentage of GAR (vacancy + repairs + capex)')
st.sidebar.write('---')
st.sidebar.write('THRESHOLDS')
incomeTH = st.sidebar.number_input('Net Income Threshold ($)',min_value=1, value=2000, step=500, help='Gross Annual Rents - Total Expenses')
npmTH = st.sidebar.number_input('Net Profit Margin Threshold (%)', min_value=1.00, value=5.00, step=0.1, help='Net Income / Gross Annual Rents')
onePctTH = st.sidebar.number_input('One Pct Test Threshold (%)',min_value=0.00, value=1.00, step=0.01, help='Annual Rents / Price')
cocroiTH = st.sidebar.number_input('CoCROI Threshold (%)',min_value=1.00, value=5.00, step=0.1, help='Net Income / Cash In')

#%% CALCULATE
df_price = ideal_price(listPrice=listPrice, units=units, estRentUnit=maxRents, squareFeet=squareFeet, tax=taxes, ins=insurance, rate=rate, term=term, varExpPct=var_exp_rt, ni_th=incomeTH, npm_th=npmTH, pct_th=onePctTH, coc_th=cocroiTH)
df_ideal_price = df_price[(df_price.TH_Total == df_price.TH_Total.max())]
df_second_price = df_price[(df_price.TH_Total == (df_price.TH_Total.max() - 1))].head(1)

price_final = df_ideal_price[['IdealOffer','Price','Diff','DiffPct','TH_Total','NetInc','NPM','OnePctTest','CoCROI', 'Rent','DownPay','CashToClose',
                              'OfferSqFt','RentSqtFt','GAR','FixedExp','VarExp','TotalExp']].head(1).reset_index(drop=True)

price_final = price_final.rename(index={0:'IDEAL'})

df_rent = ideal_rent(listPrice=listPrice, units=units, estRentUnit=maxRents, squareFeet=squareFeet, tax=taxes, ins=insurance, rate=rate, term=term, varExpPct=var_exp_rt, ni_th=incomeTH, npm_th=npmTH, pct_th=onePctTH, coc_th=cocroiTH)

df_first_rent = df_rent[(df_rent.TH_Total == df_rent.TH_Total.max())].head(1)
df_second_rent = df_rent[(df_rent.TH_Total == (df_rent.TH_Total.max() - 1))].head(1)

df_ideal_rent = pd.concat([df_first_rent, df_second_rent], axis=0, ignore_index=True)

rent_final = df_ideal_rent[['Price','IdealRent','Diff', 'TH_Total', 'NetInc', 'NPM','OnePctTest','CoCROI','DownPay','CashToClose',
                            'OfferSqFt','RentSqtFt','GAR','FixedExp','VarExp','TotalExp']].reset_index(drop=True)

rent_final = rent_final.rename(index={0:'IDEAL', 1:'MAYBE'})

idealPrice = '${:,.0f}'.format(int(df_ideal_price.head(1)["IdealOffer"].iloc[0]))
idealRent = '${:,.0f}'.format(df_first_rent.head(1)["IdealRent"].iloc[0])
maxRentFormat = '${:,.0f}'.format(int(maxRents))
listPriceFormat = '${:,.0f}'.format(listPrice)

idealPriceText = f'The Ideal Price is {df_ideal_price.head(1)["IdealOffer"].iloc[0]}, if Rents are actually {maxRents} per Unit.'
idealRentText = f'The Ideal Rent is {df_first_rent.head(1)["IdealRent"].iloc[0]} per Unit, if the Purchase Price is actually {listPrice}'

#%% BUILD PAGE
tab1, tab2 = st.tabs(["ANALYSIS", "THRESHOLDS"])
with tab1:
    st.title('Ideal Price and Rents')
    
    if price_final.head(1)["TH_Total"].iloc[0] == 4:
        st.write(idealPriceText)
    else:
        'This Price is too HIGH!'
    
    if rent_final.head(1)["TH_Total"].iloc[0] == 4:
        st.write(idealRentText)
    else:
        'These Rents are too LOW!'
    
    """
    ---
    Ideal Price Data Table:
    """
    if price_final.head(1)["TH_Total"].iloc[0] < 4:
        st.write('THIS SCENARIO DOES NOT WORK!')
    else:
        st.dataframe(price_final)
        st.caption('_(F) denotes threshold was NOT met._')
    
    '''
    ---
    Ideal Rents Data Table:
    '''
    if rent_final.head(1)["TH_Total"].iloc[0] < 4:
        st.write('THIS SCENARIO DOES NOT WORK!')
    else:
        st.dataframe(rent_final)
        st.caption('_(F) denotes threshold was NOT met._')

with tab2:
    """
    ---
    THRESHOLDS (FLOORS) SET FOR THIS SCENARIO:
    """
    st.caption('Net Income: ' '${:,.0f}'.format(incomeTH))
    st.caption(f'Net Profit Margin: {round(npmTH, 2)}%')
    st.caption(f'One Percent Test: {round(onePctTH, 2)}%')
    st.caption(f'CoC ROI: {round(cocroiTH, 2)}%')
