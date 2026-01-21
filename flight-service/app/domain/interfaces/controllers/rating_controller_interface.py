from abc import ABC, abstractmethod
from typing import Any


class RatingControllerInterface(ABC):
    @abstractmethod
    def create_rating(self) -> Any:
        pass

    @abstractmethod
    def update_rating(self, rating_id: int) -> Any:
        pass

    @abstractmethod
    def get_rating(self, rating_id: int) -> Any:
        pass

    @abstractmethod
    def get_user_ratings(self, user_id: int) -> Any:
        pass

    @abstractmethod
    def get_all_ratings(self) -> Any:
        pass

    @abstractmethod
    def delete_rating(self, rating_id: int) -> Any:
        pass