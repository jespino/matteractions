import RAKE

Rake = RAKE.Rake(RAKE.SmartStopList())


def autotag(text):
    return Rake.run(text, minCharacters=3, maxWords=1)[:4]
