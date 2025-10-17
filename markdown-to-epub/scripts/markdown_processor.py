"""
Markdown processing module for converting markdown to EPUB-compatible structure.

This module handles:
- Parsing markdown into chapters and sections
- Converting markdown to HTML
- Extracting metadata and structure
- Building table of contents
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class HeaderLevel(Enum):
    """Header hierarchy levels."""
    H1 = 1
    H2 = 2
    H3 = 3
    H4 = 4
    H5 = 5
    H6 = 6


@dataclass
class Header:
    """Represents a markdown header."""
    level: HeaderLevel
    text: str
    anchor: Optional[str] = None

    def __post_init__(self):
        if not self.anchor:
            # Generate anchor from text
            self.anchor = re.sub(r'[^\w\s-]', '', self.text.lower())
            self.anchor = re.sub(r'[-\s]+', '-', self.anchor).strip('-')


@dataclass
class Chapter:
    """Represents a chapter (H1 section)."""
    title: str
    content: str
    sections: List['Section']
    anchor: Optional[str] = None

    def __post_init__(self):
        if not self.anchor:
            self.anchor = re.sub(r'[^\w\s-]', '', self.title.lower())
            self.anchor = re.sub(r'[-\s]+', '-', self.anchor).strip('-')


@dataclass
class Section:
    """Represents a section (H2-H6)."""
    title: str
    level: int
    content: str
    anchor: Optional[str] = None

    def __post_init__(self):
        if not self.anchor:
            self.anchor = re.sub(r'[^\w\s-]', '', self.title.lower())
            self.anchor = re.sub(r'[-\s]+', '-', self.anchor).strip('-')


@dataclass
class EbookMetadata:
    """Metadata for the ebook."""
    title: Optional[str] = None
    author: Optional[str] = "Unknown Author"
    language: str = "en"
    date: Optional[str] = None
    identifier: Optional[str] = None


class MarkdownProcessor:
    """Process markdown content into EPUB-compatible structure."""

    def __init__(self):
        """Initialize the markdown processor."""
        self.chapters: List[Chapter] = []
        self.metadata = EbookMetadata()
        self.front_matter: Dict[str, str] = {}

    def process(self, markdown_content: str) -> Dict:
        """
        Process markdown content into structured format.

        Args:
            markdown_content: Raw markdown text

        Returns:
            Dictionary containing chapters, metadata, and TOC
        """
        # Extract front matter if present
        content = self._extract_frontmatter(markdown_content)

        # Extract metadata from headers
        self._extract_metadata(content)

        # Parse content into chapters
        self.chapters = self._parse_chapters(content)

        # Build table of contents
        toc = self._build_toc()

        return {
            'chapters': self.chapters,
            'metadata': self.metadata,
            'toc': toc,
            'front_matter': self.front_matter
        }

    def _extract_frontmatter(self, content: str) -> str:
        """
        Extract YAML front matter if present.

        Args:
            content: Raw markdown content

        Returns:
            Markdown content without front matter
        """
        if not content.startswith('---'):
            return content

        # Find closing ---
        try:
            end_idx = content.index('---', 3)
            fm_text = content[3:end_idx].strip()

            # Parse simple key: value pairs
            for line in fm_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    self.front_matter[key.strip().lower()] = value.strip()

            # Update metadata from front matter
            if 'title' in self.front_matter:
                self.metadata.title = self.front_matter['title']
            if 'author' in self.front_matter:
                self.metadata.author = self.front_matter['author']
            if 'date' in self.front_matter:
                self.metadata.date = self.front_matter['date']
            if 'language' in self.front_matter:
                self.metadata.language = self.front_matter['language']

            return content[end_idx + 3:].lstrip()
        except ValueError:
            return content

    def _extract_metadata(self, content: str) -> None:
        """
        Extract metadata from document headers.

        Args:
            content: Markdown content
        """
        # If no title from front matter, use first H1
        if not self.metadata.title:
            h1_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if h1_match:
                self.metadata.title = h1_match.group(1).strip()

    def _parse_chapters(self, content: str) -> List[Chapter]:
        """
        Parse markdown into chapters.

        Chapters are delimited by H1 headers. Content between H1s
        becomes a chapter with potential subsections (H2-H6).

        Args:
            content: Markdown content

        Returns:
            List of Chapter objects
        """
        # Split by H1 headers
        h1_pattern = r'^# (.+)$'
        chapters = []

        # Find all H1 headers and their positions
        h1_matches = list(re.finditer(h1_pattern, content, re.MULTILINE))

        if not h1_matches:
            # No chapters, treat entire content as single chapter
            if content.strip():
                sections = self._parse_sections(content, 2)  # Start from H2
                chapters.append(Chapter(
                    title="Untitled",
                    content="",
                    sections=sections
                ))
            return chapters

        # Process each chapter
        for i, match in enumerate(h1_matches):
            title = match.group(1).strip()
            start = match.end()

            # Find next H1 or end of content
            if i + 1 < len(h1_matches):
                end = h1_matches[i + 1].start()
            else:
                end = len(content)

            chapter_content = content[start:end].rstrip()

            # Parse sections within this chapter
            sections = self._parse_sections(chapter_content, 2)

            # Extract direct content (before first H2)
            direct_content = ""
            if sections:
                first_h2_pos = chapter_content.find('\n##')
                if first_h2_pos == -1:
                    direct_content = chapter_content
                else:
                    direct_content = chapter_content[:first_h2_pos].strip()
            else:
                direct_content = chapter_content

            chapters.append(Chapter(
                title=title,
                content=direct_content,
                sections=sections
            ))

        return chapters

    def _parse_sections(self, content: str, min_level: int = 2) -> List[Section]:
        """
        Parse sections from content (H2 and below).

        Args:
            content: Markdown content
            min_level: Minimum header level to parse (2-6)

        Returns:
            List of Section objects
        """
        sections = []

        # Build pattern for headers from min_level to 6
        header_pattern = r'^(#{' + str(min_level) + r',6}) (.+)$'
        matches = list(re.finditer(header_pattern, content, re.MULTILINE))

        if not matches:
            return sections

        for i, match in enumerate(matches):
            hashes = match.group(1)
            level = len(hashes)
            title = match.group(2).strip()
            start = match.end()

            # Find next header or end
            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(content)

            section_content = content[start:end].rstrip()

            sections.append(Section(
                title=title,
                level=level,
                content=section_content
            ))

        return sections

    def _build_toc(self) -> List[Dict]:
        """
        Build table of contents from chapters and sections.

        Returns:
            List of TOC entries with links and hierarchy
        """
        toc = []

        for chapter in self.chapters:
            chapter_entry = {
                'title': chapter.title,
                'anchor': chapter.anchor,
                'level': 1,
                'subsections': []
            }

            for section in chapter.sections:
                section_entry = {
                    'title': section.title,
                    'anchor': section.anchor,
                    'level': section.level
                }
                chapter_entry['subsections'].append(section_entry)

            toc.append(chapter_entry)

        return toc

    @staticmethod
    def markdown_to_html(markdown_text: str) -> str:
        """
        Convert markdown to HTML.

        This is a simplified converter for common markdown elements.

        Args:
            markdown_text: Markdown text

        Returns:
            HTML string
        """
        if not markdown_text or not markdown_text.strip():
            return "<p></p>"

        lines = markdown_text.split('\n')
        html_parts = []
        in_code_block = False
        code_block_content = []
        current_paragraph = []

        for line in lines:
            # Handle code blocks
            if line.strip().startswith('```'):
                if in_code_block:
                    # End code block
                    code_html = '\n'.join(code_block_content)
                    # Escape HTML in code
                    code_html = (code_html
                                .replace('&', '&amp;')
                                .replace('<', '&lt;')
                                .replace('>', '&gt;'))
                    html_parts.append(f'<pre><code>{code_html}</code></pre>')
                    code_block_content = []
                    in_code_block = False
                else:
                    # Start code block
                    if current_paragraph:
                        paragraph_text = ' '.join(current_paragraph).strip()
                        if paragraph_text:
                            html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')
                        current_paragraph = []
                    in_code_block = True
                continue

            if in_code_block:
                code_block_content.append(line)
                continue

            # Handle blockquotes
            if line.strip().startswith('>'):
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph).strip()
                    if paragraph_text:
                        html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')
                    current_paragraph = []
                quote_text = line.lstrip('> ').strip()
                html_parts.append(f'<blockquote>{MarkdownProcessor._render_inline(quote_text)}</blockquote>')
                continue

            # Handle headers
            if line.startswith('#'):
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph).strip()
                    if paragraph_text:
                        html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')
                    current_paragraph = []

                level = len(line) - len(line.lstrip('#'))
                header_text = line.lstrip('# ').strip()
                if level <= 6:
                    html_parts.append(f'<h{level}>{MarkdownProcessor._render_inline(header_text)}</h{level}>')
                continue

            # Handle lists
            if line.strip().startswith(('- ', '* ')) or re.match(r'^\d+\.\s', line.strip()):
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph).strip()
                    if paragraph_text:
                        html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')
                    current_paragraph = []

                list_item = re.sub(r'^[-*\d.]\s+', '', line.strip())
                html_parts.append(f'<li>{MarkdownProcessor._render_inline(list_item)}</li>')
                continue

            # Handle horizontal rules
            if line.strip() in ('---', '***', '___'):
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph).strip()
                    if paragraph_text:
                        html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')
                    current_paragraph = []
                html_parts.append('<hr/>')
                continue

            # Handle empty lines (paragraph break)
            if not line.strip():
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph).strip()
                    if paragraph_text:
                        html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')
                    current_paragraph = []
                continue

            # Add to current paragraph
            current_paragraph.append(line.strip())

        # Finish any remaining paragraph
        if current_paragraph:
            paragraph_text = ' '.join(current_paragraph).strip()
            if paragraph_text:
                html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')

        html = '\n'.join(html_parts) if html_parts else '<p></p>'
        return html

    @staticmethod
    def _render_inline(text: str) -> str:
        """
        Render inline markdown elements (bold, italic, links, code).

        Args:
            text: Text with inline markdown

        Returns:
            HTML string
        """
        # Escape HTML special characters first, but be careful with our markers
        text = (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))

        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)

        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)

        # Inline code
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)

        # Links
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)

        return text

    @staticmethod
    def escape_html(text: str) -> str:
        """Escape HTML special characters."""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))
