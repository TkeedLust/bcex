import logging
import random
import time

from core.exchange_interface import ExchangeInterface
from core.order_response import OrderStatus
from core.orders import Order, OrderSide, OrderType, TimeInForce
from core.symbol import Symbol

ORDER_QUANTITY_MAP = {Symbol.ETHBTC: 0.024, Symbol.BTCUSD: 0.001}


def quote_randomly_both_sides_client(bcex_client, levels, sleep_time):
    """
    Parameters
    ----------
    bcex_client: BcexClient
    levels: int
        levels of the orderbooks to populate
    sleep_time: int
        waiting time between each order updates in seconds
    """
    time.sleep(5)
    for clordid, order in bcex_client.open_orders.items():
        bcex_client.send_order(Order(OrderType.CANCEL, order_id=order.order_id))

    while True:
        time.sleep(sleep_time)

        # Randomly cancel existing open orders
        for clordid, order in bcex_client.open_orders.items():
            # if isinstance(order, Order):
            #     # exchange has not updated us on this order yet
            #     continue

            if order.order_status not in OrderStatus.terminal_states():
                if random.random() > 0.4:
                    bcex_client.send_order(
                        Order(OrderType.CANCEL, order_id=order.order_id)
                    )
        for symbol in bcex_client.symbols:

            buy_price = bcex_client.tickers.get(symbol)
            logging.info(f"Buy price {buy_price}")
            if buy_price:
                balance_coin = symbol.split("-")[1]
                balance = bcex_client.balances.get(balance_coin, {}).get("available", 0)
                logging.info(f"Balance {balance} {balance_coin}")
                if balance > 0:
                    for k in range(levels):
                        i = 1 + (k + 1) / 1000 + (random.random() - 0.5) / 1000
                        price = round(float(buy_price) / i, 0)
                        order_quantity = min(
                            round(max(balance / (price), 10 / price), 6), 0.01
                        )
                        o = Order(
                            OrderType.LIMIT,
                            symbol=symbol,
                            price=price,
                            side=OrderSide.BUY,
                            time_in_force=TimeInForce.GTC,
                            order_quantity=order_quantity,
                        )
                        logging.info(
                            "Sending Buy Limit at {} amount {}".format(
                                price, order_quantity
                            )
                        )
                        bcex_client.send_order(o)

            sell_price = bcex_client.tickers.get(symbol)
            logging.info(f"Buy price {sell_price}")

            if sell_price:
                balance_coin = symbol.split("-")[0]
                balance = bcex_client.balances.get(balance_coin, {}).get("available", 0)
                logging.info(f"Balance {balance} {balance_coin}")
                if balance > 0:
                    for k in range(levels):
                        i = 1 - (k + 1) / 1000 + (random.random() - 0.5) / 1000
                        price = round(float(sell_price / i), 0)
                        order_quantity = min(round(balance / 10, 6), 0.01)
                        o = Order(
                            OrderType.LIMIT,
                            symbol=symb,
                            price=price,
                            side=OrderSide.SELL,
                            time_in_force=TimeInForce.GTC,
                            order_quantity=order_quantity,
                        )
                        logging.info(
                            "Sending Sell Limit at {} amount {}".format(
                                price, order_quantity
                            )
                        )
                        bcex_client.send_order(o)


def quote_randomly_both_sides_interface(
    ex_interface: ExchangeInterface, levels, sleep_time
):
    """
    Parameters
    ----------
    bcex_client: ExchangeInterface
    levels: int
        levels of the orderbooks to populate
    sleep_time: int
        waiting time between each order updates in seconds
    """
    ex_interface.connect()

    time.sleep(sleep_time)
    ex_interface.cancel_all_orders()

    while True:
        time.sleep(sleep_time)

        # Randomly cancel existing open orders
        for clordid, order in ex_interface.get_all_open_orders(to_dict=False).items():
            # if isinstance(order, Order):
            #     # exchange has not updated us on this order yet
            #     continue

            if order.order_status not in OrderStatus.terminal_states():
                if random.random() > 0.4:
                    ex_interface.cancel_order(order_id=order.order_id)
        for symbol in ex_interface.get_symbols():

            last_trade_price = ex_interface.get_last_traded_price(symbol)
            logging.info(f"Last Traded price {last_trade_price}")
            if last_trade_price:
                balance_coin = symbol.split("-")[1]
                balance = ex_interface.get_available_balance(balance_coin)
                logging.info(f"Balance {balance} {balance_coin}")
                if balance > 0:
                    for k in range(levels):
                        i = 1 + (k + 1) / 1000 + (random.random() - 0.5) / 1000
                        price = float(last_trade_price) / i
                        order_quantity = min(max(balance / (price), 10 / price), 0.01)
                        ex_interface.place_order(
                            symbol=symbol,
                            side=OrderSide.BUY,
                            quantity=order_quantity,
                            price=price,
                            order_type=OrderType.LIMIT,
                            time_in_force=TimeInForce.GTC,
                            check_balance=True,
                        )
                        logging.info(
                            "Sending Buy Limit at {} amount {}".format(
                                price, order_quantity
                            )
                        )

                balance_coin = symbol.split("-")[0]
                balance = ex_interface.get_available_balance(balance_coin)
                logging.info(f"Balance {balance} {balance_coin}")
                if balance > 0:
                    for k in range(levels):
                        i = 1 - (k + 1) / 1000 + (random.random() - 0.5) / 1000
                        price = round(float(last_trade_price / i), 0)
                        order_quantity = min(round(balance / 10, 6), 0.01)
                        ex_interface.place_order(
                            symbol=symbol,
                            side=OrderSide.SELL,
                            quantity=order_quantity,
                            price=price,
                            order_type=OrderType.LIMIT,
                            time_in_force=TimeInForce.GTC,
                            check_balance=True,
                        )
                        logging.info(
                            "Sending Sell Limit at {} amount {}".format(
                                price, order_quantity
                            )
                        )