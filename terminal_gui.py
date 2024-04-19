import argparse
import curses

HIGHLIGHTED_COLOR_ID = 1
TEXT_COLOR_ID = 2


def print_wrapper(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    h = h // 2
    w = w // 2

    # Init colors
    curses.init_pair(HIGHLIGHTED_COLOR_ID, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(TEXT_COLOR_ID, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Draw border
    stdscr.border()

    # Print title
    title = "Research Chain"
    title_id = 1

    stdscr.addstr(title_id, w - len(title) // 2, title)

    return h, w


def print_menu(stdscr, selected_row_idx, options):
    h, w = print_wrapper(stdscr)

    for idx, option in enumerate(options):
        x = w - len(option) // 2
        y = h - len(options) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(HIGHLIGHTED_COLOR_ID))
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.color_pair(HIGHLIGHTED_COLOR_ID))
        else:
            stdscr.attron(curses.color_pair(TEXT_COLOR_ID))
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.color_pair(TEXT_COLOR_ID))

    stdscr.refresh()


def select_input(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.keypad(True)  # Enable keypad for non-character keys

    options = ["News", "Docs", "Wiki", "Exit"]
    selected_row_idx = 0

    print_menu(stdscr, selected_row_idx, options)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected_row_idx = max(0, selected_row_idx - 1)
        elif key == curses.KEY_DOWN:
            selected_row_idx = min(len(options) - 1, selected_row_idx + 1)
        elif key in [curses.KEY_ENTER, 10, 13]:
            if selected_row_idx == len(options) - 1:
                exit()
            else:
                break

        print_menu(stdscr, selected_row_idx, options)

    return options[selected_row_idx]


def print_input_field(stdscr, text_input_value):
    stdscr.clear()
    h, w = print_wrapper(stdscr)
    # Print text input field
    stdscr.addstr(h, w - 20, "Enter Text:")
    stdscr.attron(curses.color_pair(HIGHLIGHTED_COLOR_ID))
    stdscr.addstr(h, w - 8, text_input_value)
    stdscr.attroff(curses.color_pair(HIGHLIGHTED_COLOR_ID))

    stdscr.refresh()


def user_input(stdscr):
    def get_input():
        text = ""
        print_input_field(stdscr, text)
        while True:
            char = stdscr.getch()
            if char in [curses.KEY_ENTER, 10, 13]:
                break
            elif char in [curses.KEY_BACKSPACE, 8, 127]:
                text = text[:-1]
            elif 32 <= char <= 126:
                text += chr(char)
            print_input_field(stdscr, text)
        return text

    curses.curs_set(1)  # Show cursor
    stdscr.keypad(True)  # Enable keypad for non-character keys

    text_input_value = get_input()
    curses.endwin()  # End curses window
    return text_input_value


parser = argparse.ArgumentParser()
parser.add_argument(
    "-H",
    "--use-hugging-face",
    dest="use_hugging_face",
    action="store_true",
    help="Use Hugging Face as the model provider",
)
parser.add_argument(
    "-M",
    "--pick-model",
    type=str,
    dest="model_choice",
    choices=["default", "small", "large"],
    default="default",
    help="Select model configuration",
)

args = parser.parse_args()

USE_HUGGING_FACE = args.use_hugging_face
MODEL_CHOICE = args.model_choice

"""
parser.add_argument(
    '-O',
    '--use-ollama',
    dest='use_ollama',
    action="store_true",
    help='Use Ollama as the model provider'
)
USE_OLLAMA = parser.parse_args().use_ollama
"""
