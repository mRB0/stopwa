#!/usr/bin/env python3

import curses
from time import perf_counter, sleep

def main(stdscr):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.timeout(1000 // 30) # 1000 millis / 30 fps
    stdscr.clear()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    stop = False
    run = True

    start_time = perf_counter()
    paused_elapsed = 0
    
    while not stop:
        h, w = stdscr.getmaxyx()

        if run:
            now = perf_counter()
            elapsed = (now - start_time)
            color_pair = 1
        else:
            elapsed = paused_elapsed
            color_pair = 2

        display = '{:02d}h {:02d}m {:02d}s {:02d}'.format(int(elapsed) // 3600,
                                                          (int(elapsed) % 3600) // 60,
                                                          (int(elapsed) % 60),
                                                          int((elapsed * 100) % 100))

        stdscr.addstr(h // 2,
                      (w - len(display)) // 2,
                      display,
                      curses.color_pair(color_pair) | curses.A_BOLD)
        stdscr.refresh()
        
        ch = stdscr.getch() # delays by timeout waiting for input
        
        if ch != -1:
            if ch == curses.KEY_RESIZE:
                stdscr.clear()
                
            if ch == ord('q'):
                break

            if ch == ord(' '):
                # pause/resume
                run = not run
                if run:
                    start_time = perf_counter() - paused_elapsed
                else:
                    paused_elapsed = perf_counter() - start_time
            

curses.wrapper(main)
