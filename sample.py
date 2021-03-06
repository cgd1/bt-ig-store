import backtrader as bt
from datetime import datetime
import logging
from bt_ig import IGStore
from bt_ig import IGData


api_key = 'INSERT YOUR API KEY'
usr = 'INSERT YOUR USERNAME'
pwd = 'INSERT YOU PASSWORD'
acc = "INSERT YOUR ACC NUM"

class IGTest(bt.Strategy):
    '''
    Simple strat to test IGStore.
    '''
    def __init__(self):
        pass

    def next(self):
        dt = self.datetime.datetime()
        bar = len(self)
        print('{}: O: {} H: {} L: {} C:{}'.format(dt, self.data.open[0],
                        self.data.high[0],self.data.low[0],self.data.close[0]))


        if bar == 1:
            print('Testing Get Cash!')
            cash = self.broker.getcash()
            print("Current Cash: {}".format(cash))

            print('Testing Get Value!')
            value = self.broker.getvalue()
            print("Current Value: {}".format(value))

        if bar == 2:
            print('Testing Simple Order!')
            pos = self.broker.getposition(self.data)
            self.buy(size=5)
        if bar == 3:
            print('Closing Order')
            pos = self.broker.getposition(self.data)
            print('Open Position Size = {}'.format(pos.size))
            cOrd = self.close()
            print('Closing Order Size = {}'.format(cOrd.size))

            # CHECK CASH AND EQUITY ARE AUTMATICALLY BEING UPDATED
            cash = self.broker.getcash()
            value = self.broker.getvalue()
            print("Current Cash: {}".format(cash))
            print("Current Value: {}".format(value))

        if bar == 4:
            print('Testing Limit Order')
            limit_price = self.data.close[0] * 0.9 #Buy better price 10% lower
            self.limit_ord = self.buy(exectype=bt.Order.Limit, price=limit_price, size=5)

        if bar == 5:
            print('Cancelling Limit Order')
            self.cancel(self.limit_ord)

        if bar ==6:
            print('Testing Stop Order')
            stop_price = self.data.close[0] * 0.9 #buy at a worse price 10% lower
            self.stop_ord = self.buy(exectype=bt.Order.Limit, price=stop_price, size=5)

        if bar == 7:
            print('Cancelling Stop Order')
            self.cancel(self.stop_ord)

        if bar == 8:
            print("Test Finished")
            self.env.runstop()


    ## NOTIFICATIONS
    def notify_order(self,order):
        if order.status == order.Rejected:
            print('Order Rejected')

    def notify_data(self, data, status, *args, **kwargs):
        print('DATA NOTIF: {}: {}'.format(data._getstatusname(status), ','.join(args)))

    def notify_store(self, msg, *args, **kwargs):
        print('STORE NOTIF: {}'.format(msg))


#Logging - Uncomment to see ig_trading library logs
#logging.basicConfig(level=logging.DEBUG)

tframes = dict(
    seconds = bt.TimeFrame.Seconds,
    minutes=bt.TimeFrame.Minutes,
    daily=bt.TimeFrame.Days,
    weekly=bt.TimeFrame.Weeks,
    monthly=bt.TimeFrame.Months)

#Create an instance of cerebro
cerebro = bt.Cerebro()

#Setup IG
igs = IGStore(usr=usr, pwd=pwd, token=api_key, account=sbet)
broker = igs.getbroker()
cerebro.setbroker(broker)


data = igs.getdata(dataname='CS.D.GBPUSD.TODAY.IP')
#Replay the data in forward test envirnoment so we can act quicker
cerebro.resampledata(data, timeframe=tframes['seconds'], compression=15, name='GBP_USD')

#Add our strategy
cerebro.addstrategy(IGTest)

# Run over everything
cerebro.run()
