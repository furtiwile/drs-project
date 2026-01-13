from typing import Optional, Dict
from ..domain.models.flights import Airline
from .. import db
from .interfaces import IAirlineRepository


class SqlAlchemyAirlineRepository(IAirlineRepository):
    def save_airline(self, airline: Airline) -> Airline:
        db.session.add(airline)
        db.session.commit()
        db.session.refresh(airline)
        return airline
    
    def get_airline_by_id(self, airline_id: int) -> Optional[Airline]:
        airline = Airline.query.get(airline_id)
        return airline if airline else None

    def get_all_airlines(self, page: int = 1, per_page: int = 10) -> Dict:
        query = Airline.query
        total = query.count()
        orms = query.offset((page - 1) * per_page).limit(per_page).all()
        airlines = [orm for orm in orms]
        pages = (total + per_page - 1) // per_page
        return {
            'airlines': airlines,
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages
        }

    def update_airline(self, airline_id: int, data: Dict) -> Optional[Airline]:
        orm = Airline.query.get(airline_id)
        if not orm:
            return None
        for key, value in data.items():
            if hasattr(orm, key):
                setattr(orm, key, value)
        db.session.commit()
        return orm

    def delete_airline(self, airline_id: int) -> bool:
        orm = Airline.query.get(airline_id)
        if not orm:
            return False
        db.session.delete(orm)
        db.session.commit()
        return True