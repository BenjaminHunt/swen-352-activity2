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

    def test_is_book_available_found_book(self):
        data = {"start":0,"num_Found":1,"numFound":1,"docs":[{"title_suggest":"Das Kapital"}]}
        book = self.get_api()
        with patch.object(requests,'get') as get_mock:
            get_mock.return_value.status_code = 200
            get_mock.return_value.json.return_value = data
            assert book.is_book_available("Das Kapital") == True
    #test_is_book_available end

    #test_books_by_author start
    def test_books_by_author_non_200(self):
        book = self.get_api()
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value.status_code = 201
            assert book.books_by_author("Karl Marx") == []

    def test_books_by_author_no_books(self):
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
            assert book.books_by_author("Karl Marx") == []

    def test_books_by_author_found_book(self):
        data = {"start":0,"num_Found":1,"numFound":1,"docs":[{"title_suggest":"Das Kapital"}]}
        book = self.get_api()
        with patch.object(requests,'get') as get_mock:
            get_mock.return_value.status_code = 200
            get_mock.return_value.json.return_value = data
            assert book.books_by_author("Karl Marx") == ["Das Kapital"]
    #test_books_by_author end

    #test_get_book_info start
    def test_get_book_info_non_200(self):
        book = self.get_api()
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value.status_code = 201
            assert book.get_book_info("Das Kapital") == []

    def test_get_book_info_no_book(self):
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
            assert book.get_book_info("Das Kapital") == []

    def test_get_book_info_found_book(self):
        data = {"start":0,"num_Found":1,"numFound":1,
                "docs":[
                    {'title_suggest':"Das Kapital",
                     'title':"Das Kapital",
                     'publisher':"Verlag von Otto Meisner",
                     'publish_year':"1867",
                     'language':"German"}
                ]}
        book = self.get_api()
        with patch.object(requests,'get') as get_mock:
            get_mock.return_value.status_code = 200
            get_mock.return_value.json.return_value = data
            assert book.get_book_info("Das Kapital") == [
                {'title':"Das Kapital",
                'publisher':"Verlag von Otto Meisner",
                 'publish_year':"1867",
                 'language':"German"}
            ]
    #test_get_book_info end

    #test_get_ebooks start
    def test_get_ebook_non_200(self):
        book = self.get_api()
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value.status_code = 201
            assert book.get_ebooks("Das Kapital") == []

    def test_get_ebook_no_book(self):
        data = {
            'start': 0,
            'num_Found': 0,
            'numFound': 0,
            'docs': []
        }
        book = self.get_api()
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value.status_code = 200
            get_mock.return_value.json.return_value = data
            assert book.get_ebooks("Das Kapital") == []

    def test_get_ebook_found_book(self):
        data = {"start": 0, "num_Found": 1, "numFound": 1,
                "docs": [
                    {'title_suggest': "Das Kapital",
                     'title': "Das Kapital",
                    'ebook_count_i':10}
                ]}
        book = self.get_api()
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value.status_code = 200
            get_mock.return_value.json.return_value = data
            assert book.get_ebooks("Das Kapital") == [
                {'title': "Das Kapital",
                 'ebook_count': 10,
                }
            ]
    def test_get_ebook_found_book_but_0_ebooks(self):
        data = {"start": 0, "num_Found": 1, "numFound": 1,
                "docs": [
                    {'title_suggest': "Das Kapital",
                     'title': "Das Kapital",
                    'ebook_count_i':0}
                ]}
        book = self.get_api()
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value.status_code = 200
            get_mock.return_value.json.return_value = data
            assert book.get_ebooks("Das Kapital") == [
            ]
if __name__ == '__main__':
    unittest.main()
