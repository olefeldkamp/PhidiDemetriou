import xml.etree.ElementTree as etree
import re


def analize_isbn(isbn):
    isbn = join(isbn)
    #print ('\nStarting to analize ISBN: ' + isbn + ' ...')
    tree_root = etree.parse('RangeMessage.xml').getroot()
    [ean, lang_entry] = check_ean(isbn, tree_root)
    #print (ean)
    [language] = analize_language(isbn, lang_entry)
    #print (language)
    [publisher, agency] = analize_publisher(isbn, tree_root, ean, language)
    #print (publisher)
    [number] = analize_number(isbn, ean, language, publisher)
    #print (number)
    [crc] = analize_crc(isbn)
    return (ean + '-' +  language + '-' + publisher + '-' + number + '-' + crc)

def join(isbn_string):
    '''selects the the digits of the string as groups then joins these groups back together as ONE string'''
    grouped = re.findall('[0-9]+', isbn_string) #finds all the characters that are digits
                                                #in groups like in the input string
    joined = ''.join(grouped)                   #joins the groups back as one string
    return (joined)                             #returns the joined isbn string with
                                                #no non-numeral characters between the digits

def check_ean(isbn, tree_root):
    '''checks if the EAN identifier is bookish'''
    ucc = tree_root.find('EAN.UCCPrefixes').findall('EAN.UCC')
    for lang_entry in ucc:
        if lang_entry.find('Prefix').text == isbn[:3]:
    #        print ('EAN-Prefix ' + ean + ' is valid')
            return ([lang_entry.find('Prefix').text, lang_entry])
    raise ValueError(isbn[:3] + ' is not a EAN code for a book')
                    

def analize_language(isbn, lang_entry):
    '''analizes the laguage in witch the book is published'''
    for rule in lang_entry.find('Rules'):
        lang_range = rule.find('Range').text.split('-')
        if int(lang_range[0]) <= int(isbn[3:10]) <= int(lang_range[1]):
            lang_length =rule.find('Length').text
            language = isbn[3:3+int(lang_length)]
            return([language])
    raise Error('can not find language')
    
def analize_publisher(isbn, tree_root, ean, lang):
    '''analizes the publisher of the book'''
    reg_groups = tree_root.find('RegistrationGroups')            
    for lang_code in reg_groups:
        if lang_code.find('Prefix').text == ean + '-' + lang:
            agency = lang_code.find('Agency').text
            for rule in lang_code.find('Rules'):
                pub_range = rule.find('Range').text.split('-')
                if int(pub_range[0]) <= int(isbn[len(ean)+len(lang):len(ean)+len(lang)+7]) <= int(pub_range[1]): #muss eventuell mit nullen aufgefüllt werden
                    pub_length =rule.find('Length').text
                    publisher = isbn[len(ean)+len(lang):len(ean)+len(lang)+int(pub_length)]
                    return ([publisher, agency])
    raise Error('can not find publisher')
    
def analize_number(isbn, ean, language, publisher):
    '''analizes the publisher-intern number of the book'''
    number = isbn[len(ean)+len(language)+len(publisher):-1]
    return ([number])
    
def analize_crc(isbn):
    '''checks if the check sum is right'''
    crc = isbn[-1]
    #isbn = join(isbn)
    mask = (1,3,1,3,1,3,1,3,1,3,1,3)
    check_sum = 0
    i = 0
    for mask_i in mask:
        check_sum = check_sum + (mask_i * int(isbn[i]))
        i = i+1
    CRC_calc = (10-check_sum%10)%10
    CRC_given = int(isbn[-1])
    if CRC_calc == CRC_given:
        return ([crc])
    raise crcError('check sum does not match')



isbns_for_test = ['978-1430224150', '978-3150000014', '9783150000014', '978-3-15-000001-4', '978 3 15 000001 4', '978-3 150000014', '978-3-15  000001-4', '9783899056761']
for number in isbns_for_test: 
    print('Analizing...  {:<20} --> {}'.format(number, analize_isbn(number)))
