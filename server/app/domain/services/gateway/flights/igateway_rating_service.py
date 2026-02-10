from abc import abstractmethod

from app.domain.dtos.gateway.flights.rating.rating_create_dto import RatingCreateDTO
from app.domain.types.gateway_result import GatewayResult
from app.domain.dtos.gateway.flights.rating.rating_dto import RatingDTO
from app.domain.dtos.gateway.flights.rating.paginated_ratings_dto import PaginatedRatingsDTO
from app.domain.dtos.gateway.flights.rating.rating_update_dto import RatingUpdateDTO

class IGatewayRatingService:
    @abstractmethod
    def create_rating(self, data: RatingCreateDTO, created_by: int) -> GatewayResult[RatingDTO]:
        pass

    @abstractmethod
    def get_all_ratings(self, page: int, per_page: int) -> GatewayResult[PaginatedRatingsDTO]:
        pass

    @abstractmethod
    def get_rating(self, rating_id: int) -> GatewayResult[RatingDTO]:
        pass

    @abstractmethod
    def get_user_ratings(self, page: int, per_page: int, user_id: int) -> GatewayResult[PaginatedRatingsDTO]:
        pass

    @abstractmethod
    def update_rating(self, rating_id: int, data: RatingUpdateDTO, updated_by: int) -> GatewayResult[RatingDTO]:
        pass

    @abstractmethod
    def delete_rating(self, rating_id: int, deleted_by: int) -> GatewayResult[None]:
        pass
