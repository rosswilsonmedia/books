from ..config.mysqlconnection import connectToMySQL

from ..models import author

class Book:
    def __init__(self, data):
        self.id=data['id']
        self.title=data['title']
        self.num_of_pages=data['num_of_pages']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.authors=[]

    @classmethod
    def get_all(cls):
        query="SELECT * FROM books;"
        results=connectToMySQL('books_schema').query_db(query)
        all_books=[]
        for book in results:
            all_books.append(cls(book))
        return all_books

    @classmethod
    def get_one(cls, data):
        query="SELECT * FROM books "\
            "LEFT JOIN favorites ON books.id=favorites.book_id "\
            "LEFT JOIN authors ON favorites.author_id=authors.id "\
            "WHERE books.id=%(id)s;"
        results=connectToMySQL('books_schema').query_db(query, data)
        book=cls(results[0])
        if results[0]['authors.id']!=None:
            for row in results:
                row_data={
                    'id':row['authors.id'],
                    'name':row['name'],
                    'created_at':row['authors.created_at'],
                    'updated_at':row['authors.updated_at']
                }
                book.authors.append(author.Author(row_data))
        return book

    @classmethod
    def add_new(cls, data):
        query="INSERT INTO books (title, num_of_pages, created_at, updated_at) "\
            "VALUES (%(title)s, %(num_of_pages)s, NOW(), NOW());"
        book_id=connectToMySQL('books_schema').query_db(query, data)
        return book_id

    @classmethod
    def add_favorite_author(cls, data):
        query="INSERT INTO favorites (book_id, author_id) "\
            "VALUES (%(book_id)s, %(author_id)s);"
        connectToMySQL('books_schema').query_db(query, data)