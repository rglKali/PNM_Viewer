from config import LAUNCH_TESTS
from src.main import main


if __name__ == '__main__':
    if LAUNCH_TESTS:
        from tests import test
        test()

    main()
