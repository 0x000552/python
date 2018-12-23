"""
Logic task to find mouse in holes.
Console version.

Written by 0x000552 23.12.18
"""

from collections import deque
import sys



class CatAndMouse:
    rbt = "\033[91;5m"  # red blink
    rt = "\033[91m"  # red
    gt = "\033[32m"  # green
    clt = "\033[0m"  # reset text decoration

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

        if len(algorithm) < 1:
            print("Algorithm len should be > 1")
            raise ValueError

        # mouse can be everywhere, but not in the hole what cat will choose at the first step
        self._holes = [[f"{self.MOUSE}.{i}"] if i != int(algorithm[0])-1 else [] for i in range(holes_count)]

        self._algorithm = deque(map(int, algorithm))

        # self._WOMS = len(self._algorithm) * 2 + len(self.MOUSE)  # maximum width of mouse string

    def start(self):
        self._main()

    def _main(self):
        """
        All magic is here :D
        :return:
        """

        any_alive_mouse = True
        caught_mouses = []
        moved_mouses = []

        while any_alive_mouse and len(self._algorithm) > 0:
            print("Before Attack:   ", end='')
            self._update_holes_graphic()

            # Here we will caught mouse(s)
            caught_mouses.clear()
            cat_cur_hole = self._algorithm.popleft() - 1
            if len(self._holes[cat_cur_hole]) > 0:  # if not blank, only mouse(s) can be here
                caught_mouses = self._holes[cat_cur_hole].copy()
            self._holes[cat_cur_hole].append(self.CAT)  # insert cat's paw

            print("       Attack:   ", end='')
            self._update_holes_graphic()
            print("\n")

            self._holes[cat_cur_hole].clear() # remove cat's paw

            # Here we will move alive mouse(s)
            any_alive_mouse = False
            for i, hole in enumerate(self._holes):
                if len(hole) > 0:  # only (alive) mouse(s) can be in the hole now
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

        print("\n")
        if any_alive_mouse:
            print(f"{self.rt}Algorithm FAILED!{self.clt}")
        else:
            print(f"{self.gt}All mouses was caught{self.clt}", end='')
            if len(self._algorithm) > 0:
                print(f"{self.rt}, but end of algorithm not reached{self.clt}")
            else:
                print("")
        print("\n       Result:   ", end='')
        self._update_holes_graphic()


    def _update_holes_graphic(self):
        """
        Console version
        :return:
        """
        # mmih =  max(map(max, self._holes)) * self.WOMS  # maximum mouses in hole  # TODO should find maximum possible...
        mmih = 30
        for hole in self._holes:
            moc = []
            for mouse_or_cat in hole:
                moc.append(f"{mouse_or_cat} ")
            moc = "".join(moc)
            if self.CAT in moc:
                # Mouse(s) was caught in the hole where cat's paw exists
                print(f"| {self.rbt}{moc:^{mmih}}{self.clt} |   ", end='')
            else:
                print(f"| {moc:^{mmih}} |   ", end='')

        print("\n\n\n")


def main():
    print("\n\n\nAlgorithm (ex. '2344' Cat will try 2,3,4,4 holes): ", end='')
    if len(sys.argv) == 2:
        al = sys.argv[1]
    else:
        al = input()
    print(f"{al}\n\n\n\n")
    CatAndMouse(4, al).start()
    print("\n\n\n\n")


if __name__ == "__main__":
    main()
