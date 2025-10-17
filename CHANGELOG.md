# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-10-17

### Added
- Initial release of Markdown to EPUB Claude skill
- Markdown parsing with support for headers, paragraphs, lists, code blocks, and tables
- EPUB3 file generation with professional styling
- Automatic table of contents generation from markdown headers
- Support for inline formatting (bold, italic, code)
- Syntax highlighting for code blocks
- Responsive table styling for EPUB readers
- Comprehensive test suite
- Documentation and usage examples

### Technical Details
- Built with Python 3.9+
- Uses `ebooklib` for EPUB generation
- Uses `markdown2` for markdown parsing
- Follows EPUB 3.0 specification
- Compatible with major EPUB readers (Apple Books, Calibre, etc.)

[Unreleased]: https://github.com/smerchek/claude-epub-skill/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/smerchek/claude-epub-skill/releases/tag/v1.0.0
