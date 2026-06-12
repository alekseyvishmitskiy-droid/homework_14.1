class ZeroQuantityProductError(ValueError):
    """Исключение для ситуаций, когда товар с нулевым количеством
    пытаются добавить в Категорию или Заказ.
    """

    def __init__(self, message: str = "Товар с нулевым количеством не может быть добавлен"):
        self.message = message
        super().__init__(self.message)
