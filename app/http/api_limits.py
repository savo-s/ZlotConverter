from abc import ABC, abstractmethod


class ApiLimits(ABC):

    @abstractmethod
    def schedule_weight_reset(self):
        """Abstract method to time-schedule reset weights"""
        pass

    @abstractmethod
    def reset_weights(self):
        """Abstract method to reset"""
        pass

    def is_in_rate_limits(self):
        """Abstract method to return True/False if weight is in rate limits"""
        pass