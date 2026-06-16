from app.schemas.company import CompanyReadSingle
from app.schemas.project import ProjectReadSingle
from app.schemas.task import TaskReadSingle
from app.schemas.user import UserRead
from app.schemas.profile import ProfileRead
from app.schemas.join_requests import ReadMultipleJoinRequest,ReadSingleJoinRequest

CompanyReadSingle.model_rebuild()
ProjectReadSingle.model_rebuild()
TaskReadSingle.model_rebuild()
UserRead.model_rebuild()
ProfileRead.model_rebuild()
ReadSingleJoinRequest.model_rebuild()
ReadMultipleJoinRequest.model_rebuild()