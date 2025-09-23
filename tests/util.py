def relative_error_check(value: float, reference: float, relative_error: float) -> bool:
    return reference * (1 - relative_error) <= value <= reference * (1 + relative_error)


def absolute_error_check(value: float, reference: float, absolute_error: float) -> bool:
    return reference - absolute_error <= value <= reference + absolute_error
