import argparse


def valid_mtu(value):
    if not (68 <= int(value) <= 100000000):
        raise argparse.ArgumentTypeError("MTU должен быть в промежутке от 68 до 100000000")
    return int(value)


def parse_args():
    parser = argparse.ArgumentParser(description="Поиска минимального значения MTU в канале между хостами")
    parser.add_argument("--address", type=str, required=True, help="Адрес назначения")
    parser.add_argument("--min_mtu", type=valid_mtu, default=68, help="Минимальное значение MTU")
    parser.add_argument("--max_mtu", type=valid_mtu, default=3000, help="Максимальное значение MTU")
    parser.add_argument("--interval", type=float, default=0, help="Интервал между попытками в секундах (float)")

    return parser.parse_args()
