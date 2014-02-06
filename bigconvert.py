from lxml import etree

context = etree.iterparse("big.xml", events=("start", "end"))
event, root_element = context.next()

for action, element in context:
    if action == 'end' and element.tag == 'EMAIL':
        print element.text
    root_element.clear()
