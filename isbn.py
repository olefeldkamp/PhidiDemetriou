import re

debug = False

def join(isbn_string):
    '''selects the the digits of the string as groups then joins these groups back together as ONE string'''
    grouped = re.findall('[0-9]+', isbn_string) #finds all the characters that are digits
                                                #in groups like in the input string
    joined = ''.join(grouped)                   #joins the groups back as one string
    return (joined)                             #returns the joined isbn string with
                                                #no non-numeral characters between the digits

def split(isbn_string):
    '''split a isbn in its components (EAN, language, publisher, number, CRC)'''
    joined_isbn = join(isbn_string)
    if debug:  print('  eliminating non integer: '+joined_isbn)
    EAN = joined_isbn[0:3]
    if debug: print('  extracting EAN: '+EAN)
    if int(joined_isbn[3:4]) < 8:
        if debug: print('    lang < 8')
        language_code = joined_isbn[3:4]
    elif int(joined_isbn[3:5]) < 95:
        if debug: print('lang < 95')
        language_code = joined_isbn[3:5]
    elif int(joined_isbn[3:6]) < 990:
        if debug: print('lang < 990')
        language_code = joined_isbn[3:6]
    elif int(joined_isbn[3:7]) < 9990:
        if debug: print('lang < 9990')
        language_code = joined_isbn[3:7]
    if debug: print('  extracting language_code: '+language_code)
    
    #if language_code == '0': check_eng1(joined_isbn)
    #if language_code == '1': check_eng2(joined_isbn)
    #if language_code == '3': check_ger(joined_isbn)
    
    with open('publisher_system', encoding='utf-8') as pub_file:
        for line in pub_file:
            start_range,  stop_range = line.split(None, 2)
            lang, start_pub, num, c = start_range.split('-')
            lang, stop_pub, num, c = stop_range.split('-')
            if lang == language_code:
                soaPub = 3+len(lang)
                eoaPub = 3+len(lang)+len(stop_pub)
                if int(start_pub) <= int(joined_isbn[soaPub:eoaPub]) <= int(stop_pub):
                    publisher_code = joined_isbn[soaPub:eoaPub]
                    begin_num = int(eoaPub)
    if debug: print('  extracting publisher_code: '+publisher_code)
    
    
    book_number = joined_isbn[begin_num:-1]
    if debug: print('  extracting book_number: '+book_number)
    CRC = joined_isbn[-1]
    if debug: print('  extracting CRC: '+CRC)
    return (EAN, language_code, publisher_code, book_number, CRC)

def checkCRC(isbn_string):
    '''check the control-number'''
    isbn = join(isbn_string)
    mask = (1,3,1,3,1,3,1,3,1,3,1,3)
    check_sum = 0
    i = 0
    for mask_i in mask:
        check_sum = check_sum + (mask_i * int(isbn[i]))
        i = i+1
    CRC_calc = (10-check_sum%10)%10
    CRC_given = int(isbn[-1])
    if CRC_calc == CRC_given:
        print ('checks out')
        return (True)
    print('wait... what??')
    return (False)
