import curses
import time
from curses import wrapper


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to Speed Typing Test!")
    stdscr.addstr("\nPress any key to Begin!")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)


def wpm_test(stdscr):
    target_text = "Hello world this is test type for beginning!"
    current_txt = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_txt) / (time_elapsed / 60)) / 5)
        stdscr.clear()
        display_text(stdscr, target_text, current_txt, wpm)
        stdscr.refresh()

        if "".join(current_txt) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue
        if key != "KEY_BACKSPACE":
            if ord(key) == 27:
                break
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_txt) > 0:
                current_txt.pop()
        elif len(current_txt) < len(target_text):
            current_txt.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    start_screen(stdscr)

    while True:
        wpm_test(stdscr)

        stdscr.addstr(2, 0, "You completed the test! Press any key to continue...")
        key = stdscr.getkey()
        if ord(key) == 27:
            break


wrapper(main)
