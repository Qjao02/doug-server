from .NewsBehavior import NewsBehavior
from .ReportBehavior import ReportBehavior
from .ReportBehaviorNews import ReportBehaviorNews
from .ResolutionBehavior import ResolutionBehavior

class BehaviorFactory:
    def getBeahavior(self): pass


class BehaviorFactory(BehaviorFactory):

    def getReportBehavior(self):
        return ReportBehavior()

    def getReportBehaviorNews(self):
        return ReportBehaviorNews()

    def getNewsBehavior(self):
        return NewsBehavior()

    def getResolutionBehavior(self):
        return ResolutionBehavior()


class Factory:

    @staticmethod
    def getBehavior(usersIntent):
        if (usersIntent == 'boletins'):
            object = BehaviorFactory().getReportBehavior()

        elif (usersIntent == 'boletins - yes'):
            object = BehaviorFactory().getReportBehaviorNews()

        elif (usersIntent == 'noticia'):
            object = BehaviorFactory().getNewsBehavior()

        elif (usersIntent == 'resolucao'):
            object = BehaviorFactory().getResolutionBehavior()

        return object

