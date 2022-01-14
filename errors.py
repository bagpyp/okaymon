class AllowablePurchasesError(Exception):
    def __init__(self, purchase_record) -> None:
        self.message = f"{purchase_record} full"
        super().__init__()