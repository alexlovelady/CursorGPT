# Screen OCR & GPT Assistant

A Python script that lets you select an area on your screen, perform OCR using [Tesseract](https://github.com/tesseract-ocr/tesseract), and get a concise answer from GPT. Perfect for quick lookups, code explanations, or translations.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

## Features
- **Interactive Screen Capture**: Drag-select any region on your screen for OCR.
- **Tesseract OCR Integration**: Converts screenshots to text seamlessly.
- **GPT-4 Powered**: Gets concise answers from the extracted text.
- **Tooltip Display**: Shows the GPT response in a floating window near your mouse cursor.

## Requirements
- Python 3.7 or higher
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and on your PATH  
  Or specify `pytesseract.pytesseract.tesseract_cmd` in the script
- [PyAutoGUI](https://pyautogui.readthedocs.io)
- [Pillow](https://pillow.readthedocs.io) (often installed with PyAutoGUI)
- [pytesseract](https://pypi.org/project/pytesseract/)
- [openai](https://pypi.org/project/openai/)
- [keyboard](https://pypi.org/project/keyboard/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (usually included with Python on most systems)

## Installation
1. Clone this repository:
   ```bash
     git clone https://github.com/yourusername/screen-ocr-gpt.git
     cd screen-ocr-gpt
   ```
   
2. Install Python dependencies:

  ```bash
    pip install -r requirements.txt
    Or manually install:
  ```
  
  ```bash
    pip install pyautogui pytesseract openai keyboard
  ```

Make sure Tesseract OCR is installed:
On Windows, download the installer here.
On macOS, brew install tesseract.
On Linux, sudo apt-get install tesseract-ocr.
Verify pytesseract can find the Tesseract executable:

If necessary, set pytesseract.pytesseract.tesseract_cmd to your Tesseract path in the script.


Usage
Set your OpenAI API key in the script:

  ```python
    openai.api_key = "YOUR-OPENAI-API-KEY"
  ```

Run the script:

  ```bash
    python screen_ocr_gpt.py
  ```

Trigger the capture:

Press Ctrl+Shift+Q to open the drag-select overlay.
Drag a box around the text you want to capture and release.
The script performs OCR, sends the text to GPT, and displays the answer in a small tooltip near your mouse.
Close the tooltip or wait for it to disappear automatically.

Configuration
Change the tooltip duration by adjusting show_tooltip(answer, duration=10).
Modify the system prompt (in ask_chatgpt) if you want more verbose or different styles of answers.
