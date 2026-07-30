import logging

from ...routers.dto import TransactionDto
from ...repository import TransactionRepository
from ...mappers import TransactionMapper
from ..transaction_service import TransactionService

logger = logging.getLogger(__name__)

class TransactionServiceImpl(TransactionService):
    """Transaction Service Layer"""

    def __init__(self, transaction_repo: TransactionRepository, transaction_mapper: TransactionMapper):
        self.transaction_repo = transaction_repo
        self.transaction_mapper = transaction_mapper

    def create_transaction(self, txnDto: TransactionDto) -> TransactionDto:
        txnEntity = self.transaction_mapper.to_entity(txnDto)
        created_entity = self.transaction_repo.save(txnEntity)
        return self.transaction_mapper.to_dto_from_entity(created_entity)

    def list_transactions(self) -> list[TransactionDto]:
        return [self.transaction_mapper.to_dto_from_entity(txnEntity) for txnEntity in self.transaction_repo.list_all()]

    def get_transaction(self, id: str) -> TransactionDto | None:
        txnEntity = self.transaction_repo.find_by_id(id)
        if not txnEntity:
            return None
        txtDto = self.transaction_mapper.to_dto_from_entity(txnEntity)
        return txtDto

    def delete_transaction(self, id: str) -> TransactionDto | None:
        txnEntity = self.transaction_repo.find_by_id(id)
        if not txnEntity:
            return None
        txnDto = self.transaction_mapper.to_dto_from_entity(txnEntity)
        self.transaction_repo.delete(txnEntity)
        return txnDto