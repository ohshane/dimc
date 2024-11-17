from typing import Union


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
    
    def __call__(self, *args, **kwargs):
        return self.dimtrack(*args, **kwargs)
    
    def odimtrack(self, f) -> callable:
        return self.dimtrack(name=False)(f)

    def dimtrack(self, name: Union[bool, str] = True) -> callable:
        if callable(name):
            return self.dimtrack()(name)

        def get_f(f):
            f_name = name
            if name == True:
                f_name = f.__name__
            elif name == False:
                f_name = ""

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
                    "f_name": f_name,
                    "in_shapes": in_shapes,
                    "out_shapes": out_shapes,
                }
                return result
            return f_wrapper
        return get_f
    
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

    def __repr__(self) -> str:
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
                f_name = self.f_info[f_id]["f_name"]
                if f_name:
                    temp += f" :: {f_name}"

            s.append(temp)
            visited.append(f_id)
        
        s = "\n".join(s)
        return s
        
    def show(self) -> None:
        print(self.__repr__())