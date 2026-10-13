"""Rebuild the static Tough Old Men site from raw Wayback HTML in source/raw. Run: python3 -I source/build.py"""
import re, json, glob, os, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', 'site')
RAW = os.path.join(HERE, 'raw')
os.chdir(ROOT)
imgmap = json.load(open('assets/img/photos/_map.json'))

# page slug -> output path
def out_path(slug):
    if slug == 'home': return 'index.html'
    if slug.startswith('store-'): return 'store/' + slug[6:] + '/index.html'
    return slug + '/index.html'

def page_url(path):
    path = path.strip('/')
    if path == '': return '/'
    return '/' + path + '/'

raw_adv = open(os.path.join(RAW, 'adventure-story.html'), encoding='utf8').read()
hdr = re.search(r'<header id="header">.*?</header>', raw_adv, re.S).group(0)
# Store link removed from the main nav
hdr = re.sub(r'\s*<li class="[^"]*">\s*(?:<!--[^>]*-->\s*)*<a href="[^"]*/store/">Store</a>.*?</li>', '', hdr, count=1, flags=re.S)
ftr = re.search(r'<footer id="footer">.*?</footer>', raw_adv, re.S).group(0)

def unwayback(s):
    s = re.sub(r'(?:https?:)?//web\.archive\.org/web/\d+[a-z_]*/', '', s)
    s = re.sub(r'/web/\d+[a-z_]*/', '', s)
    return s

def local_img(u):
    b = u.split('?')[0]
    b = re.sub(r'^https?:', 'http:', b)
    for k, v in imgmap.items():
        if re.sub(r'^https?:', 'http:', k) == b and v:
            return '/' + v
    return None

FORM_RE = re.compile(r'<div class="sqs-block form-block sqs-block-form".*?</form>\s*</div>\s*</div>\s*</div></div>', re.S)

def mailto_block(label, subject, body=''):
    href = 'mailto:tom@tougholdmen.com?subject=' + urllib.parse.quote(subject) + ('&body=' + urllib.parse.quote(body) if body else '')
    return ('<div class="sqs-block html-block sqs-block-html"><div class="sqs-block-content">'
            '<p><a class="email-button" href="%s">%s</a></p>'
            '<p>Or write to us directly at <a href="mailto:tom@tougholdmen.com">tom@tougholdmen.com</a>.</p>'
            '</div></div>') % (href, label)

def email_instead_of_form(html, slug):
    if slug == 'contact':
        block = mailto_block('Say hello', 'Hello from the web')
        html = html.replace('stories[at]tougholdmen.com', '<a href="mailto:stories@tougholdmen.com">stories@tougholdmen.com</a>')
        html = html.replace('nate[at]tougholdmen.com', '<a href="mailto:nate@tougholdmen.com">nate@tougholdmen.com</a>')
    else:
        block = mailto_block('Email us to join', 'Join Tough Old Men', 'Name:\nEmail:\nPostal code:\n')
        html = html.replace('Fill out the form and you are in, brother!', 'Send us an email with your name and postal code and you are in, brother!')
    assert FORM_RE.search(html), slug
    return FORM_RE.sub(lambda m: block, html, count=1)

def fix(html, slug):
    # header/footer: use the 2014 versions everywhere
    html = re.sub(r'<header id="header">.*?</header>', lambda m: hdr, html, flags=re.S)
    html = re.sub(r'<footer id="footer">.*?</footer>', lambda m: ftr, html, flags=re.S)
    html = unwayback(html)
    html = html.replace(' active-link','')
    sec = {'home':'/','adventure-story':'/adventure-story/','contact':'/contact/','join':'/join/'}.get(slug, None)
    if sec:
        html = re.sub(r'(<li class=")("\s*>\s*(?:<!--[^>]*-->\s*)*<a href="%s">)' % re.escape(sec), r'\1 active-link\2', html, count=1)
    if slug in ('contact', 'join'):
        html = email_instead_of_form(html, slug)
    # drop scripts (Squarespace runtime), noscript wrappers keep img
    html = re.sub(r'<script\b.*?</script>', '', html, flags=re.S)
    html = re.sub(r'<link[^>]*(?:site\.css|shortcut icon)[^>]*>', '', html)
    html = re.sub(r'<link[^>]*(?:squarespace\.com|sitecss)[^>]*>', '', html)
    html = re.sub(r'</?noscript>', '', html)
    html = re.sub(r'<base href="[^"]*"\s*/?>', '', html)
    # lazy images: data-src -> src
    def lazy(m):
        tag = m.group(0)
        ds = re.search(r'data-src="([^"]*)"', tag)
        if ds and 'src="' not in re.sub(r'data-src="[^"]*"', '', tag):
            tag = tag.replace('<img ', '<img src="%s" ' % ds.group(1), 1)
        return tag
    html = re.sub(r'<img\b[^>]*>', lazy, html)
    # image urls -> local
    def img_sub(m):
        u = m.group(2)
        if 'squarespace.com/static/ta/' in u:
            return m.group(1) + '/assets/img/' + u.split('/')[-1] + '"'
        if 'squarespace.com/static/' in u:
            l = local_img(u)
            if l: return m.group(1) + l + '"'
        return m.group(0)
    html = re.sub(r'((?:src|data-src|data-image|content|href)=")((?:https?:)?//?[^"]*squarespace\.com[^"]*)"', img_sub, html)
    html = re.sub(r'(src=")(https?://[^"]*tom-(?:header-logo|symbol)\.svg)"',
                  lambda m: m.group(1) + '/assets/img/' + m.group(2).split('/')[-1] + '"', html)
    # internal links
    html = re.sub(r'(href=")https?://(?:www\.)?tougholdmen\.com(?::80)?(/[^"]*)"', r'\1\2"', html)
    # favicon & css
    html = html.replace('</head>', '<link rel="shortcut icon" href="/assets/img/favicon.ico">\n<link rel="stylesheet" href="/assets/css/fonts.css">\n<link rel="stylesheet" href="/assets/css/site.css">\n<link rel="stylesheet" href="/assets/css/custom.css">\n</head>')
    return html

for f in sorted(glob.glob(os.path.join(RAW, '*.html'))):
    slug = os.path.basename(f)[:-5]
    s = open(f, encoding='utf8', errors='replace').read()
    o = out_path(slug)
    os.makedirs(os.path.dirname(o) or '.', exist_ok=True)
    open(o, 'w', encoding='utf8').write(fix(s, slug))
    print('wrote', o)
