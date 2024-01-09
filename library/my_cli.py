import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from library.models import Base, Author, Category, Book

# Database setup
DATABASE_URL = "sqlite:///library.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    """Library Management CLI"""

@cli.command()
@click.option('--title', prompt='Book Title', help='Title of the book')
@click.option('--author', prompt='Author Name', help='Name of the author')
@click.option('--category', prompt='Category Name', help='Name of the category')
def add_book(title, author, category):
    """Add a new book to the library"""
    # Check if author exists or create a new one
    existing_author = session.query(Author).filter_by(name=author).first()
    if not existing_author:
        existing_author = Author(name=author)
        session.add(existing_author)

    # Check if category exists or create a new one
    existing_category = session.query(Category).filter_by(name=category).first()
    if not existing_category:
        existing_category = Category(name=category)
        session.add(existing_category)

    # Add the book to the library
    new_book = Book(title=title, author=existing_author, category=existing_category)
    session.add(new_book)
    session.commit()
    click.echo(f"Book '{title}' added to the library.")

@cli.command()
def list_books():
    """List all books in the library"""
    books = session.query(Book).all()
    click.echo("Books in the library:")
    for book in books:
        click.echo(f"{book.title} - {book.author.name} - {book.category.name}")

if __name__ == '__main__':
    cli()
