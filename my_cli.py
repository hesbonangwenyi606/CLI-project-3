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
    existing_author = session.query(Author).filter_by(name=author).first()
    if not existing_author:
        existing_author = Author(name=author)
        session.add(existing_author)

    existing_category = session.query(Category).filter_by(name=category).first()
    if not existing_category:
        existing_category = Category(name=category)
        session.add(existing_category)

    new_book = Book(title=title, author=existing_author, category=existing_category)
    session.add(new_book)
    session.commit()
    click.echo(f"Book '{title}' added to the library.")

# Modify the help message for the command
@cli.command()
@click.option('--help', is_flag=True, help='Display available commands.')
def list_books():
    """List all books in the library"""
    books = session.query(Book).all()
    click.echo("Books in the library:")
    for book in books:
        click.echo(f"{book.title} - {book.author.name} - {book.category.name}")

@cli.command()
def search_books():
    """Search for books in the library"""
    # Implement your book search functionality here
    click.echo("Searching for books...")

@cli.command()
@click.argument('book_id', type=int)
def view_book(book_id):
    """View details of a specific book"""
    # Implement code to view details of the specified book
    click.echo(f"Viewing details of Book ID {book_id}...")

@cli.command()
def delete_book():
    """Delete a book from the library"""
    # Implement code to delete a book
    click.echo("Deleting a book...")

@cli.command()
def update_book():
    """Update details of a book in the library"""
    # Implement code to update book details
    click.echo("Updating book details...")

@cli.command()
def list_authors():
    """List all authors in the library"""
    authors = session.query(Author).all()
    click.echo("Authors in the library:")
    for author in authors:
        click.echo(f"{author.name}")

@cli.command()
def list_categories():
    """List all categories in the library"""
    categories = session.query(Category).all()
    click.echo("Categories in the library:")
    for category in categories:
        click.echo(f"{category.name}")

@cli.command()
def stats():
    """Display library statistics"""
    # Implement code to display library statistics
    click.echo("Displaying library statistics...")

@cli.command()
def export_data():
    """Export library data"""
    # Implement code to export library data
    click.echo("Exporting library data...")

if __name__ == '__main__':
    cli()
