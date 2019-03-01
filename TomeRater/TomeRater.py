#I chose the more sophisticated error testing option.
def verify_email(email):
    return "@" in email and (len(email)-email.find(".com")==4 or len(email)-email.find(".edu")==4 or len(email)-email.find(".org")==4)

class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        if verify_email(address):
            print(self.name+"'s email has been changed from "+self.email+" to "+address)
            self.email = address
        else:
            print(address+" is an invalid email")

    def __repr__(self):
        return "User "+self.name+", email: "+self.email+", books read: "+str(len(self.books))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        sum_ratings = 0
        for k,v in self.books.items():
            if isinstance(v, float):
                sum_ratings += v
        return sum_ratings/len(self.books)

class Book:
    isbn_list = []
    def __init__(self, title, isbn):
        self.title = title
        if isbn in Book.isbn_list:
            print("ISBN "+str(isbn)+" is taken.")
            isbn=0
            for x in Book.isbn_list:
                isbn+=x
        self.isbn = isbn
        Book.isbn_list+=[isbn]
        self.ratings = []

    def __repr__(self):
        return self.title

    def get_title(self):
        return self.title
    
    def get_isbn(self):
        return self.isbn
    
    def set_isbn(self,new_isbn):
        if new_isbn in Book.isbn_list:
            print("ISBN "+str(new_isbn)+" is taken.")
        else:
            print(self.title+"'s isbn has been changed from "+str(self.isbn)+" to "+str(new_isbn))
            Book.isbn_list.remove(self.isbn)
            self.isbn = new_isbn
            Book.isbn_list+=[new_isbn]
    
    def add_rating(self, rating):
        if isinstance(rating,float) and rating>=0 and rating<=4:
            self.ratings += [rating]
        else:
            print("Invalid Rating")

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def get_average_rating(self):
        avg = 0
        for x in self.ratings:
            avg += x
        return avg/(len(self.ratings) if len(self.ratings)>0 else 1)

    def __hash__(self):
        return hash((self.title, self.isbn))

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return self.title+" by "+self.author

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject
    
    def get_level(self):
        return self.level

    def __repr__(self):
        return self.title+", a "+self.level+" manual on "+self.subject

class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}
    
    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)
    
    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        if email in self.users:
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
            if not book in self.books:
                self.books[book] = 1
            else:
                self.books[book] += 1
    
    def add_user(self, name, email, user_books=None):
        if not email in self.users:
            if verify_email(email):
                self.users[email] = User(name, email)
                if not user_books == None:
                    for x in user_books:
                        self.add_book_to_user(x, email)
            else:
                print(email+" is invalid")
        else:
            print("User with email "+email+" already exists.")

    def print_catalog(self):
        for x in self.books:
            print(x)
        print(list(self.books))

    def print_users(self):
        print([v for k,v in self.users.items()])

    def most_read_book(self):
        b = None
        lrg = None
        for k,v in self.books.items():
            if type(b) == type(None) or lrg < v:
                b = k
                lrg = v
        return b
    
    def highest_rated_book(self):
        b = None
        rtng = None
        for k,v in self.books.items():
            c_rtng = k.get_average_rating()
            if type(b) == type(None) or rtng < c_rtng:
                b = k
                rtng = c_rtng
        return b

    def most_positive_user(self):
        u = None
        rtng = None
        for k,v in self.users.items():
            c_rtng = v.get_average_rating()
            if type(u) == type(None) or rtng < c_rtng:
                u = v
                rtng = c_rtng
        return u
