from datetime import datetime
import logging

from sqlalchemy.orm import Session

from .. import models
from ..routers.dto import TransactionDto
from ..schemas import requests
from ..repository import TransactionRepository
from ..mappers import TransactionMapper

logger = logging.getLogger(__name__)

class TransactionService:
    """Transaction Service Layer"""

    def __init__(self, budget_repo: TransactionRepository, budget_mapper: TransactionMapper):
        self.transaction_repo = budget_repo
        self.transaction_mapper = budget_mapper

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