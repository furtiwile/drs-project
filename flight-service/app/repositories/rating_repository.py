from typing import Optional
from ..domain.models.flights import Rating, Flight
from .. import db
from app.domain.interfaces.repositories.irating_repository import IRatingRepository, RatingPaginationResult

class SqlAlchemyRatingRepository(IRatingRepository):
    def save_rating(self, rating: Rating) -> Rating:
        db.session.add(rating)
        db.session.commit()
        db.session.refresh(rating)
        return rating

    def get_rating_by_id(self, rating_id: int) -> Optional[Rating]:
        rating = Rating.query.options(
            db.joinedload(Rating.flight).joinedload(Flight.airline),
            db.joinedload(Rating.flight).joinedload(Flight.departure_airport),
            db.joinedload(Rating.flight).joinedload(Flight.arrival_airport)
        ).get(rating_id)
        return rating if rating else None

    def get_ratings_by_user(self, user_id: int, page: int = 1, per_page: int = 10) -> RatingPaginationResult:
        query = Rating.query.filter_by(user_id=user_id).options(
            db.joinedload(Rating.flight).joinedload(Flight.airline),
            db.joinedload(Rating.flight).joinedload(Flight.departure_airport),
            db.joinedload(Rating.flight).joinedload(Flight.arrival_airport)
        )

        total = query.count()
        orms = query.offset((page - 1) * per_page).limit(per_page).all()
        ratings = [orm for orm in orms]
        pages = (total + per_page - 1) // per_page

        return {
            'ratings': ratings,
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages
        }

    def get_all_ratings(self, page: int = 1, per_page: int = 10) -> RatingPaginationResult:
        query = Rating.query.options(
            db.joinedload(Rating.flight).joinedload(Flight.airline),
            db.joinedload(Rating.flight).joinedload(Flight.departure_airport),
            db.joinedload(Rating.flight).joinedload(Flight.arrival_airport)
        )

        total = query.count()
        orms = query.offset((page - 1) * per_page).limit(per_page).all()
        ratings = [orm for orm in orms]
        pages = (total + per_page - 1) // per_page

        return {
            'ratings': ratings,
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages
        }

    def delete_rating(self, rating_id: int) -> bool:
        rating = Rating.query.get(rating_id)
        if not rating:
            return False
        db.session.delete(rating)
        db.session.commit()
        return True