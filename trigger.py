from collision import Platform


class Trigger(Platform):
    def __init__(self, enter: str, stay: str, exit: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.enter = movements[fcn] if fcn else movements['follows']


triggers = {
    'none': lambda: None
}


