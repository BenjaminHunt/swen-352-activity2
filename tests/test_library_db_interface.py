import unittest
from library.patron import Patron
from library.library_db_interface import Library_DB
from unittest.mock import patch, MagicMock


class MyTestCase(unittest.TestCase):
    def test_insert_new_patron_none(self):
        lib_db = Library_DB()
        self.assertEqual(lib_db.insert_patron(None), None)

    def test_insert_new_patron_again(self):
        lib_db = Library_DB()
        with patch('library.patron.Patron') as mock_patron:
            mock_db = MagicMock()
            mock_db.search.return_value = [{'fname':"q",'lname':"b",'age':12,'memberID':7}]
            lib_db.db = mock_db
            self.assertEqual(lib_db.insert_patron(mock_patron), None)

    def test_insert_new_patron(self):
        lib_db = Library_DB()
        pid = 1
        mock_patron = MagicMock()
        mock_patron.get_fname.return_value = "f"
        mock_patron.get_lname.return_value = ";"
        mock_patron.get_age.return_value = 21
        mock_patron.get_memberID.return_value = 5
        mock_patron.get_borrowed_books.return_value =[]
        mock_db = MagicMock()
        mock_db.search.return_value = None
        mock_db.insert.return_value = pid
        lib_db.db = mock_db
        self.assertEqual(lib_db.insert_patron(mock_patron), pid)

    def test_get_patron_count_empty(self):
        lib_db = Library_DB()
        with patch('tinydb.TinyDB') as mock_db:
            mock_db.all.return_value = []
            self.assertEqual(lib_db.get_patron_count(), 0)

    def test_close_db(self):
        lib_db = Library_DB()
        with patch('tinydb.TinyDB') as mock_db:
            mock_db.close = True
            self.assertIsNone(lib_db.close_db())


if __name__ == '__main__':
    unittest.main()

