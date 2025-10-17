---
name: markdown-to-epub-converter
description: Convert markdown documents and chat summaries into formatted EPUB ebook files that can be read on any device or uploaded to Kindle.
---

# Markdown to EPUB Converter Skill

This skill transforms markdown documents into professional EPUB ebook files. Perfect for converting research documents, blog posts, articles, or chat conversation summaries into portable, device-agnostic ebook formats.

## Overview

The skill accepts markdown content in multiple formats and generates a properly formatted EPUB3 file that works across all major ebook readers including:
- Apple Books
- Amazon Kindle (via Kindle for Mac/Windows/iOS/Android)
- Google Play Books
- Kobo and other EPUB readers
- Any standard EPUB reader

## Input Formats

### Option 1: Raw Markdown Text
Provide markdown content directly in your message:

```
Convert this markdown to EPUB:
# My Book Title
## Chapter 1
This is chapter one content...
```

### Option 2: File Path
Provide a path to a markdown file to be converted.

## How It Works

1. **Markdown Parsing**: Analyzes your markdown and automatically:
   - Treats H1 headers (`#`) as chapter boundaries
   - Treats H2 headers (`##`) as section headings within chapters
   - Preserves formatting (bold, italic, links, lists, code blocks)

2. **Structure Generation**: Creates proper EPUB structure:
   - Automatic table of contents from chapters
   - Navigation document (EPUB3 standard)
   - Metadata (title, language, etc.)

3. **File Creation**: Generates a valid EPUB3 file ready for download and use

## Usage Examples

### Example 1: Convert a Blog Post
"Convert this markdown blog post to EPUB:
# How to Build a Simple Web Server
## Introduction
...content..."

### Example 2: Convert a Research Summary
"I have research notes in markdown format. Convert them to an EPUB ebook. The content is:
# Research Project: Machine Learning Basics
## Chapter 1: Fundamentals
..."

### Example 3: Convert a Chat Summary
"Summarize our conversation so far as markdown and convert it to an EPUB for reference"

## Output

The skill generates a downloadable EPUB file that includes:
- Professional formatting
- Automatic table of contents
- Proper chapter structure
- Support for markdown formatting elements:
  - Headers (all levels)
  - Bold and italic text
  - Hyperlinks
  - Lists (ordered and unordered)
  - Code blocks and inline code
  - Blockquotes
  - Horizontal rules

## Markdown Elements Supported

| Element | Markdown | Support |
|---------|----------|---------|
| Headers | `# H1` through `###### H6` | Full |
| Bold | `**text**` or `__text__` | Full |
| Italic | `*text*` or `_text_` | Full |
| Links | `[text](url)` | Full |
| Lists | `- item` or `1. item` | Full |
| Code | ` `code` ` or code blocks | Full |
| Tables | Markdown tables | Full |
| Blockquotes | `> quote` | Full |
| Horizontal rule | `---` or `***` | Full |

## Advanced Features

### Custom Title and Metadata
You can specify EPUB metadata:
- Book title (defaults to first H1 header)
- Author name
- Language
- Publication date

### Chapter Organization
Chapters are automatically detected from:
- H1 headers (`#`) as primary chapter breaks
- Logical content sections between H1s
- Automatic page breaks between chapters

### Styling
The generated EPUB uses clean, readable default styling that:
- Respects the reader's font preferences
- Works on all screen sizes
- Maintains proper spacing and hierarchy
- Includes appropriate margins and padding

## Technical Details

- **Format**: EPUB3 (compatible with all modern readers)
- **Encoding**: UTF-8
- **HTML Version**: XHTML 1.1
- **CSS Support**: Responsive styling

## Downloading Your EPUB

After generation, the file will be available for download. You can then:
1. Download the EPUB to your computer
2. Open it with your preferred ebook reader
3. Transfer to your Kindle, iPad, or other device
4. Upload directly to Kindle via email or cloud

## Tips for Best Results

1. **Use Proper Markdown Structure**: The skill works best when markdown follows standard conventions (H1 for titles, H2 for sections)

2. **Clear Chapter Breaks**: Use H1 headers to clearly mark chapter divisions

3. **Descriptive Headers**: Headers become the table of contents, so make them clear and descriptive

4. **Content Organization**: Place content logically between headers

5. **Supported Formatting**: Stick to basic markdown formatting for best compatibility across all readers

## Troubleshooting

**EPUB doesn't open**: Ensure your markdown is properly formatted. Check for matching brackets in links and proper syntax.

**Table of contents is empty**: Make sure your markdown includes H1 headers to define chapters.

**Formatting looks different**: EPUB readers apply their own fonts and styling. This is normal and expected behavior.

## Scripts

- `epub_generator.py` - Core EPUB file creation and formatting
- `markdown_processor.py` - Markdown parsing and structure extraction

## Future Enhancements

- Auto-generated cover pages with custom images
- Kindle-specific optimizations (.mobi format)
- Custom CSS styling per user preferences
- Multi-document merging
- Image embedding and optimization
- Advanced metadata support
