import curses
import queue
import time
from curses import wrapper
from typing import List, Optional, Tuple


class PathFinder:
    def __init__(self, maze: List[List[str]]) -> None:
        self.maze: List[List[str]] = maze
        self.start_symbol: str = "O"
        self.end_symbol: str = "X"
        self.path_symbol: str = "X"
        self.wall_symbol: str = "#"
        self.space_symbol: str = " "

    def find_start(self) -> Optional[Tuple[int, int]]:
        for i, row in enumerate(self.maze):
            for j, value in enumerate(row):
                if value == self.start_symbol:
                    return i, j
        return None

    def find_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        neighbors: List[Tuple[int, int]] = []
        directions: List[Tuple[int, int]] = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]  # UP, DOWN, LEFT, RIGHT

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < len(self.maze) and 0 <= c < len(self.maze[0]):
                if self.maze[r][c] != self.wall_symbol:  # Avoid walls
                    neighbors.append((r, c))

        return neighbors

    def find_path(
        self, stdscr: curses.window, delay: float = 0.1
    ) -> Optional[List[Tuple[int, int]]]:
        start_pos: Optional[Tuple[int, int]] = self.find_start()
        if not start_pos:
            raise ValueError("Start position not found in the maze.")

        q: queue.Queue[Tuple[Tuple[int, int], List[Tuple[int, int]]]] = queue.Queue()
        q.put((start_pos, [start_pos]))  # (current_position, path_taken)
        visited: set = set()

        while not q.empty():
            current_pos, path = q.get()
            row, col = current_pos

            stdscr.clear()
            self.print_maze(stdscr, path)
            time.sleep(delay)
            stdscr.refresh()

            if self.maze[row][col] == self.end_symbol:  # Reached the goal
                self.visualize_final_path(stdscr, path)
                return path

            for neighbor in self.find_neighbors(row, col):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    q.put((neighbor, new_path))
                    visited.add(neighbor)

        return None  # No path found

    def visualize_final_path(
        self, stdscr: curses.window, path: List[Tuple[int, int]], delay: float = 0.05
    ) -> None:
        for pos in path:
            stdscr.clear()
            self.print_maze(stdscr, path, highlight=True)
            time.sleep(delay)
            stdscr.refresh()

    def print_maze(
        self,
        stdscr: curses.window,
        path: List[Tuple[int, int]] = [],
        highlight: bool = False,
    ) -> None:
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Walls
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Current Path
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Final Path

        for i, row in enumerate(self.maze):
            for j, value in enumerate(row):
                if (i, j) in path:
                    color = curses.color_pair(3) if highlight else curses.color_pair(2)
                    stdscr.addstr(i, j * 2, self.path_symbol, color)
                else:
                    color = (
                        curses.color_pair(1)
                        if value == self.wall_symbol
                        else curses.color_pair(0)
                    )
                    stdscr.addstr(i, j * 2, value, color)


def main(stdscr: curses.window) -> None:
    maze: List[List[str]] = [
        ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
        ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
        ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
        ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
        ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "X", "#"],
    ]

    pathfinder = PathFinder(maze)
    pathfinder.find_path(stdscr, delay=0.15)
    stdscr.getch()


if __name__ == "__main__":
    wrapper(main)
