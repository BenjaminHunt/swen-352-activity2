import unittest
from library.patron import Patron
from library.library_db_interface import Library_DB
from unittest.mock import patch, MagicMock


class MyTestCase(unittest.TestCase):
    def test_insert_new_patron_none(self):
        lib_db = Library_DB()
        self.assertEqual(lib_db.insert_patron(None), None)

    def test_insert_new_patron_again(self):
        with patch('Activity2_source.library.patron.Patron') as mock_patron:
            lib_db = Library_DB()
            mock_patron.get_memberID = MagicMock(return_value=1)
            self.assertEqual(lib_db.insert_patron(None), None)

    def test_insert_new_patron(self):
        with patch('Activity2_source.library.patron.Patron') as mock_patron:
            lib_db = Library_DB()
            mock_patron.get_fname = MagicMock()
            mock_patron.get_lname = MagicMock()
            mock_patron.get_age = MagicMock()
            mock_patron.get_memberID = MagicMock()
            mock_patron.get_borrowed_books = MagicMock()
            self.assertIsNotNone(lib_db.insert_patron(mock_patron))


if __name__ == '__main__':
    unittest.main()

