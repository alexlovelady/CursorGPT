import pyautogui
import pytesseract
from tkinter import Tk, Toplevel, Canvas, Label
import openai
import keyboard

# 1. Set your OpenAI API key
openai.api_key = "YOUR-OPENAI-API-KEY"

# If Tesseract is not on PATH, specify the location:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def select_capture_area():
    """
    Open a full-screen transparent window and let the user click and drag
    to select an area. Returns (left, top, width, height) of the selection (all ints).
    """
    root = Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.3)
    root.config(cursor="cross")

    canvas = Canvas(root, bg="grey")
    canvas.pack(fill="both", expand=True)

    start_x, start_y = None, None
    rect_id = None

    def on_mouse_down(event):
        nonlocal start_x, start_y, rect_id
        start_x, start_y = event.x, event.y
        # Draw a new rectangle; store its ID
        rect_id = canvas.create_rectangle(
            start_x, start_y, start_x, start_y,
            outline="red", width=2
        )

    def on_mouse_move(event):
        # Update rectangle coords to current mouse position
        if rect_id is not None:
            canvas.coords(rect_id, start_x, start_y, event.x, event.y)

    def on_mouse_up(event):
        # Once mouse is released, close the window
        root.quit()

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_move)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()

    if rect_id:
        # Get the float coords
        x1, y1, x2, y2 = canvas.coords(rect_id)
        root.destroy()

        # Convert floats to ints
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        # Calculate left, top, width, height
        left, top = min(x1, x2), min(y1, y2)
        width, height = abs(x2 - x1), abs(y2 - y1)
        
        return (left, top, width, height)
    else:
        root.destroy()
        return (0, 0, 0, 0)  # if no region was drawn

def capture_text_custom():
    """
    Let user interactively drag-select a region, then do OCR on it.
    """
    left, top, width, height = select_capture_area()
    if width <= 0 or height <= 0:
        return ""  # no valid region

    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    text = pytesseract.image_to_string(screenshot)
    return text

def ask_chatgpt(question_text):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant who provides short, concise answers."
                    " Do not elaborate."
                )
            },
            {
                "role": "user",
                "content": f"Answer this question. Just provide the answer, do not regive me the question. The answers are the bulleted words:\n{question_text}"
            }
        ],
        max_tokens=999,
        temperature=0.5
    )
    answer = response.choices[0].message.content.strip()
    return answer

def show_tooltip(text, duration=5):
    root = Tk()
    root.withdraw()

    top = Toplevel(root)
    top.overrideredirect(True)
    top.lift()
    top.wm_attributes("-topmost", True)

    x, y = pyautogui.position()
    top.geometry(f"+{x+10}+{y+10}")

    label = Label(top, text=text, bg="lightyellow", fg="black", padx=10, pady=5)
    label.pack()

    def close_tooltip():
        root.destroy()

    root.after(duration * 1000, close_tooltip)
    root.mainloop()

def main():
    print("Click and drag on the screen to select an area for OCR.")
    text = capture_text_custom()
    print("Extracted text:")
    print(text)

    if not text.strip():
        print("No text detected or no region selected.")
        return

    answer = ask_chatgpt(text)
    print("ChatGPT answer:", answer)
    show_tooltip(answer, duration=10)

if __name__ == "__main__":
    print("Press Ctrl+Shift+Q to run the script.")
    keyboard.add_hotkey('ctrl+shift+q', main)
    keyboard.wait()
