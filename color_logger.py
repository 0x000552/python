"""
Colorize stream logger.

22.11.2018 by 0x000552
"""
from datetime import datetime
import sys


class ColorLogger:
    """

    """
    D_iCOLOR = {
        # Service colors:
        0: "\033[94m[I]",       # Blue
        1: "\033[93m[W]",       # Yellow
        2: "\033[91m[E]",       # Red
        3: "\033[1;41;97m[D]",  # Bold Black on Red
        # Regular colors:
        # White on x background
        10: "\033[2;107;30m",   # black
        # 11: "\033[2;107;31m",   # dRed
        12: "\033[2;107;32m",   # dGreen
        13: "\033[2;107;33m",   # dYellow
        14: "\033[2;107;34m",   # dBlue
        15: "\033[2;107;35m",   # dPink
        16: "\033[2;107;36m",   # dTurquoise
        17: "\033[2;107;90m",   # Grey
        # 18: "\033[2;107;91m",   # Red
        19: "\033[2;107;92m",   # Green
        20: "\033[2;107;94m",   # Blue
        21: "\033[2;107;95m"    # Pink
    }

    iMAX_COLOR = max(D_iCOLOR)
    iBEG_REGULAR_COLOR = 10  # see above

    def __init__(self, LOG_STREAM=sys.stdout):
        self.LOG_STREAM = LOG_STREAM
        self._icurrent_regular_color = self.iMAX_COLOR + 1  # Re-init at first inext_regular_color getting
        # property (non-data) next_color_id

    @property
    def inext_regular_color(self):
        if self._icurrent_regular_color > self.iMAX_COLOR:
            self._icurrent_regular_color = self.iBEG_REGULAR_COLOR
        else:
            for _ in range(self._icurrent_regular_color, self.iMAX_COLOR+1):
                self._icurrent_regular_color += 1
                if self._icurrent_regular_color in self.D_iCOLOR:
                    break
        return self._icurrent_regular_color

    def log_it(self, message, icolor=None, indent=0):
        if icolor in self.D_iCOLOR.keys():
            if (icolor // 10) < 0:
                # Service colors
                msg = f"\n{' ' * indent}{self.D_iCOLOR[icolor]} {datetime.now().strftime('%X')} {message!r}\033[0m\n"
            else:
                # Regular colors
                msg = f"{' ' * indent}{self.D_iCOLOR[icolor]} {datetime.now().strftime('%X')} {message!r}\033[0m"
        else:
            # Without color
            msg = f"{' ' * indent}{datetime.now().strftime('%X')} {message!r}"
        print(msg, file=self.LOG_STREAM)


if __name__ == "__main__":
    print("WOWOWOW! I can't be runing as main!")
