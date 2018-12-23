"""
Logic task to find mouse in holes.
Console version.

Written by 0x000552 23.12.18
"""

from collections import deque




class CatAndMouse:
    rbt = "\033[91;5m"  # red blink
    clt = "\033[0m"  # reset text decoration
    len_rbt_clt = len(rbt) + len(clt)

    CAT = f"C"
    MOUSE = "M"
    # BLANK = "O"


    def __init__(self, holes_count, algorithm):
        """
        :param holes_count: must be int and > 0
        :param algorithm: expect string ("2344" Cat will try 2,3,4,4 holes.)
        """
        if isinstance(holes_count, int) and holes_count > 0:
            self._holes_count = holes_count
        else:
            print(f"Incorrect param: holes_count = {holes_count}, holes_count = 4 will be used instead")

        # mouse can be everywhere, but not in the hole what cat will choose at the first step
        self._holes = [[f"{self.MOUSE}.{i}"] if i != int(algorithm[0])-1 else [] for i in range(holes_count)]
        self._algorithm = deque(map(int, algorithm))

        self._WOMS = len(self._algorithm) * 2 + len(self.MOUSE)  # maximum width of mouse string

    def start(self):
        self._main()

    def _main(self):

        any_alive_mouse = True
        caught_mouses = []
        moved_mouses = []
        cat_cur_hole = 0

        while any_alive_mouse and len(self._algorithm) > 0:
            print("Before Attack:   ", end='')
            self._update_field_graphic(caught_mouses)

            # Here we will caught mouse(s)
            caught_mouses.clear()
            cat_cur_hole = self._algorithm.popleft() - 1
            if len(self._holes[cat_cur_hole]) > 0:  # if not blank, only mouse(s) can be here
                caught_mouses = self._holes[cat_cur_hole].copy()
                # self._holes[cat_cur_hole].clear()
            self._holes[cat_cur_hole].append(self.CAT)  # insert cat's paw

            print("       Attack:   ", end='')
            self._update_field_graphic(caught_mouses)
            print("\n")

            # self._holes[cat_cur_hole].remove(self.CAT)  # remove cat's paw
            self._holes[cat_cur_hole].clear()

            # Here we will move alive mouse(s)
            any_alive_mouse = False
            for i, hole in enumerate(self._holes):
                if len(hole) > 0:  # only mouse can be in the hole now
                    any_alive_mouse = True  # TODO should I check it before assign?
                    for mouse in hole:
                        if mouse in moved_mouses:
                            continue
                        if i-1 >= 0:
                            mm = f"{mouse}.{i-1}"
                            self._holes[i-1].append(mm)
                            moved_mouses.append(mm)
                        if i+1 < self._holes_count:
                            mm = f"{mouse}.{i+1}"
                            self._holes[i+1].append(mm)
                            moved_mouses.append(mm)
                        hole.remove(mouse)
            moved_mouses.clear()

        print("\n\n       Result:   ", end='')
        self._update_field_graphic()
        if any_alive_mouse:
            print("Algorithm FAILED!")
        else:
            print("All mouse caughted")

    def _update_field_graphic(self, caught_mouses=[]):
        # mmih =  max(map(max, self._holes)) * self.WOMS  # maximum mouses in hole  # TODO should find maximum possible...
        mmih = 16
        for hole in self._holes:
            moc = []
            for mouse_or_cat in hole:
                moc.append(f"{mouse_or_cat} ")
            moc = "".join(moc)
            if self.CAT in moc:
                print(f"| {self.rbt}{moc:^{mmih}}{self.clt} |   ", end='')
            else:
                print(f"| {moc:^{mmih}} |   ", end='')

        # for caught_mouse in caught_mouses:
        #     print(f";  {self.rbt}mouse {caught_mouse} has been caught!{self.clt}", end='')

        print("\n\n\n")

    def _mouse_change_pos(self):
        pass


def main():
    al = input("Algorithm ('2344' Cat will try 2,3,4,4 holes.): ")
    CatAndMouse(4, al).start()


if __name__ == "__main__":
    main()
