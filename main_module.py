import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from yahoo_fin.stock_info import *

def portfolio_allo(C1,C2,C3,C4,C5,C6,C7,C8,amt):


    print("data1")
    # aapl.iloc[0]['Adj. Close']
    for stock_df in (C1,C2,C3,C4,C5,C6,C7,C8):
        stock_df['Normed Return'] = stock_df['adjclose']/stock_df.iloc[0]['adjclose']
    
    print("d2")
    #allocation
    
    for stock_df,allo in zip([C1,C2,C3,C4,C5,C6,C7,C8],[.1, .1, .1, .1, .1, .1, .2, .2]):
        stock_df['Allocation'] = stock_df['Normed Return'] * allo
    
    print("d3")
    
    for stock_df in [C1,C2,C3,C4,C5,C6,C7,C8]:
        stock_df['Position Values'] = stock_df['Allocation'] * int(amt)
   
    print("d4")
   
    portfolio_val = pd.concat([C1['Position Values'],
    C2['Position Values'],C3['Position Values'],
    C4['Position Values'],C5['Position Values'],
    C6['Position Values'],C7['Position Values'],
    C8['Position Values']],axis=1)
    print("d5")



    portfolio_val.columns = ["C1_pos","C2_pos","C3_pos","C4_pos","C5_pos","C6_pos","C7_pos","C8_pos"]

    portfolio_val['Total Pos'] = portfolio_val.sum(axis=1)

    portfolio_val['Total Pos'].plot(figsize=(10,8))
    # plt.title('Total Portfolio Value')
    plt.savefig("static/total_portfolio_value_g1.png")

    portfolio_val.drop('Total Pos',axis=1).plot(kind='line')

    plt.savefig("static/portfolio_value_drop_g2.png")
    trash=10
    return trash



def insert_values(a,b,c,d,e,f,g,h,amt):
    C1=get_data('a')
    C2=get_data('b')
    C3=get_data('c')
    C4=get_data('d')
    C5=get_data('e')
    C6=get_data('f')
    C7=get_data('g')
    C8=get_data('h')

    

    stocks=pd.concat([C1['close'],C2['close'],C3['close'],C4['close'],C5['close'],C6['close'],C7['close'],C8['close']],axis=1,sort=True)
    stocks.columns=['C1','C2','C3','C4','C5','C6','C7','C8']

    garb_value = portfolio_allo(C1,C2,C3,C4,C5,C6,C7,C8,amt)

    # findind the mean value
    mean_daily_ret = stocks.pct_change(1).mean()
    stocks.pct_change(1).corr()
    
    #Normalize Data
    stock_normed = stocks/stocks.iloc[0]
    stock_normed.plot()
    plt.savefig("static/stock_normed_g3.png")

    #Daily return
    stock_daily_ret = stocks.pct_change(1)

    #log Return/Sharp Ratio
    log_ret = np.log(stocks/stocks.shift(1))
    log_ret.hist(bins=100,figsize=(12,6));
    plt.savefig("static/Sharp_Value_g4.png")

    log_ret.describe().transpose()
    log_ret.mean() * 252

    # Compute pairwise covariance of columns
    log_ret.cov()

    log_ret.cov()*252 # multiply by days


    # Set seed (optional)
    np.random.seed(101)
    
    # Stock Columns
    print('Stocks')
    print(stocks.columns)
    print('\n')
    
    # Create Random Weights
    print('Creating Random Weights')
    weights = np.array(np.random.random(8))
    print(weights)
    print('\n')
    
    # Rebalance Weights
    print('Rebalance to sum to 1.0')
    weights = weights / np.sum(weights)
    print(weights)
    print('\n')
    
    # Expected Return
    print('Expected Portfolio Return')
    exp_ret = np.sum(log_ret.mean() * weights) *252
    print(exp_ret)
    print('\n')
    
    # Expected Variance
    print('Expected Volatility')
    exp_vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
    print(exp_vol)
    print('\n')
    
    # Sharpe Ratio
    SR = exp_ret/exp_vol
    print('Sharpe Ratio')
    print(SR)
    

    num_ports = 15000

    all_weights = np.zeros((num_ports,len(stocks.columns)))
    ret_arr = np.zeros(num_ports)
    vol_arr = np.zeros(num_ports)
    sharpe_arr = np.zeros(num_ports)

    for ind in range(num_ports):
    
        # Create Random Weights
        weights = np.array(np.random.random(8))

        # Rebalance Weights
        weights = weights / np.sum(weights)

        # Save Weights
        all_weights[ind,:] = weights

        # Expected Return
        ret_arr[ind] = np.sum((log_ret.mean() * weights) *252)

        # Expected Variance
        vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))

        # Sharpe Ratio
        sharpe_arr[ind] = ret_arr[ind]/vol_arr[ind]

    sharpe_arr.max()

    a=sharpe_arr.argmax()

    all_weights[a,:]
    max_sr_ret = ret_arr[a]
    max_sr_vol = vol_arr[a]

    plt.figure(figsize=(12,8))
    plt.scatter(vol_arr,ret_arr,c=sharpe_arr,cmap='plasma')
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Volatility')
    plt.ylabel('Return')

    # Add red dot for max SR
    plt.scatter(max_sr_vol,max_sr_ret,c='red',s=50,edgecolors='black')
    plt.savefig("static/optimized_g5.png")

    return exp_ret, exp_vol, SR;
