import unittest,requests,json
from unittest.mock import Mock,patch
from library.ext_api_interface import Books_API



class MyTestCase(unittest.TestCase):

    @staticmethod
    def get_api():
        return Books_API()

    #test_make_requests start
    def test_make_request_200(self):
        book = self.get_api()
        with patch.object(requests,'get') as get_mock:
            get_mock.return_value.status_code = 200
            assert book.make_request(Books_API.API_URL) != None

    def test_make_request_not_200(self):
        book = self.get_api()
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value.status_code = 201
            assert book.make_request(Books_API.API_URL) == None

    def test_make_request_error(self):
        book = self.get_api()
        with patch.object(requests, 'get') as get_mock:
            get_mock.side_effect = requests.exceptions.ConnectionError()
            assert book.make_request(Books_API.API_URL) == None
    #test_make_requests end

    #test_is_book_available start
    def test_is_book_available_non_200(self):
        book = self.get_api()
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value.status_code = 201
            assert book.is_book_available("Das Kapital") == False

    def test_is_book_available_no_books(self):
        data = {
            'start':0,
            'num_Found':0,
            'numFound':0,
            'docs':[]
        }
        book = self.get_api()
        with patch.object(requests,'get') as get_mock:
            get_mock.return_value.status_code = 200
            get_mock.return_value.json.return_value = data
            assert book.is_book_available("Das Kapital") == False

    def test_is_book_available_the_book(self):
        data = {"start":0,"num_Found":1,"numFound":1,"docs":[{"title_suggest":"Das Kapital"}]}
        book = self.get_api()
        with patch.object(requests,'get') as get_mock:
            get_mock.return_value.status_code = 200
            get_mock.return_value.json.return_value = data
            assert book.is_book_available("Das Kapital") == True


if __name__ == '__main__':
    unittest.main()
