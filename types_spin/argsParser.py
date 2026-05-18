def parse(content: str):
    content = content[1:]
    content = content.split()
    content.pop(0)
    return content