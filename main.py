from dataclasses import dataclass
import random

import tkinter as tk
import pygame as py

WINDOW_SIZE = 500

ADJACENT_FIELDS = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                   (0, 1), (1, -1), (1, 0), (1, 1)]


def check_grid(y_axis, x_axis, grid_size):
    """Sprawdzanie grid'a"""
    return -1 < y_axis < grid_size and -1 < x_axis < grid_size


@dataclass
class Cell:
    """obiekty komorki"""
    cell_row: int
    cell_column: int
    cell_mine: bool = False
    cell_uncovered_mine: bool = False
    cell_marked: bool = False
    cell_question: bool = False
    cell_mine_count_neighbourhood: int = 0
    cheat_mine: bool = False

    def set_mine(self):
        self.cell_mine = True

    def show(self, distance, screen, cell_normal, cell_marked, cell_question, cell_mine, cheat_mine, uncovered):
        """pokazywanie obiektow na planszy"""
        pos = (self.cell_column * distance, self.cell_row * distance)
        if self.cell_uncovered_mine:
            if self.cell_mine:
                screen.blit(cell_mine, pos)
            else:
                screen.blit(uncovered[self.cell_mine_count_neighbourhood], pos)
        else:
            if self.cell_marked:
                screen.blit(cell_question, pos)
            elif self.cell_question:
                screen.blit(cell_marked, pos)
            else:
                screen.blit(cell_normal, pos)
        if self.cheat_mine:
            screen.blit(cheat_mine, pos)
            if self.cell_marked:
                screen.blit(cell_question, pos)
            elif self.cell_question:
                screen.blit(cell_marked, pos)
            else:
                screen.blit(cheat_mine, pos)


    def find_mines(self, grid_size, matrix):
        """szukanie min"""
        for pos in ADJACENT_FIELDS:
            new_line, new_column = self.cell_row + pos[0], self.cell_column + pos[1]
            if check_grid(new_line, new_column, grid_size) \
                    and matrix[new_line * grid_size + new_column].cell_mine:
                self.cell_mine_count_neighbourhood += 1


class Assets:
    """Zasoby potrzebne do gry."""

    @staticmethod
    def loadfile(filename, distance):
        """wczytywanie plikow z folderu Cells"""
        return py.transform.scale(py.image.load(filename), (distance, distance))


class Colors:
    """Paleta barw"""
    WHITE = (255, 255, 255)
    GREEN = (0, 128, 0)


def init_matrix(grid_size):
    matrix = []
    for cell_in_grid in range(grid_size * grid_size):
        matrix.append(Cell(cell_in_grid // grid_size, cell_in_grid % grid_size))
    return matrix


def fill_func(row, col, grid_size, matrix):
    """wypelnianie odpowienidmi gifami"""
    for pos in ADJACENT_FIELDS:
        new_line = row + pos[0]
        new_column = col + pos[1]
        if check_grid(new_line, new_column, grid_size):
            celle = matrix[new_line * grid_size + new_column]
            if celle.cell_mine_count_neighbourhood == 0 and not celle.cell_uncovered_mine:
                celle.cell_uncovered_mine = True
                fill_func(new_line, new_column, grid_size, matrix)
            else:
                celle.cell_uncovered_mine = True


def first_click(selected_cell, mines_left, grid_size, matrix):
    """pierwsze klikniecie"""
    selected_cell.cell_uncovered_mine = True
    while mines_left > 0:
        cell = matrix[random.randrange(grid_size * grid_size)]
        if not cell.cell_mine and cell != selected_cell:
            cell.cell_mine = True
            mines_left -= 1
    for object_in_matrix in matrix:
        if not object_in_matrix.cell_mine:
            object_in_matrix.find_mines(grid_size, matrix)


def end_screen(win_or_loose, screen):
    """ekran koncowy"""
    font = py.font.SysFont("comicsansms", 50)
    if win_or_loose:
        text = font.render("Wygrana!", True, Colors.GREEN)
    else:
        text = font.render("Przegrana!", True, Colors.GREEN)

    screen.fill(Colors.WHITE)
    screen.blit(text,
                (250 - text.get_width() // 2, 240 - text.get_height() // 2))

    py.display.flip()


def main_sweeper(distance, grid_size, total_mine_count, window):
    """funkcja uruchamiajaca gre"""
    py.init()
    matrix = []
    uncovered = []
    mines_left = total_mine_count
    flags_on_mines = 0
    flags_on_blanks = 0
    screen = py.display.set_mode([WINDOW_SIZE, WINDOW_SIZE])
    py.display.set_caption('Saper, Created by Szymon Żylski')

    cell_normal = Assets.loadfile('./Cells/cellnormal.gif', distance)
    cell_marked = Assets.loadfile('./Cells/cellmarked.gif', distance)
    cell_question = Assets.loadfile('./Cells/cellquestion.gif', distance)
    cell_mine = Assets.loadfile('./Cells/cellmine.gif', distance)
    cheat_mine = Assets.loadfile('./Cells/cell_cheat.gif', distance)

    cheat_input = ''
    cheat_thing = 'xyzzy'
    for cell_in_grid in range(9):
        uncovered.append(Assets.loadfile(f'./Cells/cell{cell_in_grid}.gif', distance))

    matrix = init_matrix(grid_size)

    first_click_todo = True
    ongoing = True
    while ongoing:
        for event in py.event.get():
            if event.type == py.QUIT:
                ongoing = False
            if event.type == py.MOUSEBUTTONDOWN or event.type == py.KEYDOWN:
                mouse_x, mouse_y = py.mouse.get_pos()
                cell = matrix[mouse_y // distance * grid_size + mouse_x // distance]
                if first_click_todo:
                    first_click(cell, mines_left, grid_size, matrix)
                if not first_click_todo:
                    if py.mouse.get_pressed()[2]:
                        cell.cell_marked = not cell.cell_marked
                        if cell.cell_marked:
                            cell.cell_question = not cell.cell_question
                        if cell.cell_question:
                            cell.cell_marked = not cell.cell_marked
                        if not cell.cell_marked and not cell.cell_mine:
                            flags_on_blanks += 1
                        if not cell.cell_question and not cell.cell_mine:
                            flags_on_blanks -= 1
                        if cell.cell_mine and cell.cell_question:
                            flags_on_mines += 1
                        if flags_on_mines >= total_mine_count and flags_on_blanks == 0:
                            for obj in matrix:
                                obj.cell_uncovered_mine = True
                            end_screen(True, screen)
                            ongoing = False
                            py.time.wait(3000)

                    if py.mouse.get_pressed()[0]:
                        cell.cell_uncovered_mine = True
                        if cell.cell_mine_count_neighbourhood == 0 and not cell.cell_mine:
                            fill_func(mouse_y // distance, mouse_x // distance, grid_size, matrix)
                        if cell.cell_mine:
                            for obj in matrix:
                                obj.cell_uncovered_mine = True
                            end_screen(False, screen)
                            ongoing = False
                            py.time.wait(3000)
                if event.type == py.KEYDOWN and not first_click_todo:
                    cheat_input += event.unicode
                    if event.key == py.K_BACKSPACE:
                        cheat_input = ''
                    if cheat_input == cheat_thing:
                        for obj in matrix:
                            if obj.cell_mine:
                                obj.cheat_mine = True
                first_click_todo = False

        for obj in matrix:
            obj.show(distance, screen, cell_normal, cell_marked, cell_question, cell_mine, cheat_mine, uncovered)

        py.display.flip()

    py.time.wait(5000)
    py.display.quit()
    window.destroy()


def main():
    """inicjalizacja gui"""
    window = tk.Tk()
    window.title("Wybierz plansze")
    window.resizable(False, False)
    window.geometry("250x100")

    mines_count = tk.IntVar()
    grid_size = tk.IntVar()

    mine_label = tk.Label(window, text="Ilosc bomb: ")
    mine_label.grid(row=0, column=0)

    mine_entry = tk.Entry(window, textvariable=mines_count)
    mine_entry.grid(row=0, column=1)

    grid_label = tk.Label(window, text="Wielkosc okna: ")
    grid_label.grid(row=1, column=0)

    grid_entry = tk.Entry(window, textvariable=grid_size)
    grid_entry.grid(row=1, column=1)

    grid_entry.insert(0, "1")
    mine_entry.insert(0, "1")

    def update():
        """aktualizacja vars"""
        get_grid = grid_size.get()
        get_mine_count = mines_count.get()
        distance = WINDOW_SIZE // get_grid
        if get_grid > 30 or get_mine_count > get_grid * get_grid - 1:
            print("podaj mniejsza liczbe niz \n okno < 30, bomby musza byc mniejsze niz < okno * okno -1")
        else:
            main_sweeper(distance, get_grid, get_mine_count, window)

    button_calc = tk.Button(window, text="zatwierdz", command=update)
    button_calc.grid(row=3, column=0)
    window.mainloop()


if __name__ == '__main__':
    main()
