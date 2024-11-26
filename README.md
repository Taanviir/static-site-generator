# Static Site Generator

A Python-based **Static Site Generator** for transforming Markdown content into fully functional static websites. This tool is designed for simplicity and flexibility, allowing users to generate lightweight, fast, and customizable websites.

---

## Features

- **Markdown to HTML**: Effortlessly convert Markdown files to structured HTML pages.
- **Customizable Templates**: Use the provided `template.html` or your own custom templates to define your site's layout.
- **Static Assets Management**: Includes support for images, stylesheets, and other static files.
- **Easy Navigation**: Automatically organizes and links pages based on directory structure.
- **Modular and Extensible**: Built with reusable components for easy customization and enhancement.
- **Testing Support**: Includes unit tests for key modules to ensure reliability.

---

## File Structure

```
static-site-generator/
├── README.md          # Project documentation
├── content/           # Source Markdown files
│   ├── index.md       # Main content file
│   └── majesty/       # Subdirectory with additional content
│       └── index.md
├── src/               # Core Python source files
│   ├── main.py        # Main script for running the generator
│   ├── markdown_parser.py  # Markdown to HTML parser
│   ├── generate_page.py    # HTML page generation logic
│   ├── ...            # Additional utility modules
├── static/            # Static assets (CSS, images, etc.)
│   ├── index.css      # Stylesheet for the site
│   └── images/        # Input images
├── template.html      # HTML template for page layout
├── main.sh            # Shell script for quick execution
├── test.sh            # Shell script for running tests
├── tests/             # Unit tests for the project
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Taanviir/static-site-generator.git
   cd static-site-generator
   ```

2. Ensure you have Python 3.10 or higher installed.

---

## Usage

1. **Add Content**:
   - Write your site content in Markdown and save it in the `content/` directory as `index.md`.
   - Use subdirectories to organize your pages, for example, you can save your content in subdirectories like `content/dragons/index.md`.

2. **Customize the Template**:
   - Edit the `template.html` file to modify the site's layout.

3. **Run the Generator**:
   ```bash
   python src/main.py
   ```

4. **View Output**:
   - The generated site will be saved in the `public/` directory. Open `public/index.html` in your browser to preview.

5. **Quick Run** (optional):
   - Use the shell script for streamlined execution:
     ```bash
     ./main.sh
     ```
   - This will run `src/main.py` and set up a local server on `http://localhost:8888`.

---

## Testing

Run unit tests to ensure everything is functioning correctly:

```bash
./test.sh
```

---

## Contributing

Contributions are welcome! Here's how you can get involved:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes and push to your fork.
4. Submit a pull request with a detailed explanation.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Feedback and Support

For suggestions, issues, or feedback, please open an issue on the [GitHub repository](https://github.com/Taanviir/static-site-generator).

Happy coding! 🚀

---
