try:
    from mppi import MPPI, MovingCircle
except ImportError:
    from mppiFull import MPPI, MovingCircle
from simulator import run_examples


if __name__ == "__main__":
    raise SystemExit(0 if run_examples(MPPI, MovingCircle) else 1)