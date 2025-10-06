from src.modules.orders.model import OrderStatusResponse


class OrderBuilder:
    def __init__(self, order: OrderStatusResponse):
        self.order = order