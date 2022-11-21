from models.links import Links as LinksModel
from models.links import LinksActivity
from schemas.links import Activity, LongLink
from .base import RepositoryDBActivity, RepositoryDBLink


class RepositoryLink(RepositoryDBLink[LinksModel, LongLink]):
    pass


class RepositoryActivity(RepositoryDBActivity[LinksActivity, Activity]):
    pass


link_crud = RepositoryLink(LinksModel)
activity_crud = RepositoryActivity(LinksActivity)
