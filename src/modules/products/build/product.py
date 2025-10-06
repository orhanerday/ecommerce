import logging
from src.modules.products.model import ProductResponse


class ProductBuilder:
    def __init__(self, product: ProductResponse):
        self.product = product

    # Example of another builder method
    # def normalize_initial_stock(self) -> "ProductBuilder":
    #     if not self.product.initial_stock or self.product.initial_stock < 1:
    #         self.product.initial_stock = max(self.product.stock, 1)
    #     return self

    def add_dynamic_price(self) -> "ProductBuilder":
        initial = self.product.initial_stock or 1  # avoid div by zero
        stock_ratio = self.product.stock / initial

        if stock_ratio > 0.50:
            factor = 1.0
        elif stock_ratio > 0.25:  # implicitly <= 0.50 from previous branch
            factor = 1.2
        else:
            factor = 1.5

        self.product.current_price = round(self.product.base_price * factor, 2)
        return self

    def get(self) -> ProductResponse:
        logging.info("Final product state: %s", self.product)
        return self.product