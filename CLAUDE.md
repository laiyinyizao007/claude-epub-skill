# Markdown to EPUB Skill - Development Guide

## Project Overview

A Claude agent skill that converts markdown documents into professional EPUB3 ebook files. This is a custom skill implementation demonstrating how to build Claude Code skills with file generation capabilities.

## Quick Start

### Setup
```bash
# Install dependencies
pip install -r markdown-to-epub/requirements.txt

# Test the skill
python test_epub_skill.py
```

### Usage
```python
from markdown_to_epub.scripts.epub_generator import create_epub_from_markdown

create_epub_from_markdown(
    markdown_content,
    output_path="output.epub",
    title="My Book",
    author="Author Name"
)
```

## Project Structure

```
markdown-to-epub/
├── SKILL.md                    # Skill definition with YAML frontmatter
├── requirements.txt            # Python dependencies (ebooklib, markdown2)
├── scripts/
│   ├── markdown_processor.py  # Markdown parsing & structure extraction
│   └── epub_generator.py      # EPUB file creation & formatting
test_epub_skill.py             # Test suite
```

## Claude Skills Development Guidelines

### Skill Definition (SKILL.md)
- Must include YAML frontmatter with `name` and `description`
- Description should be clear and actionable for Claude to understand when to use the skill
- Include detailed usage examples showing input formats and expected outputs
- Document all supported features and edge cases

### Python Implementation
- Keep dependencies minimal and well-documented in `requirements.txt`
- Separate concerns: parsing logic vs. file generation
- Handle edge cases gracefully (empty input, malformed markdown, etc.)
- Include comprehensive error handling and validation

### Testing
- Create standalone test file that validates all major functionality
- Test edge cases: empty content, special characters, long documents
- Verify output file quality and standards compliance
- Make tests runnable without external dependencies

## Development Best Practices

### Code Organization
- **Processing Scripts**: Put core logic in `scripts/` directory
- **Configuration**: Use YAML frontmatter in SKILL.md for metadata
- **Resources**: Keep static assets (CSS, templates) in `resources/` (if needed)
- **Tests**: Standalone test files at project root

### File Generation
- Always validate output file format compliance
- Use well-established libraries (e.g., ebooklib for EPUB)
- Include proper metadata (title, author, language, date)
- Test generated files in target applications (e.g., Apple Books, Kindle)

### Documentation
- README.md: User-facing documentation with examples
- SKILL.md: Claude-readable skill definition and usage
- REFERENCE.md: Technical implementation details (optional)
- CLAUDE.md: Development guidelines (this file)

## Common Development Tasks

### Adding New Markdown Features
1. Update `markdown_processor.py` to parse the new element
2. Update CSS in `epub_generator.py` to style it properly
3. Add test cases in `test_epub_skill.py`
4. Update documentation in README.md and SKILL.md

### Improving EPUB Styling
1. Modify CSS in `create_styled_chapter()` function
2. Test in multiple EPUB readers (Apple Books, Calibre, etc.)
3. Ensure responsive design for different screen sizes
4. Validate EPUB3 compliance

### Testing Changes
```bash
# Run test suite
python test_epub_skill.py

# Test generated EPUB manually
python -c "
from markdown_to_epub.scripts.epub_generator import create_epub_from_markdown
create_epub_from_markdown('# Test\n\nContent', 'test.epub', 'Test', 'Author')
"
open test.epub  # macOS - opens in default EPUB reader
```

## Publishing the Skill

See `publish.sh` for publishing workflow.

## Resources

- **Skills Documentation**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- **EPUB 3 Standard**: https://www.w3.org/publishing/epub32/
- **ebooklib Documentation**: https://docs.sourcefabric.org/projects/ebooklib/
