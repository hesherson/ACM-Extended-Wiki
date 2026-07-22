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
<meta http-equiv="Cache-Control" content="no-cache, must-revalidate">
<title>{title}</title>
<link rel="icon" type="image/png" href="img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;900&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
{css}
</style>
<script>
/* Runs before the body paints. Without this the page renders warm, then snaps to black once the
   footer script gets to run, which is worse than having no night mode at all. */
try{{if(localStorage.getItem('pillarNight')==='1'){{document.documentElement.className='night';}}}}catch(e){{}}
</script>
</head>
<body>
<div class="tb-veil" id="veil"></div>
<div class="shell">
"""

FOOT = r"""
<footer>
  <span class="brand">PILLAR</span> // ACM EXTENDED FIELD GUIDE // v{version} // BUILD {built}
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

  // HOVER TO OPEN after a deliberate pause, so passing the cursor over a term does not fire it.
  // Clicking still opens immediately. Touch devices never fire mouseenter, so they get the click path.
  var hoverT=null, armed=null;
  function clearArm(){{
    if(hoverT){{ clearTimeout(hoverT); hoverT=null; }}
    if(armed){{ armed.classList.remove('arming'); armed=null; }}
  }}
  document.addEventListener('mouseover',function(ev){{
    var b=ev.target.closest('.gl');
    if(!b || b===armed) return;
    clearArm();
    armed=b; b.classList.add('arming');
    hoverT=setTimeout(function(){{ open(b.dataset.t); clearArm(); }},1000);
  }});
  document.addEventListener('mouseout',function(ev){{
    var b=ev.target.closest('.gl');
    if(b && b===armed) clearArm();
  }});

  document.addEventListener('click',function(ev){{
    var b=ev.target.closest('.gl');
    if(b){{ ev.preventDefault(); clearArm(); open(b.dataset.t); return; }}
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
  // SECTION BAR. Tracks which section is in view, fills a progress line, and collapses to a thin strip
  // once the reader is past the top. Read-only apart from the toggle, so it cannot block the page.
  var sb=document.getElementById('secbar');
  if(sb){{
    var list=document.getElementById('sbList'), now=document.getElementById('sbNow');
    var cur=document.getElementById('sbCur'), prog=document.getElementById('sbProg');
    var links=[].slice.call(list.querySelectorAll('a'));
    var heads=links.map(function(a){{ return document.getElementById(a.dataset.a); }});
    var tick=false;
    function spy(){{
      var y=window.scrollY, best=0;
      for(var i=0;i<heads.length;i++){{ if(heads[i] && heads[i].offsetTop<=y+120) best=i; }}
      links.forEach(function(a,i){{ a.classList.toggle('on', i===best); }});
      if(cur.textContent!==links[best].textContent) cur.textContent=links[best].textContent;
      var doc=document.documentElement.scrollHeight-window.innerHeight;
      prog.style.width=(doc>0 ? Math.min(100,(y/doc)*100) : 0)+'%';
      sb.classList.toggle('thin', y>90);
      tick=false;
    }}
    window.addEventListener('scroll',function(){{
      if(!tick){{ tick=true; requestAnimationFrame(spy); }}
    }},{{passive:true}});
    now.addEventListener('click',function(){{
      var open=list.hidden;
      list.hidden=!open;
      now.setAttribute('aria-expanded', open?'true':'false');
      sb.classList.toggle('open', open);
    }});
    list.addEventListener('click',function(ev){{
      if(ev.target.tagName==='A'){{
        list.hidden=true; sb.classList.remove('open');
        now.setAttribute('aria-expanded','false');
      }}
    }});
    document.addEventListener('click',function(ev){{
      if(!ev.target.closest('.secbar') && !list.hidden){{
        list.hidden=true; sb.classList.remove('open');
        now.setAttribute('aria-expanded','false');
      }}
    }});
    // A page restored from the back/forward cache keeps the DOM as it was left, so a list
    // left open would come back open. Same reason the search box is reset on pageshow.
    function sbShut(){{
      list.hidden=true; sb.classList.remove('open');
      now.setAttribute('aria-expanded','false');
    }}
    window.addEventListener('pageshow',sbShut);
    document.addEventListener('keydown',function(ev){{
      if(ev.key==='Escape' && !list.hidden) sbShut();
    }});
    spy();
  }}

  // SIDEBAR SUBNAV. Marks which section of the current page is in view. Kept independent of the
  // section bar above, so it still works on a page with too few headings to be given one.
  var sn=document.querySelector('.subnav');
  if(sn){{
    var sLinks=[].slice.call(sn.querySelectorAll('a'));
    var sHeads=sLinks.map(function(a){{ return document.getElementById(a.dataset.s); }});
    var sTick=false;
    function sspy(){{
      var y=window.scrollY, best=0;
      for(var i=0;i<sHeads.length;i++){{ if(sHeads[i] && sHeads[i].offsetTop<=y+120) best=i; }}
      sLinks.forEach(function(a,i){{ a.classList.toggle('on', i===best); }});
      sTick=false;
    }}
    window.addEventListener('scroll',function(){{
      if(!sTick){{ sTick=true; requestAnimationFrame(sspy); }}
    }},{{passive:true}});
    sspy();
  }}

  // NIGHT MODE. Backgrounds only. The class is already on <html> from the head script if it was
  // left on, so this just keeps the button in step and writes the choice back.
  var nb=document.getElementById('nightBtn');
  if(nb){{
    function nightSet(on){{
      document.documentElement.classList.toggle('night',on);
      nb.setAttribute('aria-pressed',on?'true':'false');
    }}
    nightSet(document.documentElement.classList.contains('night'));
    nb.addEventListener('click',function(){{
      var on=!document.documentElement.classList.contains('night');
      nightSet(on);
      // Storage can be blocked entirely by browser settings. Losing the preference between pages is
      // survivable, a thrown error that halts the rest of this script is not.
      try{{ localStorage.setItem('pillarNight',on?'1':'0'); }}catch(e){{}}
    }});
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
    """Sticky section bar. Sits at the top of the content column, opaque so nothing shows through it,
    and collapses to a thin strip as the reader scrolls. Sections come from the h2 anchors, and named
    cards nest under them, so it can never disagree with the page."""
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
    out = ['<div class="secbar" id="secbar">',
           '  <div class="sb-in">',
           '    <button type="button" class="sb-now" id="sbNow" aria-expanded="false">',
           '      <span class="sb-lab">On this page</span>',
           '      <span class="sb-cur" id="sbCur"></span>',
           '      <span class="sb-caret"></span>',
           '    </button>',
           '    <div class="sb-prog"><i id="sbProg"></i></div>',
           '  </div>',
           '  <nav class="sb-list" id="sbList" hidden>']
    for _, kind, anchor, label in marks:
        cls = ' class="sub"' if kind == "sub" else ""
        out.append(f'    <a{cls} href="#{anchor}" data-a="{anchor}">{label}</a>')
    out += ["  </nav>", "</div>"]
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


def page_sections(body):
    """h2 anchors for one page. Only the page being viewed gets these in the sidebar, so the nav stays
    a list of pages rather than expanding into a full site outline."""
    return [(m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip())
            for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S)]


def sidebar(current, sections=()):
    """Sidebar nav, with the sections of the current page nested under its own link. Search sits at
    the top. Sub links are same page anchors, so following one never reloads."""
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
    for slug, fname, title, group in PAGES:
        if group not in seen:
            seen.append(group)
            out.append(f'    <div class="grp">{group}</div>')
        cls = ' class="on"' if slug == current else ""
        out.append(f'    <a{cls} href="{fname}">{title}</a>')
        if slug == current and sections:
            out.append('    <div class="subnav">')
            for anchor, label in sections:
                out.append(f'      <a href="#{anchor}" data-s="{anchor}">{label}</a>')
            out.append('    </div>')
    out += ['  </nav>',
            '  <button type="button" class="nightbtn" id="nightBtn" aria-pressed="false">',
            '    <span class="nb-lab">Night mode</span>',
            '    <span class="nb-sw"><i></i></span>',
            '  </button>',
            '</aside>', '<main class="main">']
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
                + sidebar(slug, page_sections(bodies[slug])) + "\n" + toc(bodies[slug]) + "\n" + bodies[slug]
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
