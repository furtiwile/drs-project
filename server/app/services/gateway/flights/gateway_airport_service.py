from app.infrastructure.gateway.gateway_client import GatewayClient
from app.domain.dtos.gateway.flights.airport.airport_dto import AirportDTO
from app.domain.types.result import Result, ok, err
from app.domain.dtos.gateway.flights.airport.airport_create_dto import AirportCreateDTO
from app.domain.dtos.gateway.flights.airport.paginated_airports_dto import PaginatedAirportsDTO
from app.domain.dtos.gateway.flights.airport.airport_update_dto import AirportUpdateDTO
from app.domain.services.gateway.flights.igateway_airport_service import IGatewayAirportService

class GatewayAirportService(IGatewayAirportService):
    def __init__(self, gateway_client: GatewayClient) -> None:
        self.client = gateway_client
        return
    
    def create_airport(self, data: AirportCreateDTO) -> Result[AirportDTO, int]:
        try:
            response = self.client.post("/airports", json=data.to_dict())
            if response.status_code in (200, 201):
                return ok(AirportDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def get_all_airports(self, page: int, per_page: int) -> Result[PaginatedAirportsDTO, int]:
        try:
            response = self.client.get("/airports", params={'page': page, 'per_page': per_page})
            if response.status_code == 200:
                return ok(PaginatedAirportsDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def get_airport(self, airport_id: int) -> Result[AirportDTO, int]:
        try:
            response = self.client.get(f"/airports/{airport_id}")
            if response.status_code == 200:
                return ok(AirportDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')
    
    def update_airport(self, airport_id: int, data: AirportUpdateDTO) -> Result[AirportDTO, int]:
        try:
            response = self.client.patch(f"/airports/{airport_id}", json=data.to_dict())
            if response.status_code == 200:
                return ok(AirportDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def delete_airport(self, airport_id: int) -> Result[None, int]:
        try:
            response = self.client.delete(f"/airports/{airport_id}")
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

    def get_airport_info(self, airport_code: str) -> Result[AirportDTO, int]:
        try:
            response = self.client.get(f"/airports/info/{airport_code}")
            if response.status_code == 200:
                return ok(AirportDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')