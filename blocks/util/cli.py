import inspect


def non_command(func):
    '''
    ensures that the function will be not treated as a command that can be accessed
    by the CLI
    '''
    def wrapper():
        func.__ignore__ = True
        return func
    return wrapper()

class CliManager:
    '''
    Object that handles function execution from the command line.

    class Handler(CliManager):
        def method(*args, **kwargs):
            ...
        
    handler = Handler().exec(argv)
    
    methods that beign with '_' are automatically ignored.
    Use @non_command to ignore a function as a commands
    '''
    def __init__(self, **opts) -> None:
        self.opts = opts
        
    def _func_details(self, func, ):
        signature = inspect.signature(func)
        params = ", ".join([f"{v}" for v in signature.parameters.values()])
        help_text = f" => {func.__doc__}" if func.__doc__ is not None else ""
        print(f"\n> {func.__name__}({params})" + help_text)

    def cmds(self):
        '''display all commands that can be called from the command line and their arguments'''
        print("<Displaying commands>")
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if self._is_command(attr):
                
                self._func_details(attr)

    @staticmethod
    def _is_command(func):
        name:str = getattr(func, "__name__", "")
        if not callable(func):
            return False
        elif getattr(func, "__ignore__", False) is True:
            return False
        elif name.startswith("__") or name.startswith("_"):
            return False
        elif type(func) is type:
            return False
        return True

        
    @non_command
    def exec(self, sys_argvs:list):
        '''execute commands from the command line'''
        if len(sys_argvs) < 1:
            raise IndexError("sys arguments require atleast one item")
        if type(sys_argvs) is not list:
            raise TypeError("sys arguments type must be a list")
        # remove file name 
        sys_argvs.pop(0)
        if len(sys_argvs) == 0:
            return None
        cmd = sys_argvs.pop(0)
        args = sys_argvs[0:]

        func = getattr(self, cmd, None)
        # unknown command
        if not self._is_command(func):
            print("unknown command :", cmd)
            return
        # special commands
        if len(args) > 0:
            if args[0] == "-h":
                print(f"<Displaying data about '{func.__name__}'>")
                return self._func_details(func)
        # execute function from cli
        instance = getattr(func, "__instance__", False)
        if instance:
            return func(self, *args)
        return func(*args)

    @non_command
    def register(self, func, instance=False, name:str=None):
        '''
        registers an external function as a command. 
        
        instance=False defines if the function should be passed the instance
        '''
        if name is not None:
            if " " in name:
                raise ValueError("whitespaces are not allowed in the command name")
            setattr(func, "__name__", name)
        if instance:
            setattr(func, "__instance__", True)
        setattr(self, func.__name__, func)

    


 