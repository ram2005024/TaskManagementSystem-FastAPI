from app.schemas.company import CompanyBasic, CompanyReadMultiple, CompanyReadSingle
from app.schemas.join_requests import ReadMultipleJoinRequest, ReadSingleJoinRequest
from app.schemas.profile import ProfileBasic, ProfileRead
from app.schemas.project import ProjectReadMultiple, ProjectReadSingle
from app.schemas.task import TaskReadMultiple, TaskReadSingle
from app.schemas.user import UserRead, UserReadBasic

CompanyReadSingle.model_rebuild()
CompanyReadMultiple.model_rebuild()
ProjectReadSingle.model_rebuild()
TaskReadSingle.model_rebuild()
TaskReadMultiple.model_rebuild()
UserReadBasic.model_rebuild()
UserRead.model_rebuild()
ProfileRead.model_rebuild()
ProfileBasic.model_rebuild()
ReadSingleJoinRequest.model_rebuild()
ReadMultipleJoinRequest.model_rebuild()
CompanyBasic.model_rebuild()
ProjectReadMultiple.model_rebuild()
