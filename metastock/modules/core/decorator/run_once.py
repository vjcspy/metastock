def run_once(func):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return func(*args, **kwargs)
        else:
            return "Function đã được gọi rồi."

    wrapper.has_run = False
    return wrapper
