def error(text=None):
    if text:
        print(text)
    raise Exception('Что-то не так')
