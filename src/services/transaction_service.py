from abc import ABC, abstractmethod
from ..routers.dto import TransactionDto

class TransactionService(ABC):
    """Transaction Service interface"""

    @abstractmethod
    def create_transaction(self, txnDto: TransactionDto) -> TransactionDto:
        ...

    @abstractmethod
    def list_transactions(self) -> list[TransactionDto]:
        ...

    @abstractmethod
    def get_transaction(self, id: str) -> TransactionDto | None:
        ...

    @abstractmethod
    def delete_transaction(self, id: str) -> TransactionDto | None:
        ...