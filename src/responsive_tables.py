"""Add column labels at build time so small-screen tables also work offline/no JS."""
import re
from html import escape, unescape


def responsive_tables(body):
    def table(match):
        html = match.group(0)
        head = re.search(r'<thead\b[^>]*>(.*?)</thead>', html, re.S)
        if not head:
            return html
        labels = [unescape(re.sub(r'<[^>]*>', '', text)).strip()
                  for text in re.findall(r'<th\b[^>]*>(.*?)</th>', head[1], re.S)]
        html = re.sub(r'<table\b', '<table role="table"', html, count=1)
        def tbody(match):
            def row(match):
                column = 0
                def cell(match):
                    nonlocal column
                    tag, attrs, content = match.groups()
                    label = labels[column] if column < len(labels) else ''
                    column += 1
                    role = 'rowheader' if tag == 'th' else 'cell'
                    return (f'<{tag}{attrs} role="{role}"><span class="mobile-column-label" aria-hidden="true" data-no-glossary>'
                            f'{escape(label)}</span><div class="table-value">{content}</div></{tag}>')
                contents = re.sub(r'<(td|th)\b([^>]*)>(.*?)</\1>', cell, match[2], flags=re.S)
                return f'<tr{match[1]} role="row">{contents}</tr>'
            contents = re.sub(r'<tr\b([^>]*)>(.*?)</tr>', row, match[2], flags=re.S)
            return f'<tbody{match[1]} role="rowgroup">{contents}</tbody>'
        return re.sub(r'<tbody\b([^>]*)>(.*?)</tbody>', tbody, html, flags=re.S)
    return re.sub(r'<table\b[^>]*>.*?</table>', table, body, flags=re.S)
