from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
from math import exp

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # Initialise PEARLS and BANANAS acceptable price
        acceptable_price_pearls = 10000
        acceptable_price_bananas = 5000

        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():

            best_ask_pearls = 0
            best_ask_volume_pearls = 0
            best_bid_pearls = 0
            best_ask_volume_pearls = 0

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'PEARLS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # If statement checks if there are any SELL orders in the PEARLS market
                cum_sum_sells = 0
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_pearls = best_ask
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    best_ask_volume_pearls = best_ask_volume

                    # Now, loop through the sell orders to weight them and eventually calculate valuation price
                    for order in order_depth.sell_orders.keys():
                        price_difference = abs(order - best_ask)
                        cum_sum_sells += abs(order_depth.sell_orders[order]) * exp(-price_difference)

                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                cum_sum_bids = 0
                if len(order_depth.buy_orders) > 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_pearls = best_bid
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    best_bid_volume_pearls = best_bid_volume

                    # Now, loop through the sell orders to weight them and eventually calculate valuation price
                    for order in order_depth.buy_orders.keys():
                        price_difference = abs(best_bid - order)
                        cum_sum_bids += abs(order_depth.buy_orders[order]) * exp(-price_difference)
                
                if best_bid is not None and best_ask is not None:
                    # Calculate our valuation
                    acceptable_price_pearls = (cum_sum_sells * best_bid + cum_sum_bids * best_ask) / (cum_sum_sells + cum_sum_bids)
                    acceptable_price_bananas = acceptable_price_pearls / 2


            # Now trade bananas given that the relation is 1 pearl = 2 bananas
            if product == 'BANANAS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Get best ask and bid values for bananas
                if len(order_depth.sell_orders) > 0:
                    best_ask_bananas = min(order_depth.sell_orders.keys())
                    best_ask_volume_bananas = order_depth.sell_orders[best_ask_bananas]

                if len(order_depth.buy_orders) > 0:
                    best_bid_bananas = max(order_depth.buy_orders.keys())
                    best_bid_volume_bananas = order_depth.sell_orders[best_bid_bananas]

                # Create our buy and sell orders based on our valuation
                # Check if the lowest ask (sell order) is lower than the above defined fair value
                if best_ask_bananas < acceptable_price_bananas:
                    # In case the lowest ask is lower than our fair value,
                    # This presents an opportunity for us to buy cheaply
                    # how much am i buying totla amount
                    print("BUY", str(best_ask_volume_bananas) + "x", best_ask_bananas)
                    orders.append(Order(product, best_ask_bananas, best_ask_volume_bananas))

                    print("SELL", str(-best_bid_volume_bananas / 2) + "x", best_bid_pearls)
                    orders.append(Order(product, best_bid_pearls, -best_bid_volume_pearls / 2))

                # If highest buy is greater than our valuation of acceptable price, we should sell
                if best_bid_bananas > acceptable_price_bananas:
                    print("SELL", str(-best_bid_volume_bananas) + "x", best_bid_bananas)
                    orders.append(Order(product, best_bid_bananas, -best_bid_volume_bananas))

                    print("BUY", str(best_ask_volume_bananas / 2) + "x", best_ask_pearls)
                    orders.append(Order(product, best_ask_pearls, best_ask_volume_pearls / 2))

                # Add all the above the orders to the result dict
                result[product] = orders
    

        # Return the dict of orders
        # These possibly contain buy or sell orders for PEARLS and BANANAS
        # Depending on the logic above
        return result