from abc import ABC, abstractmethod

from ..enums import TransactionFlow
from ..routers.dto import TransactionDto


class TransactionService(ABC):
    """Transaction Service interface"""

    @abstractmethod
    def create_transaction(self, txnDto: TransactionDto) -> TransactionDto: ...

    @abstractmethod
    def list_transactions(self) -> list[TransactionDto]: ...

    @abstractmethod
    def get_transaction(self, id: str) -> TransactionDto | None: ...

    @abstractmethod
    def delete_transaction(self, id: str) -> TransactionDto | None: ...

    @abstractmethod
    def get_transaction_sum_by_transaction_flow_type(
        self, transactionFlowType: TransactionFlow
    ) -> float: ...

    @abstractmethod
    def get_transaction_sum_by_category(self) -> list[tuple[str, float]]: ...
