
from PIL import Image


HASH_FUNCS = {
    "_thread.RLock": lambda _: None,
    "_thread.lock": lambda _: None,
    "builtins.PyCapsule": lambda _: None,
    "_io.TextIOWrapper": lambda _: None,
    "builtins.weakref": lambda _: None,
    "builtins.dict": lambda _: None,
    "builtins.function": lambda _:None
}


HTML_WRAPPER = (
    '<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; '
    '# margin-bottom: 2.5rem">{}</div>'
)

def card_begin_str(header):
    return (
        '<div style="border-radius: 5px;box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);transition: 0.3s; padding: 1rem; # margin-top: 2.5rem; # margin-bottom: 1.5rem">'
        '<div class="container">'
        f"<h3><b>{header}</b></h3>"
    )


def card_end_str():
    return "</div></div>"


def card(header, body, url):
    lines = [card_begin_str(header), f"<p>{body}</p>", f"<a href={url}> Read the article </a>",card_end_str()]
    return ("".join(lines))

def get_image(image_path, basewidth = 150):
    image = Image.open(image_path)
    wpercent = (basewidth/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((basewidth,hsize), Image.ANTIALIAS)
    return image