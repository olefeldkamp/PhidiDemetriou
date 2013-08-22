import xml.etree.ElementTree as etree

isbn = '9783150000014'
ean = isbn[:3]

publisher_int = int(isbn[3:10])

#print (ean)
#print(publisher_int)

tree = etree.parse('RangeMessage.xml')
root = tree.getroot()
#for child in root:
#    print (child)

#print(len(root))

pref = root.find('EAN.UCCPrefixes')
#print(len(pref))
#for c1 in pref:
#    print(c1)
    
ucc = pref.findall('EAN.UCC')
#print(ucc)
for code in ucc:
#    for c in code:
#        print (c)
#    print(code.find('Prefix').text)
    if code.find('Prefix').text == ean:
        print ('ean ' + ean + ' is valid')  
        for rule in code.find('Rules'):
#            print(rule)
            rule_text = rule.find('Range').text
#            print(rule_text)
            lang_range = rule_text.split('-')
            if int(lang_range[0]) <= publisher_int <= int(lang_range[1]):
#                print(range[0])
#                print (lang_range[0] + ' ' + str(publisher_int) + ' ' + lang_range[1])
                lang_length =rule.find('Length').text
#                print (length)
                lang_string = isbn[3:3+int(lang_length)]
                print (' language is: ' + lang_string)

combined = ean + '-' + lang_string
#print (combined)
reg_groups = root.find('RegistrationGroups')            
for c in reg_groups:
    if c.find('Prefix').text == combined:
        print('published in ' + c.find('Agency').text)
        
        
        
        for rule in c.find('Rules'):
#            print(rule)
            rule_text = rule.find('Range').text
#            print(rule_text)
            pub_range = rule_text.split('-')
#            print (pub_range)
            if int(pub_range[0]) <= int(isbn[3+int(lang_length):3+int(lang_length)+7]) <= int(pub_range[1]):
#                print(pub_range[0])
#                print (pub_range[0] + ' ' + str(publisher_int) + ' ' + pub_range[1])
                pub_length =rule.find('Length').text
#                print (pub_length)
                pub_string = isbn[3+int(lang_length):3+int(lang_length)+int(pub_length)]
                print ('publisher is: ' + pub_string)

print ('   number is: ' + isbn[3+int(lang_length)+int(pub_length):-1])

print ('      CRC is: ' + isbn[-1])

# <RegistrationGroups>
#    <Group>
#      <Prefix>978-0</Prefix>
#      <Agency>English language</Agency>
#      <Rules>
#        <Rule>
#          <Range>0000000-1999999</Range>
#          <Length>2</Length>
#        </Rule>
#        <Rule>