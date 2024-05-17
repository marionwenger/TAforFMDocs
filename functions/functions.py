def print_if_debug(debug: bool, text1: object, text2: object = '', text3: object = '') -> None:
    if debug:
        print(text1, text2, text3)
