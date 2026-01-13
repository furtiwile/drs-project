from typing import List, Optional, Dict
from ..domain.models.flights import Airport
from .. import db
from .interfaces import IAirportRepository


class SqlAlchemyAirportRepository(IAirportRepository):
    def save_airport(self, airport: Airport) -> Airport:
        db.session.add(airport)
        db.session.commit()
        db.session.refresh(airport)
        return airport

    def get_airport_by_id(self, airport_id: int) -> Optional[Airport]:
        airport = Airport.query.get(airport_id)
        return airport if airport else None

    def get_all_airports(self, page: int = 1, per_page: int = 10) -> Dict:
        query = Airport.query
        total = query.count()
        orms = query.offset((page - 1) * per_page).limit(per_page).all()
        airports = [orm for orm in orms]
        pages = (total + per_page - 1) // per_page
        return {
            'airports': airports,
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages
        }

    def update_airport(self, airport_id: int, data: Dict) -> Optional[Airport]:
        orm = Airport.query.get(airport_id)
        if not orm:
            return None
        for key, value in data.items():
            if hasattr(orm, key):
                setattr(orm, key, value)
        db.session.commit()
        return orm

    def delete_airport(self, airport_id: int) -> bool:
        orm = Airport.query.get(airport_id)
        if not orm:
            return False
        db.session.delete(orm)
        db.session.commit()
        return True