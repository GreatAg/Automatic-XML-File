#import telebot
#Token = '1127425871:AAHIn3SuUqNC0rqE8PlrWPLIqy5t5jIOtuk'
#bot = telebot.TeleBot(Token)
import re
import xml.etree.ElementTree as ET
import modedatabase
tree = ET.parse('Persian Normal.xml')
root = tree.getroot()

# tree.write('newitems.xml')
# tree = ET.parse('newitems.xml')
# root = tree.getroot()
# for elem in root.iter('language'):
#     elem.set('variant', 'خر')


# def change(name,change):
#     for elem in root:
#         for subelem in elem:
#             if re.search(name, subelem.text):
#                 subelem.text = subelem.text.replace(name, change)
#     tree.write('newitems.xml')


#for i in root.findall('string'):
#    modedatabase.add_main_key(i.get('key'))
#    print(i.get('key'))


#i=1
#while i <= 637:
#    modedatabase.add_main_id(i)
#    i += 1
# i=1
# for elem in root:
#     for subelem in elem:
#         modedatabase.add_main_text(i, subelem.text)
#         i+=1

#print(root[2][0].text)
#print(len(root[2]))



#data = ET.Element('data')
#items = ET.SubElement(data, 'items')
#item1 = ET.SubElement(items, 'item')
#item2 = ET.SubElement(items, 'item')
#item1.set('name','item1')
#item2.set('name','item2')
#item1.text = 'item1abc'
#item2.text = 'item2abc'
# create a new XML file with the results
#mydata = ET.tostring(data)
#myfile = open("items2.xml", "w")
#myfile.write(mydata)

#print(root.findall('string').get('key'))
#for i in root.findall('string'):
#    if i.get('key') == 'NoJoinGameRunning':
#       print(i.text)

#tree = ET.parse('items.xml')
#root = tree.getroot()

# changing a field text
#for elem in root.iter('item'):
#    elem.text = 'new text'

# modifying an attribute
#for elem in root.iter('item'):
#    elem.set('name', 'newitem')

# adding an attribute
#for elem in root.iter('item'):
#    elem.set('name2', 'newitem2')

#tree.write('newitems.xml')

#<data>
#    <items>
#        <item name="item1">item1abc</item>
#        <item name="item2">item2abc</item>
#    </items>
#</data>