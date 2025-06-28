from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.http.api_limits import ApiLimits
from app.http.endpoints.nbp.settings.nbp_config import NbpConfig


class NbpApiLimits(ApiLimits):

    _instance = None
    limit = 0
    weight = 0

    def __new__(cls):
        if cls._instance is None:
            cls.limit = int(NbpConfig.WEIGHT_PER_MIN)
            cls._instance = super().__new__(cls)
            cls._instance.schedule_weight_reset()
        return cls._instance

    def schedule_weight_reset(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            id="Reset_NBP_API_Weights",
            func=self.reset_weights,
            trigger=IntervalTrigger(minutes=1)
        )
        scheduler.start()

    def get_limit(self):
        return self.limit

    def add_weight(self, weight):
        self.weight += weight

    def reset_weights(self):
        self.weight = 0

    def is_in_rate_limits(self):
        return self.weight <= self.limit
