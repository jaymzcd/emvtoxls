from lxml import etree

context = etree.iterparse("data/big.xml", events=("start", "end"))
event, root_element = context.next()

cnt = 0

while True:
    e, m = context.next()

    for element in m.getchildren():
        #print element.tag, element.text
        root_element.clear()

    cnt += 1
    print cnt

