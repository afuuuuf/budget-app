import logging

from ..enums import TransactionFlow
from ..exception import NotFoundException
from ..mappers import TransactionMapper
from ..models import Transaction
from ..repository import TransactionRepository
from ..routers.dto import TransactionDto

logger = logging.getLogger(__name__)
TRANSACTION_NOT_FOUND_MESSAGE = "Transaction Not Found"


class TransactionService:
    """Transaction Service Layer"""

    def __init__(
        self,
        transaction_repo: TransactionRepository,
        transaction_mapper: TransactionMapper,
    ):
        self.transaction_repo = transaction_repo
        self.transaction_mapper = transaction_mapper

    def create_transaction(self, transaction_dto: TransactionDto) -> TransactionDto:
        transaction_entity = self.transaction_mapper.to_entity(transaction_dto)
        created_entity = self.transaction_repo.save(transaction_entity)
        return self.transaction_mapper.to_dto_from_entity(created_entity)

    def list_transactions(self, user_id: str) -> list[TransactionDto]:
        return [
            self.transaction_mapper.to_dto_from_entity(transaction_entity)
            for transaction_entity in self.transaction_repo.list_all(user_id)
        ]

    def get_transaction(self, id: str, user_id: str) -> TransactionDto:
        transaction_entity = self._get_transaction_entity_by_id_and_user_id(id, user_id)
        return self.transaction_mapper.to_dto_from_entity(transaction_entity)

    def delete_transaction(self, id: str, user_id: str) -> TransactionDto | None:
        transaction_entity = self._get_transaction_entity_by_id_and_user_id(id, user_id)
        self.transaction_repo.delete(transaction_entity)
        return self.transaction_mapper.to_dto_from_entity(transaction_entity)

    def get_transaction_sum_by_transaction_flow_type(
        self, transactionFlowType: TransactionFlow
    ) -> float:
        return self.transaction_repo.sum_by_flow(transactionFlowType)

    def get_transaction_sum_by_category(self) -> list[tuple[str, float]]:
        return self.transaction_repo.sum_by_category()

    def _get_transaction_entity_by_id_and_user_id(
        self, id: str, user_id: str
    ) -> Transaction:
        transaction_entity = self.transaction_repo.find_by_id(id, user_id)
        if not transaction_entity:
            raise NotFoundException(TRANSACTION_NOT_FOUND_MESSAGE)
        return transaction_entity
