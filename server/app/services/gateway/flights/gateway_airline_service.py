from app.infrastructure.gateway.gateway_client import GatewayClient
from app.domain.dtos.gateway.flights.airline.airline_create_dto import AirlineCreateDTO
from app.domain.dtos.gateway.flights.airline.airline_dto import AirlineDTO
from app.domain.dtos.gateway.flights.airline.airline_update_dto import AirlineUpdateDTO
from app.domain.types.gateway_result import GatewayResult, ok, err
from app.domain.services.gateway.flights.igateway_airline_service import IGatewayAirlineService
from app.domain.dtos.gateway.flights.airline.paginated_airlines_dto import PaginatedAirlinesDTO

class GatewayAirlineService(IGatewayAirlineService):
    def __init__(self, client: GatewayClient) -> None:
        self.client = client

    def create_airline(self, data: AirlineCreateDTO) -> GatewayResult[AirlineDTO]:
        try:
            response = self.client.post("/airlines", json=data.to_dict())
            if response.status_code in (200, 201):
                return ok(AirlineDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')
    
    def get_all_airlines(self, page: int, per_page: int) -> GatewayResult[PaginatedAirlinesDTO]:
        try:
            response = self.client.get("/airlines", params={'page': page, 'per_page': per_page})
            if response.status_code == 200:
                return ok(PaginatedAirlinesDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def get_airline(self, airline_id: int) -> GatewayResult[AirlineDTO]:
        try:
            response = self.client.get(f"/airlines/{airline_id}")
            if response.status_code == 200:
                return ok(AirlineDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')
    
    def update_airline(self, airline_id: int, data: AirlineUpdateDTO) -> GatewayResult[AirlineDTO]:
        try:
            response = self.client.patch(f"/airlines/{airline_id}", json=data.to_dict())
            if response.status_code == 200:
                return ok(AirlineDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')
    
    def delete_airline(self, airline_id: int) -> GatewayResult[None]:
        try:
            response = self.client.delete(path=f"/airlines/{airline_id}")
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
