from app.domain.services.gateway.flights.igateway_rating_service import IGatewayRatingService
from app.domain.dtos.gateway.flights.rating.rating_create_dto import RatingCreateDTO
from app.domain.dtos.gateway.flights.rating.paginated_ratings_dto import PaginatedRatingsDTO, RatingDTO
from app.domain.dtos.gateway.flights.rating.rating_update_dto import RatingUpdateDTO
from app.domain.types.result import Result

from app.infrastructure.gateway.gateway_client import GatewayClient
from app.infrastructure.gateway.utils.api_callers import make_api_call

class GatewayRatingService(IGatewayRatingService):
    def __init__(self, gateway_client: GatewayClient) -> None:
        self.client = gateway_client

    def create_rating(self, data: RatingCreateDTO, created_by: int) -> Result[RatingDTO, int]:
        return make_api_call(
            lambda: self.client.post("/ratings", headers={'user-id': str(created_by)}, json=data.to_dict()),
            lambda r: RatingDTO.from_dict(r.json()),
            success_codes=(200, 201)
        )

    def get_all_ratings(self, page: int, per_page: int) -> Result[PaginatedRatingsDTO, int]:
        return make_api_call(
            lambda: self.client.get("/ratings", params={'page': page, 'per_page': per_page}),
            lambda r: PaginatedRatingsDTO.from_dict(r.json())
        )

    def get_rating(self, rating_id: int) -> Result[RatingDTO, int]:
        return make_api_call(
            lambda: self.client.get(f"/ratings/{rating_id}"),
            lambda r: RatingDTO.from_dict(r.json())
        )

    def get_user_ratings(self, page: int, per_page: int, user_id: int) -> Result[PaginatedRatingsDTO, int]:
        return make_api_call(
            lambda: self.client.get(f"/users/{user_id}/ratings", params={'page': page, 'per_page': per_page}),
            lambda r: PaginatedRatingsDTO.from_dict(r.json())
        )

    def update_rating(self, rating_id: int, data: RatingUpdateDTO, updated_by: int) -> Result[RatingDTO, int]:
        return make_api_call(
            lambda: self.client.put(f"/ratings/{rating_id}", headers={'user-id': str(updated_by)}, json=data.to_dict()),
            lambda r: RatingDTO.from_dict(r.json())
        )

    def delete_rating(self, rating_id: int, deleted_by: int) -> Result[None, int]:
        return make_api_call(
            lambda: self.client.delete(f"/ratings/{rating_id}", headers={'user-id': str(deleted_by)}),
            lambda _: None,
            success_codes=(200, 204)
        )