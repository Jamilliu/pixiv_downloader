# Pixiv Downloader

A user-friendly tool for downloading artwork from Pixiv using cookie-based authentication. This application provides a graphical interface for easily downloading all artworks from a specified Pixiv artist.

## Features

- Simple and intuitive graphical user interface
- Cookie-based authentication for reliable access
- Automatic download of all artworks from a specified artist
- Progress tracking with real-time status updates
- Support for resuming interrupted downloads
- Organized storage of downloaded artwork in separate folders
- Built-in verification of download completeness
- Clear logging system for monitoring download progress

## Requirements

- Python 3.10 or higher
- Required Python packages (automatically installed):
  - requests
  - tkinter (usually comes with Python)
  - PyInstaller (for building executable)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/pixiv_downloader.git
cd pixiv_downloader
```

2. You can run the application in two ways:

   a. Using the batch file (Windows):
   - Simply double-click `start_pixiv.bat`
   - The script will automatically check for Python and required dependencies

   b. Building an executable:
   - Run the build script:
   ```bash
   python build_script.py
   ```
   - Find the executable in `dist/pixiv_crawler/pixiv_crawler.exe`

## Usage

1. Launch the application using either method described above
2. Obtain your Pixiv cookie:
   - Log into Pixiv in Chrome
   - Press F12 to open Developer Tools
   - Go to the Network tab
   - Refresh the page
   - Click on any pixiv.net request
   - Find the Cookie value in the request headers
   - Copy the entire cookie string
3. Paste the cookie into the application
4. Enter the Pixiv artist ID
5. Choose a save directory (defaults to D:\dairi)
6. Click "Verify Cookie" to test your login
7. Click "Start Download" to begin downloading artworks

## Project Structure

- `pixiv_crawler_gui.py`: Main GUI application
- `pixiv_crawler.py`: Core downloading functionality
- `build_script.py`: Script for building standalone executable
- `start_pixiv.bat`: Batch file for easy launching

## Contributing

Contributions are welcome! Please feel free to submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Safety and Legal Notes

- This tool is for personal use only
- Please respect artists' rights and Pixiv's terms of service
- Keep your cookie information private and secure
- Do not distribute downloaded artworks without permission

## License

[MIT License](LICENSE) - feel free to use and modify the code, but please provide attribution.

## Acknowledgments

Thanks to all the artists sharing their work on Pixiv and making the platform what it is today.