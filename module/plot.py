import pandas as pd
import matplotlib.pyplot as plt
'''
manager = Manager('BTC')
manager.main()

'''
class Manager:
    def __init__(self, coin_type):
        self.coin_type = coin_type

    def __read_excel(self, file_path='record.xlsx', sheet_name='main'):
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df = df[df['coin_type'] == self.coin_type]
        return df

    def __is_sell(self, df):
        df_ana = df.copy()
        df_buy = df_ana.query('is_sell == 0')
        df_sell = df_ana.query('is_sell == 1')
        return df_buy, df_sell

    def __calculate_cost(self, df):
        coin = df['num_order(coin)'].sum() if df.shape[0] != 0 else 0
        sum_deal = df['num_deal_fixed(USDT)'].sum() if df.shape[0] != 0 else 1
        price = ((df['average_price(USDT)'] * df['num_deal_fixed(USDT)']).sum() / sum_deal) if df.shape[0] != 0 else 0
        return price, coin

    def __get_info(self, df):
        df_buy, df_sell = self.__is_sell(df)
        buy_price, buy_coin = self.__calculate_cost(df_buy)
        sell_price, sell_coin = self.__calculate_cost(df_sell)
        coin_type = self.coin_type
        return buy_price, buy_coin, sell_price, sell_coin, coin_type

    def __trade_image(self, remain_coin, buy_price=0, buy_coin=0, sell_price=0, sell_coin=0, coin_type=None):
        upper_list = [buy_price, buy_coin, 'BUY'] if buy_price > sell_price else [sell_price, sell_coin, 'SELL']
        low_list = [buy_price, buy_coin, 'BUY'] if buy_price < sell_price else [sell_price, sell_coin, 'SELL']
        least_benefit, now_benefit, now_coin = self.calculate_benefit(remain_coin, buy_price, buy_coin, sell_price, sell_coin)
        
        plt.figure(figsize=(6,4))
        plt.plot([0.5, 0.5], [0, 1], color='black', linewidth=2)
        plt.plot(0.5, 0.8, 'ro')  # 賣出點
        plt.plot(0.5, 0.2, 'go')  # 買入點
        plt.text(0.51, 0.8, f'{upper_list[2]} \n Average_price : {upper_list[0]:.4f} \n num of coin : {upper_list[1]}', fontsize=12, verticalalignment='center')
        plt.text(0.51, 0.5, f'lowest benefit point(USDT) : {least_benefit}\n current profit(USDT):{now_benefit} ', fontsize=12, verticalalignment='center')
        plt.text(0.51, 0.2, f'{low_list[2]} \n Average_price : {low_list[0]:.4f} \n num of coin : {low_list[1]}', fontsize=12, verticalalignment='center')
        plt.title(coin_type)
        plt.axis('off')
        # plt.show()
    
    def calculate_benefit(self, remain_coin, buy_price=0, buy_coin=0, sell_price=0, sell_coin=0, coin_type='BTC'):
        sum_buy = buy_price * buy_coin
        sum_sell = sell_price * sell_coin

        least_benefit = abs(sum_sell - sum_buy) / remain_coin if sum_buy > sum_sell and remain_coin != 0 else 'No lower limit'
        least_benefit = '-' if remain_coin == 0 else least_benefit
        now_benefit = sum_sell - sum_buy 
        now_coin = buy_coin - sell_coin
    
        data = [least_benefit, now_benefit, now_coin]
        index = [f'最低買點(USDT)', f'目前利潤(USDT)', f'剩餘coin({coin_type})']
        
        # print(pd.DataFrame(data, index=index, columns=['Value']))
        return least_benefit, now_benefit, now_coin

    def main(self, remain_coin):
        df = self.__read_excel()
        buy_price, buy_coin, sell_price, sell_coin, coin_type = self.__get_info(df)
        self.__trade_image(remain_coin, buy_price, buy_coin, sell_price, sell_coin, coin_type)


