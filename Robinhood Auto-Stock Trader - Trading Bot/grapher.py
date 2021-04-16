import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

def normalize(df):
    # df.shape = (rows, columns)
    if len(df.shape) == 1 or df.shape[1] == 1:
        dfNORMALIZED = df/df.iloc[0]
    else:
        dfNORMALIZED = pd.DataFrame()
        trading_days = df.index
        for stock in df.columns.values.tolist():
            dfNORMALIZED[stock] = pd.Series(df[stock]/df[stock].iloc[0], index=trading_days)

    return(dfNORMALIZED)

def active_graph(df, df_trades, pause=1):
    plt.clf()
    plt.ion()
    plt.title('active_graph')
    plt.xlabel('Time')
    plt.xticks([])
    plt.ylabel('Normalized Price')

    for stock in df_trades.columns.values.tolist():
        if df_trades[stock].iloc[-1] == 'HOLD' or df_trades[stock].iloc[-1] == 'BUY':
            plt.plot(df[stock], alpha=1.0)
        elif df_trades[stock].iloc[-1] == 'WAIT' or df_trades[stock].iloc[-1] == 'SELL':
            plt.plot(df[stock], alpha=0.2)

        for day, order in df_trades.iterrows():
            if order[stock] == 'BUY':
                plt.axvline(day, color='g', alpha=0.25)
            elif order[stock] == 'SELL':
                plt.axvline(day, color='r', alpha=0.25)

    print('df_prices \n', df)
    print('df_trades \n', df_trades)

    plt.legend(df.columns.values.tolist(), loc='upper left')
    plt.draw()
    plt.savefig(str(dt.date.today()))
    plt.pause(pause)
