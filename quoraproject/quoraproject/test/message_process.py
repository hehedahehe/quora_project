# -*- coding: utf-8 -*-

def processMessage(message):
    import re
    m = re.split("html|css|js", message)
    result = []
    for each in m:
        each = each.strip().replace("\\","")
        if "<div" in each:
            result.append(each[each.find("<"):each.rfind(">")+1])


    return "".join(result)


if __name__ == "__main__":
    with open("message") as mf:
        content = mf.read()
        content = processMessage(content)
        print content




