from abc import ABC, abstractmethod
from typing import Any

from athena.workflow.workflow import Workflow


class BaseCapability(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        ...

    @property
    @abstractmethod
    def workflows(self) -> dict[str, Workflow]:
        ...

    @property
    def metadata(self) -> dict[str, Any]:
        return {}
    

# class DocumentReviewCapability(BaseCapability):

#     @property
#     def name(self) -> str:
#         return "document_review"

#     @property
#     def description(self) -> str:
#         return "Review and analyze documents."

#     @property
#     def workflows(self) -> dict[str, Workflow]:
#         return {
#             "contract_review": ContractReviewWorkflow(),
#             "clause_analysis": ClauseAnalysisWorkflow(),
#         }