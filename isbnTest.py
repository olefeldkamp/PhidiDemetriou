import isbn
import unittest

class Isbn13Input(unittest.TestCase):
    
    known_books = ( ('978-1430224150', ('978', '1', '4302', '2415', '0') ), #Dive into Python 3
                    ('978-3150000014', ('978', '3', '15', '000001', '4') ), #Faust
                    ('9783150000014', ('978', '3', '15', '000001', '4') ),
                    ('978-3-15-000001-4', ('978', '3', '15', '000001', '4') ),
                    ('978 3 15 000001 4', ('978', '3', '15', '000001', '4') ),
                    ('978-3 150000014', ('978', '3', '15', '000001', '4') ),
                    ('978-3-15  000001-4', ('978', '3', '15', '000001', '4') ),
                  )

#class Isbn10Input(unittest.TestCase):
#  knownBooks = ( ('1430224150', ('1', '430', '22415', '0') ) '''Dive into Python 3''',
#                 ('3150000017', ('3', '15', '000001', '7') ) '''Faust'''
#               )

    def test_isbn13_split_EAN(self):
        '''first component of the isbn13 should be the 3 digit EAN code'''
        for isbn_string, splited in self.known_books:
            result = isbn.split(isbn_string)
            self.assertEqual(splited[0], result[0])

    def test_isbn13_split_language(self):
        '''second component of the isbn13 should be the language code (1-5 digits)'''
        for isbn_string, splited in self.known_books:
            result = isbn.split(isbn_string)
            self.assertEqual(splited[1], result[1])

    def test_isbn13_split_publisher(self):
        '''third component of the isbn13 should be the publisher code (2-7 digits)'''
        for isbn_string, splited in self.known_books:
            result = isbn.split(isbn_string)
            self.assertEqual(splited[2], result[2])

    def test_isbn13_split_number(self):
        '''fourth component of the isbn13 should be the publisher-intern book number (1-6 digits)'''
        for isbn_string, splited in self.known_books:
            result = isbn.split(isbn_string)
            self.assertEqual(splited[3], result[3])

    def test_isbn13_split_CRC(self):
        '''fifth component of the isbn13 should be the checksum'''
        for isbn_string, splited in self.known_books:
            result = isbn.split(isbn_string)
            self.assertEqual(splited[4], result[4])

    def test_isbn13_split_known_books(self):
        '''isbn13_split schould give a touple of strings'''
        for isbn_string, splited in self.known_books:
            result = isbn.split(isbn_string)
            self.assertEqual(splited, result)


class Isbn13CRC(unittest.TestCase):
    
    valid_books = ('9781430224150',
                   '9783150000014'
                  )
    
    def test_isbn13_testCRC(self):
        '''isbn13_checkCRC should give back true if the check sum is right'''
        for books in self.valid_books:
            result = isbn.checkCRC(books)
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()

