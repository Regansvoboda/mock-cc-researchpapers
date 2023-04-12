from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here

class Research(db.Model, SerializerMixin):
    __tablename__ = 'researches'

    serialize_rules = ('-research_authors.researches')

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer, db.CheckConstraint('year = len(4)'), nullable=False)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    __table_args__ = (
        db.CheckConstraint('year = len(4)'),
    )

    research_authors = db.relationship('ResearchAuthors', backref='research')
    authors = association_proxy('research_authors', 'authors')


class ResearchAuthors(db.Model, SerializerMixin):
    __tablename__ = 'research_authors'

    serialize_rules = ('-researches.research_authors', '-authors.research_authors')

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    research_id = db.Column(db.Integer, db.ForeignKey('researches.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    serialize_rules = ('-research_authors.authors')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    research_authors = db.relationship('ResearchAuthors', backref='author')
    researches = association_proxy('research_authors', 'researches')