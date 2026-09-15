"""Group complete article sections without rewriting their tables or figures."""
import json
import re
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path


def plain(text):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]*>", " ", text))).strip()


class SectionRanges(HTMLParser):
    def __init__(self, body):
        super().__init__(convert_charrefs=False)
        self.offsets = [0]
        for match in re.finditer("\n", body):
            self.offsets.append(match.end())
        self.depth = 0
        self.ranges = []
        self.feed(body)

    def position(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag == "section":
            if self.depth == 0:
                self.start = self.position()
            self.depth += 1

    def handle_endtag(self, tag):
        if tag == "section":
            self.depth -= 1
            if self.depth == 0:
                self.ranges.append((self.start, self.position() + len("</section>")))


HEADINGS = re.compile(r'<(?P<tag>h[23])\b(?P<attrs>[^>]*)>(?P<body>.*?)</(?P=tag)>', re.S)


def heading_marks(body):
    """Both navigation surfaces and search use the same two-level outline."""
    marks = []
    for match in HEADINGS.finditer(body):
        attrs = match['attrs']
        anchor = re.search(r'\bid="([^"]+)"', attrs)
        if not anchor or (match['tag'] == 'h3' and 'data-wiki-nav="sub"' not in attrs):
            continue
        marks.append((match.start(), 'sub' if match['tag'] == 'h3' else 'sec',
                      anchor[1], plain(match['body']), match.end()))
    return marks


def group_sections(slug, body):
    groups = json.loads(Path(__file__).with_name('page-groups.json').read_text(encoding='utf-8')).get(slug)
    if not groups:
        return body
    ranges = SectionRanges(body).ranges
    sections = {}
    for i, (start, end) in enumerate(ranges):
        # Preserve material between sections with its preceding section.
        next_start = ranges[i + 1][0] if i + 1 < len(ranges) else end
        chunk = body[start:next_start]
        heading = re.search(r'<h2\b[^>]*\bid="([^"]+)"[^>]*>', chunk)
        if not heading:
            raise ValueError(f'{slug}: section has no navigable heading')
        sections[heading[1]] = chunk
    requested = [anchor for group in groups for anchor in group['sections']]
    if len(set(requested)) != len(requested) or set(requested) != set(sections):
        raise ValueError(f'{slug}: update page-groups.json for these sections: {set(requested) ^ set(sections)}')
    result = [body[:ranges[0][0]]]
    for number, group in enumerate(groups, 1):
        anchor = 'topic-' + group['id']
        result.append(f'<section class="topic-group" aria-labelledby="{anchor}">'
                      f'<div class="topic-head"><span class="topic-number" aria-hidden="true">{number:02d}</span>'
                      f'<h2 id="{anchor}">{escape(group["title"])}</h2></div>')
        for child in group['sections']:
            chunk = sections[child]
            chunk = re.sub(r'(<\/?h)([2-5])(\b)', lambda m: m[1] + str(int(m[2]) + 1) + m[3], chunk)
            chunk = re.sub(r'<h3\b', '<h3 data-wiki-nav="sub"', chunk, count=1)
            result.append(chunk)
        result.append('</section>')
    result.append(body[ranges[-1][1]:])
    return '\n'.join(result)


class SourceNotes(HTMLParser):
    """Hide optional citations only when they are outside an existing disclosure."""
    def __init__(self, body):
        super().__init__(convert_charrefs=False)
        self.offsets = [0] + [m.end() for m in re.finditer('\n', body)]
        self.depth = 0
        self.start = None
        self.ranges = []
        self.feed(body)

    def position(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag == 'details':
            self.depth += 1
        classes = dict(attrs).get('class', '').split()
        if tag == 'p' and self.depth == 0 and 'source-note' in classes and 'guide-note' not in classes:
            self.start = self.position()

    def handle_endtag(self, tag):
        if tag == 'p' and self.start is not None:
            self.ranges.append((self.start, self.position() + 4))
            self.start = None
        if tag == 'details':
            self.depth -= 1


def fold_source_notes(body):
    for start, end in reversed(SourceNotes(body).ranges):
        body = (body[:start] + '<details class="source-details"><summary>Sources and revision</summary>'
                + body[start:end] + '</details>' + body[end:])
    return body
