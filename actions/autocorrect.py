from gingerit.gingerit import GingerIt

parser = GingerIt()


def autocorrect(text):
    result = parser.parse(text)
    return result['result']
