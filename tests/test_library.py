from library.library import Library
from library.patron import Patron
from library.ext_api_interface import Books_API
from library.library_db_interface import Library_DB
import unittest, requests, json
from unittest.mock import Mock,patch


class MyTestCase(unittest.TestCase):

    @staticmethod
    def get_library():
        return Library()

    def test_is_ebook_true(self):
        lib = self.get_library()
        lib.api = Mock()
        lib.api.get_ebooks = Mock(return_value=[{'title': 'Title', 'ebook_count': 3},
                                                {'title': 'Title2', 'ebook_count': 4}])
        self.assertTrue(lib.is_ebook('Title'))

    def test_is_ebook_not_found(self):
        lib = self.get_library()
        lib.api = Mock()
        lib.api.get_ebooks = \
            Mock(return_value=[{'title': 'Title', 'ebook_count': 3},
                                {'title': 'Title2', 'ebook_count': 4}])
        self.assertFalse(lib.is_ebook('Random'))

    def test_is_ebook_empty(self):
        lib = self.get_library()
        lib.api = Mock()
        lib.api.get_ebooks = Mock(return_value=[])
        self.assertFalse(lib.is_ebook('Title'))

    def test_get_ebooks_count_empty(self):
        lib = self.get_library()
        lib.api = Mock()
        lib.api.get_ebooks = Mock(return_value=[])
        self.assertEqual(0, lib.get_ebooks_count('Title'))

    def test_get_ebooks_count_0(self):
        lib = self.get_library()
        lib.api = Mock()
        lib.api.get_ebooks = Mock(return_value=[{'title': 'Title', 'ebook_count': 0}])
        self.assertEqual(0, lib.get_ebooks_count('Title'))

    def test_get_ebooks_count_multiple(self):
        lib = self.get_library()
        lib.api = Mock()
        lib.api.get_ebooks = Mock(return_value=[{'title': 'Title', 'ebook_count': 3},
                                                {'title': 'Title2', 'ebook_count': 5}])
        self.assertEqual(8, lib.get_ebooks_count('Title'))

    def test_is_book_by_author_true(self):
        lib = self.get_library()
        lib.api = Mock()
        d = ["Title", "Title2"]
        lib.api.books_by_author = Mock(return_value=d)
        self.assertTrue(lib.is_book_by_author("Author 1", "Title"))

    def test_is_book_by_author_empty(self):
        lib = self.get_library()
        lib.api = Mock()
        d = []
        lib.api.books_by_author = Mock(return_value=d)
        self.assertFalse(lib.is_book_by_author("Author 1", "Title"))

    def test_get_languages_for_book_empty(self):
        lib = self.get_library()
        lib.api = Mock()
        d = []
        lib.api.get_book_info = Mock(return_value=d)
        sol = set()
        self.assertSetEqual(sol, lib.get_languages_for_book("book 1"))

    def test_get_languages_for_book_multiple(self):
        lib = self.get_library()
        lib.api = Mock()
        d = [{
                'title_suggest': "Title 1",
                 'title': "Title 1",
                 'author': "Author 1",
                 'ebook_count_i': 3,
                'language': "German"},
                {'title_suggest': "Title 2",
                 'title': "Title 2",
                 'author': "Author 2",
                 'ebook_count_i': 2,
                 'language': "English"}
                ]
        lib.api.get_book_info = Mock(return_value=d)
        sol = set()
        sol.update("English")
        sol.update("German")
        self.assertSetEqual(sol, lib.get_languages_for_book("Title 1"))


#########


    def test_register_patron_valid(self):
        lib = self.get_library()
        lib.db = Mock()
        lib.db.insert_patron = Mock(return_value=1)
        id = 1
        self.assertEqual(lib.register_patron("albert", "jones", 19, id), id)

    def test_is_patron_registered_false(self):
        lib = self.get_library()
        lib.db = Mock()
        lib.db.retrieve_patron= Mock(return_value=None)
        mock_patron = Mock()
        mock_patron.get_memberID = Mock(return_value=1)
        self.assertFalse(lib.is_patron_registered(mock_patron))

    def test_is_patron_registered_true(self):
        lib = self.get_library()
        lib.db = Mock()
        mock_patron = Mock()
        lib.db.retrieve_patron= Mock(return_value=mock_patron)
        mock_patron.get_memberID = Mock(return_value=1)
        self.assertTrue(lib.is_patron_registered(mock_patron))



if __name__ == '__main__':
    unittest.main()
