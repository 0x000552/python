"""
Logic task to find mouse in holes.
Console version.

Written by 0x000552 23.12.18
"""





class CatAndMouse:
    rbt = "\033[91;5m"  # red blink
    clt = "\033[0m"  # reset text decoration

    CAT = "C"
    MOUSE = "M"
    BLANK = "O"

    def __init__(self, holes_count, algorithm):
        self._holes_count = holes_count
        self._holes = [self.BLANK for _ in range(holes_count)]
        self._algorithm = [int(n) for n in algorithm]
        self._mouses = [i for i in self._holes if i != self._algorithm[0]] # mouse can be everywhere,
                                                                          # but not in first cat step
        # self.any_mouse_alive = True

    def start(self):
        self._main()


    def _main(self):
        while self._check_mouses_alive():
            self._update_field_graphic()


    def _check_mouses_alive(self):
        for mouse in self._mouses:
            if mouse != -1:
                return True
        return False

    def _update_field_graphic(self, killed_mouses=[]):
        for hole in self._holes:
            print(f"{hole}  ", end='')

        for killed_mouse in killed_mouses:
            print(";  {rbt}mouse {killed_mouse} has been killed!{clt}")

        print("\n\n\n")

    def _mouse_change_pos(self):
        pass






def main():
    pass



if __name__ == "__main__":
    main()
