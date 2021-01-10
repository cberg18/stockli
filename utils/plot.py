import plotext as plt

def plot( y=None, range=30):
    """
    Simple line plot of the stock price.
    y = close price
    range = last x days of price to plot, For full history use -1, default 30 days.
    """
    if y == None:
        return print('y cannot be None') 
    y = y.tail(range) if range != -1 else y 

    plt.clp()
    #set plot size to the size of the terminal
    plt.fig_size(plt.terminal_size()[0],plt.terminal_size()[1])
    plt.plot(y)
    plt.scatter(y)
    plt.show()
