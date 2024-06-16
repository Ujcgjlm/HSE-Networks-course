import icmplib
import sys
import time

import parser
from logger import logging
from binary_search import binary_search


HEADER_SIZE = 28
TEST_CASE_SEPARATOR = "--------------------------------------------------------"


def verify_host_reachability(address):
    logging.info(f"Проверяем достижимость адреса: {address}")

    if not icmplib.ping(address):
        logging.error("Адрес не достежим")
        sys.exit(1)


def ping_with_fixed_mtu_size(address, interval, mid_mtu):
    payload_size = mid_mtu - HEADER_SIZE

    logging.info(TEST_CASE_SEPARATOR)
    logging.info(f"Пробуем MTU: {mid_mtu}")
    logging.info(f"Размер данных в пинге за вычетом хедера: {payload_size}")
    try:
        ping_res = icmplib.ping(
            address,
            interval=interval,
            payload_size=payload_size,
        )
    except icmplib.exceptions.DestinationUnreachable:
        logging.error(f"Хост {address} недостежим")
        exit(0)
    except icmplib.exceptions.NameLookupError:
        logging.error(f"Хост {address} не может быть определен")
        exit(0)
    except icmplib.exceptions:
        logging.error("Неизвестная ошибка icmplib")
        exit(1)
    except Exception:
        logging.error("Неизвестная ошибка")
        exit(1)

    return ping_res


def find_mtu(address, min_mtu, max_mtu, interval):

    def checker(cur_mtu):
        res = ping_with_fixed_mtu_size(address, interval, cur_mtu).is_alive
        time.sleep(interval)
        return res

    return binary_search(min_mtu, max_mtu, checker)


def check_minimal_mtu(address, min_mtu, max_mtu, interval):
    verify_host_reachability(address)

    try:
        mtu = find_mtu(address, min_mtu, max_mtu, interval)
    except Exception as e:
        logging.info(TEST_CASE_SEPARATOR)
        logging.exception(f"Произошла ошибка: {e}")
        sys.exit(1)

    logging.info(TEST_CASE_SEPARATOR)
    if mtu:
        logging.info(f"Минимальный MTU: {mtu}")
    else:
        logging.error("Не удалось определить MTU для указанного диапазона.")

    return mtu


if __name__ == "__main__":
    args = parser.parse_args()
    check_minimal_mtu(**vars(args))
