import curses

def print_menu(stdscr, selected_row_idx, options):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Draw border
    stdscr.border()

    # Print title
    title = "Research Chain"
    stdscr.addstr(1, w // 2 - len(title) // 2, title)

    for idx, option in enumerate(options):
        x = w//2 - len(option)//2
        y = h//2 - len(options)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.color_pair(2))

    stdscr.refresh()

def select_input(stdscr):
    curses.curs_set(0)  # Hide cursor
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
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
    h, w = stdscr.getmaxyx()

    # Draw border
    stdscr.border()

    # Print title
    title = "Research Chain"
    stdscr.addstr(1, w // 2 - len(title) // 2, title)

    # Print text input field
    stdscr.addstr(h // 2, w // 2 - 20, "Enter Text:")
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(h // 2, w // 2 - 8, text_input_value)
    stdscr.attroff(curses.color_pair(1))


    stdscr.refresh()

def text_input(stdscr):
    def get_input():
        text = ""
        print_input_field(stdscr, text)
        while True:
            char = stdscr.getch()
            if char in [curses.KEY_ENTER, 10, 13]:
                break
            elif char in [curses.KEY_BACKSPACE, 127]:
                text = text[:-1]
            elif 32 <= char <= 126:
                text += chr(char)
            print_input_field(stdscr, text)
        return text

    curses.curs_set(2)  # Show cursor
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    stdscr.keypad(True)  # Enable keypad for non-character keys

    text_input_value = get_input()
    curses.endwin()  # End curses window
    return text_input_value