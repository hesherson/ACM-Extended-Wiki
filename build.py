#!/usr/bin/env python3
"""
PILLAR guide builder.

WHY THIS EXISTS. Every output page is SELF-CONTAINED: css inlined, no external stylesheet, no framework. That is
what lets a card survive being emailed, saved to a phone, opened with no signal, and printed. The cost of that is
duplication, so the duplication is moved to build time: you edit one stylesheet and one layout, run this, and every
page is rewritten.

    python3 build.py

    src/_pillar.css       the stylesheet. Edit once, applies everywhere.
    src/content/*.html    one file per page. Body content ONLY, no <html>, no <style>.
    docs/                 output. This is the folder GitHub Pages serves.

ADDING A PAGE: drop a file in src/content/ and add a line to PAGES below. That is the whole process.
ADDING AN IMAGE: put it in docs/img/ and reference it as img/thing.png from any page.
"""
import os, re, datetime, json, sys

sys.dont_write_bytecode = True   # keep src/ free of __pycache__
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
from glossary_terms import TERMS

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "docs")

VERSION = "0.9.873"

# slug, filename, nav title, nav group.
# Order here is the order in the sidebar. Groups are emitted in first-seen order.
PAGES = [
    ("index",        "index.html",        "Start here",          "Overview"),
    ("ventilator",   "ventilator.html",   "Ventilator",          "Systems"),
    ("oxygen",       "oxygen.html",       "Oxygen delivery",     "Systems"),
    ("bleeding",     "bleeding.html",     "Bleeding and shock",  "Systems"),
    ("airway",       "airway.html",       "Airway and chest",    "Systems"),
    ("circulation",  "circulation.html",  "Arrest and Rhythms",  "Systems"),
    ("medications",  "medications.html",  "Medications",         "Systems"),
    ("access",       "access.html",       "Access and blood",    "Systems"),
    ("tbi",          "tbi.html",          "Head injury",         "Systems"),
    ("flight",       "flight.html",       "Flight and altitude", "Systems"),
    ("menu",         "menu.html",         "Medical menu",        "Interface"),
    ("accessibility","accessibility.html","Accessibility",       "Interface"),
    ("overrides",    "overrides.html",    "Advanced Functions / Overrides", "Reference"),
    ("glossary",     "glossary.html",     "Glossary",            "Reference"),
    ("settings",     "settings.html",     "Settings reference",  "Reference"),
    ("zeus",         "zeus.html",         "Zeus modules",        "Reference"),
]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="icon" type="image/png" href="img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;900&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>
<div class="tb-veil" id="veil"></div>
<div class="shell">
"""

FOOT = r"""
<footer>
  <span class="brand">PILLAR</span> // ACM EXTENDED FIELD GUIDE // v{version} // BUILT {built}
</footer>
</main>
</div>
<div id="glpop" class="glpop" hidden>
  <div class="glpop-in">
    <div class="glpop-t"></div>
    <div class="glpop-d"></div>
    <button type="button" class="glpop-x">Close</button>
  </div>
</div>
<script>
var TERMS={terms};
var IDX={index};
(function(){{
  var pop=document.getElementById('glpop');
  var t=pop.querySelector('.glpop-t'), d=pop.querySelector('.glpop-d');
  function open(slug){{
    var e=TERMS[slug]; if(!e) return;
    t.textContent=e[0]; d.textContent=e[1];
    pop.hidden=false; requestAnimationFrame(function(){{pop.classList.add('on');}});
  }}
  function close(){{
    pop.classList.remove('on');
    setTimeout(function(){{pop.hidden=true;}},180);
  }}
  document.addEventListener('click',function(ev){{
    var b=ev.target.closest('.gl');
    if(b){{ ev.preventDefault(); open(b.dataset.t); return; }}
    if(ev.target.closest('.glpop-x') || ev.target===pop) close();
  }});
  document.addEventListener('keydown',function(ev){{ if(ev.key==='Escape') close(); }});

  var q=document.getElementById('q'), qr=document.getElementById('qr');
  function esc(s){{return s.replace(/[&<>]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;'}}[c];}});}}
  function run(){{
    var v=q.value.trim().toLowerCase();
    if(v.length<2){{ qr.hidden=true; qr.innerHTML=''; return; }}
    var words=v.split(/\s+/), hits=[];
    for(var i=0;i<IDX.length;i++){{
      var r=IDX[i], hay=(r.h+' '+r.p+' '+r.t).toLowerCase(), sc=0, ok=true;
      for(var w=0;w<words.length;w++){{
        if(hay.indexOf(words[w])<0){{ ok=false; break; }}
        if(r.h.toLowerCase().indexOf(words[w])>=0) sc+=10;
        if(r.p.toLowerCase().indexOf(words[w])>=0) sc+=4;
        sc+=1;
      }}
      if(ok){{
        var k=r.t.toLowerCase().indexOf(words[0]);
        var sn=k<0?r.t.slice(0,120):r.t.slice(Math.max(0,k-50),k+90);
        hits.push({{r:r,s:sc,sn:sn}});
      }}
    }}
    hits.sort(function(a,b){{return b.s-a.s;}});
    if(!hits.length){{ qr.innerHTML='<div class="tb-none">Nothing found</div>'; qr.hidden=false; return; }}
    qr.innerHTML=hits.slice(0,12).map(function(h){{
      var href=h.r.f+(h.r.a?'#'+h.r.a:'');
      return '<a href="'+href+'"><span class="tb-p">'+esc(h.r.p)+'</span>'+
             '<span class="tb-h">'+esc(h.r.h)+'</span>'+
             '<span class="tb-s">'+esc(h.sn)+'</span></a>';
    }}).join('');
    qr.hidden=false;
  }}
  // Contents rail: highlight the section currently in view. Read-only, so nothing here can block the page.
  var toc=document.querySelector('.toc');
  if(toc){{
    var links=[].slice.call(toc.querySelectorAll('a'));
    var heads=links.map(function(a){{ return document.getElementById(a.dataset.a); }});
    var tick=false;
    function spy(){{
      var best=0, y=window.scrollY+140;
      for(var i=0;i<heads.length;i++){{ if(heads[i] && heads[i].offsetTop<=y) best=i; }}
      links.forEach(function(a,i){{ a.classList.toggle('on', i===best); }});
      tick=false;
    }}
    window.addEventListener('scroll',function(){{
      if(!tick){{ tick=true; requestAnimationFrame(spy); }}
    }},{{passive:true}});
    spy();
  }}

  var veil=document.getElementById('veil');
  function focusMode(on){{ veil.classList.toggle('on',on); }}
  function dismiss(){{ qr.hidden=true; focusMode(false); q.blur(); }}

  // RESET ON ARRIVAL. A page restored from the back/forward cache keeps the DOM exactly as it was left,
  // including a focused search box and a lit veil, which locked the page until a manual reload. Clearing
  // on pageshow covers both a fresh load and a restore.
  window.addEventListener('pageshow',function(){{
    qr.hidden=true; veil.classList.remove('on');
    if(document.activeElement===q) q.blur();
  }});

  q.addEventListener('input',run);
  q.addEventListener('focus',function(){{ focusMode(true); run(); }});
  q.addEventListener('blur',function(){{ setTimeout(function(){{
    if(!qr.matches(':hover')) focusMode(false);
  }},120); }});
  veil.addEventListener('click',dismiss);
  document.addEventListener('click',function(ev){{
    if(!ev.target.closest('.tb-wrap') && !ev.target.closest('.tb-veil')) {{ qr.hidden=true; focusMode(false); }}
  }});
  q.addEventListener('keydown',function(ev){{ if(ev.key==='Escape') dismiss(); }});

  }})();
</script>
</body>
</html>
"""




def apply_terms(body):
    """{{slug}} or {{slug|shown text}} becomes a clickable term. Unknown slugs are reported rather than
    silently rendered as literal braces, because a typo would otherwise ship as visible junk."""
    missing = []

    def sub(m):
        raw = m.group(1)
        slug, _, shown = raw.partition("|")
        slug = slug.strip()
        if slug not in TERMS:
            missing.append(slug)
            return shown or slug
        label = shown.strip() if shown else TERMS[slug][0]
        return f'<button type="button" class="gl" data-t="{slug}">{label}</button>'

    return re.sub(r"\{\{([^}]+)\}\}", sub, body), missing


def add_anchors(body):
    """Give every h2 an id so search results and the sidebar can deep link to a section."""
    def sub(m):
        text = re.sub(r"<[^>]+>", "", m.group(1))
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return f'<h2 id="{slug}">{m.group(1)}</h2>'
    return re.sub(r"<h2>(.*?)</h2>", sub, body)


def add_card_anchors(body):
    """Give drug cards and injury cards ids too. On a page like medications the h2 sections are only
    scaffolding and the real navigation targets are the 19 cards, so the rail needs to reach them."""
    def drug(m):
        slug = re.sub(r"[^a-z0-9]+", "-", m.group(1).lower()).strip("-")
        return f'<div class="drug" id="d-{slug}"><header><span class="dn">{m.group(1)}</span>'
    body = re.sub(r'<div class="drug">\s*<header><span class="dn">([^<]+)</span>', drug, body)

    def inj(m):
        slug = re.sub(r"[^a-z0-9]+", "-", m.group(1).lower()).strip("-")
        return f'<article class="icard" id="c-{slug}"><header><span class="iname">{m.group(1)}</span>'
    body = re.sub(r'<article class="icard">\s*<header><span class="iname">([^<]+)</span>', inj, body)
    return body


def toc(body):
    """Right hand contents rail, in document order. Sections come from the h2 anchors, and named cards
    are nested under whichever section they fall in, so the rail matches what the reader actually sees."""
    marks = []
    for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S):
        marks.append((m.start(), "sec", m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()))
    for m in re.finditer(r'id="d-([\w-]+)"><header><span class="dn">([^<]+)<', body):
        marks.append((m.start(), "sub", "d-" + m.group(1), m.group(2).strip()))
    for m in re.finditer(r'id="c-([\w-]+)"><header><span class="iname">([^<]+)<', body):
        marks.append((m.start(), "sub", "c-" + m.group(1), m.group(2).strip()))
    marks.sort()
    if len(marks) < 2:
        return ""
    out = ['<aside class="toc"><div class="toc-h">On this page</div><nav>']
    for _, kind, anchor, label in marks:
        cls = " class=\"sub\"" if kind == "sub" else ""
        out.append(f'  <a{cls} href="#{anchor}" data-a="{anchor}">{label}</a>')
    out += ["</nav></aside>"]
    return "\n".join(out)


def index_page(slug, fname, title, body):
    """One search record per section: page, heading, anchor, and the visible text under it."""
    recs = []
    parts = re.split(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    lead = re.sub(r"<[^>]+>", " ", parts[0])
    recs.append({"p": title, "f": fname, "a": "", "h": title,
                 "t": re.sub(r"\s+", " ", lead).strip()[:900]})
    for i in range(1, len(parts), 3):
        anchor, head, chunk = parts[i], parts[i + 1], parts[i + 2]
        head = re.sub(r"<[^>]+>", "", head)
        txt = re.sub(r"<[^>]+>", " ", chunk)
        recs.append({"p": title, "f": fname, "a": anchor, "h": head,
                     "t": re.sub(r"\s+", " ", txt).strip()[:900]})
    return recs


def glossary_page():
    """Generated from TERMS so the glossary and the popups can never disagree."""
    out = ['<div class="eyebrow">PILLAR <span class="tag">//</span> REFERENCE</div>',
           "<h1>Glossary</h1>",
           '<p class="lede">Every advanced term used in this guide, in plain language. Anywhere a term appears '
           "underlined you can tap it to see this same definition without leaving the page.</p>",
           '<div class="rule"></div>',
           '<section class="sec"><div class="sec-head"><span class="sec-num">01</span><h2>All Terms</h2></div>',
           '<div class="glist">']
    for slug in sorted(TERMS, key=lambda k: TERMS[k][0].lower()):
        name, desc = TERMS[slug]
        out.append(f'  <div class="gitem" id="term-{slug}"><div class="gt">{name}</div><div class="gd">{desc}</div></div>')
    out += ["</div>", "</section>"]
    return "\n".join(out)


def sidebar(current):
    """Sidebar nav. Search sits at the top of it. Every link carries an index so CSS can stagger the
    cascade without any JavaScript, which means the animation can never get stuck part way."""
    out = ['<aside class="side">',
           '  <div class="side-head">',
           '    <a class="brand" href="index.html"><img src="img/pillar_mark.png" alt="PILLAR"></a>',
           f'    <div class="ver">ACM Extended // v{VERSION}</div>',
           '  </div>',
           '  <div class="tb-wrap">',
           '    <input id="q" class="tb-q" type="search" placeholder="Search" autocomplete="off" spellcheck="false">',
           '    <div id="qr" class="tb-res" hidden></div>',
           '  </div>',
           '  <nav class="nav">']
    seen = []
    i = 0
    for slug, fname, title, group in PAGES:
        if group not in seen:
            seen.append(group)
            out.append(f'    <div class="grp" style="--i:{i}">{group}</div>')
            i += 1
        cls = "on" if slug == current else ""
        out.append(f'    <a class="{cls}" style="--i:{i}" href="{fname}">{title}</a>')
        i += 1
    out += ['  </nav>', '</aside>', '<main class="main">']
    return "\n".join(out)


def build():
    css = open(os.path.join(SRC, "_pillar.css"), encoding="utf-8").read()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
    built = datetime.date.today().isoformat()

    # PASS 1: read and transform every body, and build the search index from the result.
    bodies, index, missing, badterms = {}, [], [], []
    for slug, fname, title, group in PAGES:
        if slug == "glossary":
            body = glossary_page()
        else:
            cpath = os.path.join(SRC, "content", slug + ".html")
            if not os.path.exists(cpath):
                missing.append(slug)
                continue
            body = open(cpath, encoding="utf-8").read()
        body, miss = apply_terms(body)
        badterms += [(slug, m) for m in miss]
        body = add_anchors(body)
        body = add_card_anchors(body)
        bodies[slug] = body
        index += index_page(slug, fname, title, body)

    # PASS 2: write pages. The index is inlined into each page rather than fetched, so a page still
    # searches when opened from disk with no server behind it.
    idx_json = json.dumps(index, separators=(",", ":"))
    terms_json = json.dumps({k: list(v) for k, v in TERMS.items()}, separators=(",", ":"))
    for slug, fname, title, group in PAGES:
        if slug not in bodies:
            continue
        page = (HEAD.format(title=f"ACM Extended Wiki | {title}", css=css)
                + sidebar(slug) + "\n" + toc(bodies[slug]) + "\n" + bodies[slug]
                + FOOT.format(version=VERSION, built=built, terms=terms_json, index=idx_json))
        open(os.path.join(OUT, fname), "w", encoding="utf-8").write(page)

    open(os.path.join(OUT, ".nojekyll"), "w").write("")

    print(f"built {len(bodies)} page(s), {len(index)} search records, {len(TERMS)} glossary terms")
    if badterms:
        print("UNKNOWN GLOSSARY TERMS (add to src/glossary_terms.py):")
        for pg, t in badterms:
            print(f"  {pg}: {{{{{t}}}}}")
    if missing:
        print("no content file yet for: " + ", ".join(missing))


if __name__ == "__main__":
    build()
