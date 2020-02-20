import unittest
from Activity2_source.library.patron import Patron, InvalidNameException
from unittest.mock import Mock


class MyTestCase(unittest.TestCase):

    @staticmethod
    def get_patron():
        return Patron("Stephen", "Cook", 22, 1)

    def test_no_numbers_in_name(self):
        self.assertRaises(InvalidNameException, Patron, "5tephen", "Cook", 22, 1)

    def test_add_borrowed_book(self):
        patron = self.get_patron()
        book = 'the bible'
        patron.add_borrowed_book(book)
        self.assertTrue(book in patron.borrowed_books)

    def test_add_already_borrowing(self):
        patron = self.get_patron()
        book = 'the bible'
        patron.borrowed_books = [book]
        patron.add_borrowed_book(book)
        self.assertEqual(patron.borrowed_books, [book])

    def test_eq(self):
        patron1 = self.get_patron()
        patron2 = self.get_patron()
        self.assertTrue(patron1.__eq__(patron2))

    def test_ne(self):
        patron1 = self.get_patron()
        patron2 = Patron('Stephen', 'Hook', 23, 2)
        self.assertTrue(patron1.__ne__(patron2))

    def test_get_borrowed_books(self):
        patron = self.get_patron()
        book = 'the marshin'
        borrowed = [book]
        patron.borrowed_books = borrowed
        self.assertEqual(
            patron.get_borrowed_books(),
            [book]
        )

    def test_return_book(self):
        patron = self.get_patron()
        book = "Oprah's Book".lower()
        patron.borrowed_books = [book]
        patron.return_borrowed_book(book)
        self.assertFalse(book in patron.borrowed_books)

    def test_get_fname(self):
        patron = self.get_patron()
        self.assertEqual(patron.fname, patron.get_fname())

    def test_get_lname(self):
        patron = self.get_patron()
        self.assertEqual(patron.lname, patron.get_lname())

    def test_get_age(self):
        patron = self.get_patron()
        self.assertEqual(patron.age, patron.get_age())

    def test_get_memberID(self):
        patron = self.get_patron()
        self.assertEqual(patron.memberID, patron.get_memberID())



if __name__ == '__main__':
    unittest.main()
