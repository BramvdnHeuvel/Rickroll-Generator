from flask import request

def title(name, code):
    """
        Build a new valid title route for the rickroll

        > http://rr.noordstar.me/ef8b2bb9

        > http://rr.noordstar.me/the-title-that-emphasizes-your-point-well-ef8b2bb9

        These are interpreted the same way.
    """
    url = ""
    for char in name:
        char = char.lower()
        if char in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
            url += char
        elif char in [' ', '-', '/']:
            url += '-'
        else:
            continue

        if len(url) >= 41:
            break
    
    url += '-' + code
    return url

def new_link():
    """
        Extract the needed information about a new link to be added.
    """
    f = request.form

    return {
        'title'         : f['title'][:65],
        'description'   : None if 'description' not in f or f['description'] == '' else f['description'][:155],
        'image'         : None if 'image' not in f or f['image'] == '' else f['image'][:1024]
    }