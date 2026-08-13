from datetime import datetime
from uuid import UUID

from ..requests.transaction_upsert_request import TransactionUpsertRequest


class TransactionUpsertResponse(TransactionUpsertRequest):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
