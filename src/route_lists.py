"""Keep route labels aligned with their values in static medication lists."""
import re


def _items(routes, value=""):
    return ''.join(
        f'<li><strong>{route}</strong>'
        + (f'<span>{value}</span>' if value else '')
        + '</li>'
        for route in routes
    )


def stack_route_lists(body):
    """Expand shared IV/IO list entries without changing doses or curve data.

    Run before glossary markup and mobile table labels. Only route list entries,
    exact route cells and medication Route facts are transformed; prose is kept.
    """
    def peaks(match):
        def entry(item):
            return ''.join(
                '<li' + item[1] + '><strong>' + route + '</strong>' + item[2] + '</li>'
                for route in ('IV', 'IO')
            )
        return re.sub(
            r'<li\b([^>]*)>\s*<strong>IV\s*/\s*IO</strong>(.*?)</li>',
            entry, match[0], flags=re.S,
        )

    body = re.sub(
        r'<ul\b[^>]*class="[^"]*\broute-peaks\b[^"]*"[^>]*>.*?</ul>',
        peaks, body, flags=re.S,
    )

    def route_fact(match):
        prefix, route_text, suffix = match.groups()
        routes = ['IV', 'IO']
        joined = re.match(r'\s+or\s+IM\b', route_text)
        if joined:
            routes.append('IM')
            route_text = route_text[joined.end():]
        # The first clause qualifies the shared route. Keep subsequent notes once.
        parts = re.split(r'[.;]\s*', route_text.strip(), maxsplit=1)
        detail = parts[0].strip()
        note = parts[1].strip() if len(parts) > 1 else ''
        listing = '<ul class="route-peaks route-options">' + _items(routes, detail) + '</ul>'
        if note:
            listing += f'<p class="route-note">{note}</p>'
        return prefix + listing + suffix

    body = re.sub(
        r'(<div class="med-fact"><dt>Route</dt><dd>)IV\s*/\s*IO([^<]*)(</dd></div>)',
        route_fact, body,
    )

    def printable_routes(table):
        # Limit qualifier handling to the Route column of medication print tables.
        # Shared doses elsewhere in the row must retain their original wording.
        headings = re.search(r'<thead\b[^>]*>(.*?)</thead>', table[0], re.S)
        if not headings:
            return table[0]
        labels = [re.sub(r'<[^>]*>', '', heading).strip()
                  for heading in re.findall(r'<th\b[^>]*>(.*?)</th>', headings[1], re.S)]
        if 'Route' not in labels:
            return table[0]
        route_column = labels.index('Route')

        def row(match):
            column = 0

            def cell(match):
                nonlocal column
                current = column
                column += 1
                route = re.fullmatch(r'\s*IV\s*/\s*IO([^<]*)', match[2])
                if current != route_column or not route:
                    return match[0]
                remainder = route[1].strip()
                routes = ['IV', 'IO']
                if re.fullmatch(r'/\s*IM', remainder):
                    routes.append('IM')
                elif remainder.startswith(';'):
                    routes.append(remainder[1:].strip())
                elif remainder:
                    routes = [f'{route} {remainder}' for route in routes]
                items = ''.join(f'<li>{route}</li>' for route in routes)
                return match[1] + f'<ul class="route-names">{items}</ul>' + match[3]

            return re.sub(r'(<t[dh]\b[^>]*>)(.*?)(</t[dh]>)', cell, match[0], flags=re.S)

        return re.sub(r'<tr\b[^>]*>.*?</tr>', row, table[0], flags=re.S)

    body = re.sub(
        r'<table\b[^>]*class="[^"]*\bmedication-print-table\b[^"]*"[^>]*>.*?</table>',
        printable_routes, body, flags=re.S,
    )
    body = re.sub(
        r'(<td\b[^>]*>)\s*IV\s*/\s*IO\s*(</td>)',
        lambda match: match[1] + '<ul class="route-names">'
        + '<li>IV</li><li>IO</li></ul>' + match[2], body,
    )
    return body
