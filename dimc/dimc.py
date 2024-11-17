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

class DimTrack:
    def __init__(
            self,
            indent: int = 0,
            dim_fn: callable = lambda x: str(tuple(x.shape))
        ):
        self.indent = indent
        self.dim_fn = dim_fn
        self.f_id  = -1
        self.f_info = {}
        self.stack  = [] 
    
    def __call__(self, f, *args, **kwargs):
        def f_wrapper(*args, **kwargs):
            self.f_id += 1
            f_id = self.f_id

            in_shapes  = []
            self.stack.append(f_id)
            # TODO: make forloop compatible for both args and kwargs
            for x in args:
                try: in_shapes.append(self.dim_fn(x))
                except: pass

            out_shapes = []
            result = f(*args, **kwargs)
            # TODO: make forloop compatible for both args and kwargs
            for x in (result if type(result) is tuple else (result,)):
                try: out_shapes.append(self.dim_fn(x))
                except: pass
            
            self.stack.append(f_id)
            self.f_info[f_id] = {
                "in_shapes": in_shapes,
                "out_shapes": out_shapes,
            }
            return result
        return f_wrapper
    
    def _process(self):
        visited  = []
        levels = []
        level  = -1
        for f_id in self.stack:
            if f_id in visited:
                levels.append(level)
                level -= 1
            else:
                visited.append(f_id)
                level += 1
                levels.append(level)
        self.levels = levels
        
    def show(self):
        self._process()
        max_level = max(self.levels)
        head_decorations = []
        visited = []
        for f_id, level in zip(self.stack, self.levels):
            temp = []
            for i in range(max_level+1):
                if i < level:
                    temp.append("│" + " "*self.indent)
                elif i == level:
                    temp.append("╰" if f_id in visited else "╭")
                elif i > level:
                    temp.append("─")
            temp.append("→" if f_id in visited else "─")
            head_decorations.append("".join(temp))
            visited.append(f_id)

        visited = []
        s = []
        for f_id, d in zip(self.stack, head_decorations):
            temp = ""            
            temp += d
            temp += " "
            if f_id in visited:
                temp += " ".join(self.f_info[f_id]["out_shapes"])
            else:
                temp += " ".join(self.f_info[f_id]["in_shapes"])
            s.append(temp)
            visited.append(f_id)
        
        s = "\n".join(s)
        print(s)

