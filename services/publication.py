from models.publication import Publication as PublicationModel
from schemas.publication import Publication

class PublicationService:

    def __init__(self, db) -> None:
        self.db = db

    def get_publications(self):
        result = self.db.query(PublicationModel).all()
        return result

    def get_publication(self, id):
        result = self.db.query(PublicationModel).filter(PublicationModel.id == id).first()
        return result

    def get_publications_by_state(self, state):
        result = self.db.query(PublicationModel).filter(PublicationModel.state == state).all()
        return result

    def create_publication(self, publication: Publication):
        new_publication = PublicationModel(**publication.dict())
        self.db.add(new_publication)
        self.db.commit()
        return

    def update_publication(self, id: int, data: Publication):
        publication = self.db.query(PublicationModel).filter(PublicationModel.id == id).first()
        publication.title = data.title
        publication.content = data.content
        publication.state = data.state
        self.db.commit()
        return

    def delete_publication(self, id: int):
        self.db.query(PublicationModel).filter(PublicationModel.id == id).delete()
        self.db.commit()
        return