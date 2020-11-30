def get_month_digit_formatted(month_digit):
    return '0' + str(month_digit) if len(month_digit) == 1 else str(month_digit)


def mkdir_folder(my_path):
    from errno import EEXIST
    from os import makedirs, path

    try:
        makedirs(my_path)
    except OSError as exc:
        if exc.errno == EEXIST and path.isdir(my_path):
            pass
        else:
            raise
