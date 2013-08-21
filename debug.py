if __name__ == '__main__':
#def run():
    import isbn
    isbn.debug = True
    print("testing isbn.split with: '978-3-15  000001-4'")
    isbn.split('978-3-15  000001-4')
    print("\n\ntesting isbn.checkCRC with: '978-3-15  000001-4'")
    isbn.checkCRC('978-3-15  000001-4')
