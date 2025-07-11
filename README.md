# Static Site Generator

A Python-based static site generator that converts Markdown content into styled HTML pages using customizable templates and static assets. 

## Features

- **Markdown to HTML:** Recursively scans a `content/` directory of Markdown files, converts each `.md` file to `.html`, and applies a template for consistent layout.
- **Custom Templating:** Uses `template.html` with `{{ Title }}` and `{{ Content }}` placeholders for dynamic page generation.
- **Static Assets Support:** Copies all files from a `static/` directory (like CSS, images) to the output `public/` directory.
- **Automatic Directory Management:** Deletes any existing `public/` directory before generating a new site to ensure a clean build.
- **Recursive Processing:** Handles nested directories inside `content/` for complex site structures.

## Usage

1. **Prepare your content:**
   - Place Markdown files inside the `content/` directory.
   - Add a base HTML template as `template.html` (uses `{{ Title }}` and `{{ Content }}`).
   - Place any CSS, images, or assets in the `static/` directory.

2. **Run the generator:**
   ```bash
   bash main.sh
   ```
   This will:
   - Delete the existing `public/` directory (if it exists)
   - Copy static assets to `public/`
   - Convert all Markdown files in `content/` to HTML in `public/` using the template

3. **View your site:**
   - Open any of the generated `.html` files in the `public/` directory in a browser.

## Project Structure

```
.
├── content/        # Markdown files for your site's content
├── public/         # (Generated) Output HTML and copied static assets
├── src/            # Python source code for the generator
├── static/         # Static assets (CSS, images, etc.)
├── template.html   # HTML template for all generated pages
```

## Customization

- **Template:** Adjust `template.html` to change the layout/site-wide HTML.
- **Styling:** Edit `static/index.css` (or add more CSS) for custom styles.
- **Content:** Add or organize Markdown files in `content/` as needed.

## Development

- Source code is in `src/`.
- Main entry point: `src/main.py`
- Utilities for markdown parsing and page generation are in `src/util.py`.
