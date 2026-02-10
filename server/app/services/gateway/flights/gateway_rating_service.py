from app.domain.services.gateway.flights.igateway_rating_service import IGatewayRatingService
from app.infrastructure.gateway.gateway_client import GatewayClient
from app.domain.dtos.gateway.flights.rating.rating_create_dto import RatingCreateDTO
from app.domain.dtos.gateway.flights.rating.paginated_ratings_dto import PaginatedRatingsDTO, RatingDTO
from app.domain.dtos.gateway.flights.rating.rating_update_dto import RatingUpdateDTO
from app.domain.types.gateway_result import GatewayResult, err, ok


class GatewayRatingService(IGatewayRatingService):
    def __init__(self, gateway_client: GatewayClient) -> None:
        self.client = gateway_client

    def create_rating(self, data: RatingCreateDTO, created_by: int) -> GatewayResult[RatingDTO]:
        try:
            response = self.client.post("/ratings", json=data.to_dict(), headers={'user-id': str(created_by)})
            if response.status_code in (200, 201):
                return ok(RatingDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def get_all_ratings(self, page: int, per_page: int) -> GatewayResult[PaginatedRatingsDTO]:
        try:
            response = self.client.get("/ratings", params={'page': page, 'per_page': per_page})
            if response.status_code == 200:
                return ok(PaginatedRatingsDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def get_rating(self, rating_id: int) -> GatewayResult[RatingDTO]:
        try:
            response = self.client.get(f"/ratings/{rating_id}")
            if response.status_code == 200:
                return ok(RatingDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def get_user_ratings(self, page: int, per_page: int, user_id: int) -> GatewayResult[PaginatedRatingsDTO]:
        try:
            response = self.client.get(f"/users/{user_id}/ratings", params={'page': page, 'per_page': per_page})
            if response.status_code == 200:
                return ok(PaginatedRatingsDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def update_rating(self, rating_id: int, data: RatingUpdateDTO, updated_by: int) -> GatewayResult[RatingDTO]:
        try:
            response = self.client.put(f"/ratings/{rating_id}", headers={'user-id': str(updated_by)}, json=data.to_dict())
            if response.status_code == 200:
                return ok(RatingDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def delete_rating(self, rating_id: int, deleted_by: int) -> GatewayResult[None]:
        try:
            response = self.client.delete(f"/ratings/{rating_id}", headers={'user-id': str(deleted_by)})
            if response.status_code in (200, 204):
                return ok(None)
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')