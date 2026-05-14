from sqlmodel import select

from app.storage.database import (
    get_session
)

from app.storage.models import Listing

from app.core.logger import app_logger

from app.storage.models import (
    Listing,
    SearchProfile
)


class ListingRepository:

    @staticmethod
    def create_listing(listing: Listing):

        with get_session() as session:

            existing = session.exec(
                select(Listing).where(
                    Listing.krisha_id == listing.krisha_id
                )
            ).first()

            if existing:

                return existing

            session.add(listing)

            session.commit()

            session.refresh(listing)

            app_logger.success(
                f"Saved listing: "
                f"{listing.krisha_id}"
            )

            return listing

    @staticmethod
    def update_listing(listing: Listing):

        with get_session() as session:

            session.merge(listing)

            session.commit()

            app_logger.success(
                f"Updated listing: "
                f"{listing.krisha_id}"
            )

    @staticmethod
    def get_all():

        with get_session() as session:

            return session.exec(
                select(Listing)
            ).all()

class SearchProfileRepository:

    @staticmethod
    def create_profile(profile):

        with get_session() as session:

            session.add(profile)

            session.commit()

            session.refresh(profile)

            return profile

    @staticmethod
    def get_all():

        with get_session() as session:

            return session.exec(
                select(SearchProfile)
            ).all()
    
    @staticmethod
    def update_profile(profile):

        with get_session() as session:

            session.merge(profile)

            session.commit()