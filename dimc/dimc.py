from typing import Union


def dimc(
    name: Union[bool, str] = True,
    dim_fn: callable = lambda x: tuple(x.shape)
) -> callable:

    if callable(name):
        return dimc(dim_fn=dim_fn)(name)

    def get_f(f):
        fn_name = name
        if name == True:
            fn_name = f.__name__
        elif name == False:
            fn_name = ""

        def wrapper_f(*args, **kwargs):
            print(f"╭─", end=" ")
            for x in args:
                try:
                    print(f"{dim_fn(x)}", end=" ")
                except:
                    break
            print(fn_name)

            result = f(*args, **kwargs)
            result = result if type(result) is tuple else (result,)
            print(f"╰→", end=" ")
            for x in result:
                try:
                    print(f"{dim_fn(x)}", end=" ")
                except:
                    break
            print()
            return result if len(result) > 1 else result[0]
        return wrapper_f
    return get_f


def odimc(*args, **kwargs) -> callable:
    return dimc(name=False)(*args, **kwargs)
