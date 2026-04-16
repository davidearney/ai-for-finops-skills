#!/usr/bin/env python3
"""Convert markdown files to Google Docs-friendly HTML with proper tables."""

import re
import sys
from pathlib import Path


def parse_ascii_table(block):
    """Parse an ASCII table from a code block into rows of cells."""
    lines = block.strip().split('\n')
    rows = []
    current_row = None
    num_cols = None

    for line in lines:
        stripped = line.strip()
        # Skip separator lines (---+--- or ===+=== or ---|--- etc)
        if stripped and all(c in '-+=| ' for c in stripped) and ('|' in stripped or '+' in stripped) and not any(c.isalpha() for c in stripped):
            continue
        # Skip empty lines
        if not stripped:
            continue

        # Check if this line has pipe-separated content
        if '|' in stripped:
            # Determine if this is a continuation line by checking if
            # the text before the first | in the ORIGINAL line is all whitespace
            before_first_pipe = line.split('|')[0]
            is_continuation = before_first_pipe.strip() == '' and current_row is not None and before_first_pipe != ''

            # Split into cells
            parts = [p.strip() for p in line.split('|')]

            if is_continuation and current_row is not None:
                # For continuations, keep all parts to preserve column alignment.
                # The line "          | content |" splits into ['', 'content', '']
                # which aligns with [col0, col1, col2] - DON'T strip empties.
                all_parts = [p.strip() for p in line.split('|')]
                # Only remove trailing empty if it's an extra (more parts than columns)
                while len(all_parts) > num_cols and all_parts and all_parts[-1] == '':
                    all_parts.pop()

                # Merge aligned parts into current row
                for i, part in enumerate(all_parts):
                    if i < len(current_row) and part:
                        if current_row[i]:
                            current_row[i] += ' ' + part
                        else:
                            current_row[i] = part
            else:
                # New row
                if current_row is not None:
                    rows.append(current_row)

                # Clean parts: remove empty edges
                all_parts = [p.strip() for p in line.split('|')]
                while all_parts and all_parts[0] == '':
                    all_parts.pop(0)
                while all_parts and all_parts[-1] == '':
                    all_parts.pop()

                current_row = all_parts
                if num_cols is None:
                    num_cols = len(current_row)
        else:
            # Non-pipe line in a code block - might be a non-table code block
            return None

    if current_row is not None:
        rows.append(current_row)

    if len(rows) < 2:
        return None

    return rows


def ascii_table_to_html(rows):
    """Convert parsed table rows to HTML table."""
    if not rows:
        return ''

    html = '<table style="border-collapse: collapse; width: 100%; margin: 12px 0;">\n'

    # First row is header
    html += '  <thead>\n    <tr>\n'
    for cell in rows[0]:
        html += '      <th style="border: 1px solid #ccc; padding: 8px 12px; background-color: #f5f5f5; font-weight: bold; text-align: left;">{}</th>\n'.format(cell)
    html += '    </tr>\n  </thead>\n'

    # Remaining rows are body
    html += '  <tbody>\n'
    for row in rows[1:]:
        html += '    <tr>\n'
        for i, cell in enumerate(row):
            # Pad if row has fewer cells than header
            html += '      <td style="border: 1px solid #ccc; padding: 8px 12px; vertical-align: top;">{}</td>\n'.format(cell)
        html += '    </tr>\n'
    html += '  </tbody>\n'
    html += '</table>\n'

    return html


def parse_gap_analysis(block):
    """Parse the gap analysis block which uses [covered]/[partial]/[gap] markers."""
    lines = block.strip().split('\n')
    sections = {}
    current_section = None
    items = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith('What TBM provides'):
            if current_section and items:
                sections[current_section] = items
            current_section = stripped.rstrip(':')
            items = []
        elif stripped.startswith('['):
            # Extract tag and content
            match = re.match(r'\[(\w+)\]\s+(.*)', stripped)
            if match:
                tag = match.group(1)
                content = match.group(2)
                items.append((tag, content))
        elif current_section and items:
            # Continuation of previous item
            items[-1] = (items[-1][0], items[-1][1] + ' ' + stripped)

    if current_section and items:
        sections[current_section] = items

    if not sections:
        return None

    # Build HTML
    html = ''
    tag_colors = {
        'covered': '#e6f4ea',
        'partial': '#fef7e0',
        'gap': '#fce8e6'
    }
    tag_labels = {
        'covered': 'Covered',
        'partial': 'Partial',
        'gap': 'Gap'
    }

    for section_name, section_items in sections.items():
        html += '<p><strong>{}</strong></p>\n'.format(section_name + ':')
        html += '<table style="border-collapse: collapse; width: 100%; margin: 8px 0 16px 0;">\n'
        for tag, content in section_items:
            color = tag_colors.get(tag, '#f5f5f5')
            label = tag_labels.get(tag, tag)
            html += '  <tr>\n'
            html += '    <td style="border: 1px solid #ccc; padding: 6px 10px; width: 80px; text-align: center; background-color: {}; font-weight: bold; font-size: 0.9em;">{}</td>\n'.format(color, label)
            html += '    <td style="border: 1px solid #ccc; padding: 6px 10px;">{}</td>\n'.format(content)
            html += '  </tr>\n'
        html += '</table>\n'

    return html


def convert_code_block(block_content):
    """Try to convert a code block to an HTML table, or return as-is."""
    # Check if it's the gap analysis block
    if '[covered]' in block_content or '[partial]' in block_content or '[gap]' in block_content:
        result = parse_gap_analysis(block_content)
        if result:
            return result

    # Try parsing as ASCII table
    rows = parse_ascii_table(block_content)
    if rows:
        return ascii_table_to_html(rows)

    # Not a table - return as formatted code
    return '<pre style="background-color: #f5f5f5; padding: 12px; border-radius: 4px; overflow-x: auto; font-size: 0.9em;">{}</pre>\n'.format(block_content)


def md_pipe_table_to_html(table_text):
    """Convert a markdown pipe table to HTML."""
    lines = [l.strip() for l in table_text.strip().split('\n') if l.strip()]
    if len(lines) < 2:
        return table_text

    rows = []
    for line in lines:
        # Skip separator lines
        if re.match(r'^[\s|:-]+$', line):
            continue
        cells = [c.strip() for c in line.split('|')]
        # Remove empty first/last from leading/trailing pipes
        if cells and cells[0] == '':
            cells = cells[1:]
        if cells and cells[-1] == '':
            cells = cells[:-1]
        if cells:
            rows.append(cells)

    if len(rows) < 2:
        return table_text

    html = '<table style="border-collapse: collapse; width: 100%; margin: 12px 0;">\n'
    html += '  <thead>\n    <tr>\n'
    for cell in rows[0]:
        # Process inline markdown in cells
        cell = process_inline(cell)
        html += '      <th style="border: 1px solid #ccc; padding: 8px 12px; background-color: #f5f5f5; font-weight: bold; text-align: left;">{}</th>\n'.format(cell)
    html += '    </tr>\n  </thead>\n'

    html += '  <tbody>\n'
    for row in rows[1:]:
        html += '    <tr>\n'
        for cell in row:
            cell = process_inline(cell)
            html += '      <td style="border: 1px solid #ccc; padding: 8px 12px; vertical-align: top;">{}</td>\n'.format(cell)
        html += '    </tr>\n'
    html += '  </tbody>\n'
    html += '</table>\n'

    return html


def process_inline(text):
    """Process inline markdown formatting."""
    # Bold + italic
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`(.*?)`', r'<code style="background-color: #f0f0f0; padding: 2px 4px; border-radius: 3px; font-size: 0.9em;">\1</code>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def markdown_to_html(md_text, title="Document"):
    """Convert markdown to clean HTML suitable for Google Docs."""
    html_parts = []

    # HTML header with styling
    html_parts.append('''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {{
    font-family: Arial, sans-serif;
    max-width: 900px;
    margin: 40px auto;
    padding: 0 20px;
    line-height: 1.6;
    color: #333;
}}
h1 {{ font-size: 1.8em; margin-top: 24px; margin-bottom: 8px; }}
h2 {{ font-size: 1.4em; margin-top: 24px; margin-bottom: 8px; border-bottom: 1px solid #eee; padding-bottom: 4px; }}
h3 {{ font-size: 1.15em; margin-top: 20px; margin-bottom: 8px; }}
h4 {{ font-size: 1em; margin-top: 16px; margin-bottom: 6px; }}
p {{ margin: 8px 0; }}
hr {{ border: none; border-top: 1px solid #ccc; margin: 20px 0; }}
ol, ul {{ margin: 8px 0; padding-left: 24px; }}
li {{ margin: 4px 0; }}
blockquote {{ border-left: 3px solid #ccc; margin: 12px 0; padding: 8px 16px; color: #555; }}
</style>
</head>
<body>
'''.format(title=title))

    lines = md_text.split('\n')
    i = 0
    in_list = False
    list_type = None

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Code block (```)
        if stripped.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```

            if in_list:
                html_parts.append('</{}>\n'.format('ol' if list_type == 'ol' else 'ul'))
                in_list = False

            block_content = '\n'.join(code_lines)
            html_parts.append(convert_code_block(block_content))
            continue

        # Pipe table detection
        if '|' in stripped and not stripped.startswith('```'):
            # Check if this is a markdown pipe table
            if re.match(r'^\|.*\|$', stripped):
                table_lines = [line]
                j = i + 1
                while j < len(lines) and '|' in lines[j].strip() and lines[j].strip():
                    table_lines.append(lines[j])
                    j += 1
                if len(table_lines) >= 3:  # header + separator + at least one row
                    if in_list:
                        html_parts.append('</{}>\n'.format('ol' if list_type == 'ol' else 'ul'))
                        in_list = False
                    html_parts.append(md_pipe_table_to_html('\n'.join(table_lines)))
                    i = j
                    continue

        # Horizontal rule
        if stripped == '---' or stripped == '***' or stripped == '___':
            if in_list:
                html_parts.append('</{}>\n'.format('ol' if list_type == 'ol' else 'ul'))
                in_list = False
            html_parts.append('<hr>\n')
            i += 1
            continue

        # Headers
        header_match = re.match(r'^(#{1,6})\s+(.*)', stripped)
        if header_match:
            if in_list:
                html_parts.append('</{}>\n'.format('ol' if list_type == 'ol' else 'ul'))
                in_list = False
            level = len(header_match.group(1))
            content = process_inline(header_match.group(2))
            html_parts.append('<h{0}>{1}</h{0}>\n'.format(level, content))
            i += 1
            continue

        # Ordered list
        ol_match = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if ol_match:
            if not in_list or list_type != 'ol':
                if in_list:
                    html_parts.append('</{}>\n'.format('ol' if list_type == 'ol' else 'ul'))
                html_parts.append('<ol>\n')
                in_list = True
                list_type = 'ol'
            content = process_inline(ol_match.group(2))
            html_parts.append('  <li>{}</li>\n'.format(content))
            i += 1
            continue

        # Unordered list
        ul_match = re.match(r'^[-*]\s+(.*)', stripped)
        if ul_match:
            if not in_list or list_type != 'ul':
                if in_list:
                    html_parts.append('</{}>\n'.format('ol' if list_type == 'ol' else 'ul'))
                html_parts.append('<ul>\n')
                in_list = True
                list_type = 'ul'
            content = process_inline(ul_match.group(1))
            html_parts.append('  <li>{}</li>\n'.format(content))
            i += 1
            continue

        # End list if we hit a non-list line
        if in_list and stripped and not ol_match and not ul_match:
            html_parts.append('</{}>\n'.format('ol' if list_type == 'ol' else 'ul'))
            in_list = False

        # Empty line
        if not stripped:
            i += 1
            continue

        # Regular paragraph
        para_lines = [stripped]
        j = i + 1
        while j < len(lines):
            next_stripped = lines[j].strip()
            if not next_stripped:
                break
            if next_stripped.startswith('#'):
                break
            if next_stripped.startswith('```'):
                break
            if next_stripped == '---' or next_stripped == '***':
                break
            if re.match(r'^\|.*\|$', next_stripped):
                break
            if re.match(r'^[-*]\s+', next_stripped):
                break
            if re.match(r'^\d+\.\s+', next_stripped):
                break
            para_lines.append(next_stripped)
            j += 1

        content = process_inline(' '.join(para_lines))
        html_parts.append('<p>{}</p>\n'.format(content))
        i = j
        continue

    if in_list:
        html_parts.append('</{}>\n'.format('ol' if list_type == 'ol' else 'ul'))

    html_parts.append('</body>\n</html>\n')
    return ''.join(html_parts)


def main():
    if len(sys.argv) < 3:
        print("Usage: python convert_md_to_html.py <input.md> <output.html> [title]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else "Document"

    md_text = Path(input_path).read_text(encoding='utf-8')
    html = markdown_to_html(md_text, title)
    Path(output_path).write_text(html, encoding='utf-8')
    print("Converted {} -> {} ({} chars)".format(input_path, output_path, len(html)))


if __name__ == '__main__':
    main()
