import plotext as plt


def plot(plot_name, y, range=30):
    """
    Simple line plot of the stock price.
    y = close price
    range = last x days of price to plot, For full history use -1, default 30 days.
    plotext does not currently support datetime so x axis labels are just len(y) numbers
    """
    if y.empty:
        return print('y cannot be None')
    y = y.tail(range) if range != -1 else y

    plt.clp()
    # set plot size to the size of the terminal
    plt.fig_size(plt.terminal_size()[0], plt.terminal_size()[1])
    plt.plot(y)
    plt.scatter(y)
    plt.title(plot_name)
    plt.ylabel('Close Price - $')
    plt.facecolor('iron')
    plt.canvas_color('iron')
    plt.show()
    return
