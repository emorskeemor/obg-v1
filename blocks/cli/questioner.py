from typing import Any, Iterable
from webbrowser import get

from blocks.cli.execeptions import ValidationError


class IOCLIMixin:
    '''
    input/output CLI mixin which provides methods which make interacting with
    the CLI easier and more practical.
    '''
    msg_formats = {
        "?":"| ? %s",
        "!":"| ! %s",
        "error":"\n| Error : %s",
        "i":"| # %s",
        ">":"=> %s",
        "%":"| %% %s"
    }
    accept_types = ["y","Y","Yes","yes"]

    def normalise(self, msg:str, ttype:str, end=False):
        format_type = self.msg_formats.get(ttype, None)
        if format_type is None:
            raise KeyError("could not find a valid format type called '%s'" % ttype)
        formatted = format_type % msg
        if end:
            return "%s : " % formatted
        return formatted

    def output(self, message:str, ttype:str=None, end=False, newline=False):
        if ttype is None:
            ttype = "i"
        
        res = self.normalise(message, ttype, end)
        if newline:
            res = "%s\n" % res
        print(res)


    def question(self, message:str, expec_type:Any=str, default=None, blank=False):
        result = input(self.normalise(message, "?", end=True))
        if not result.strip():
            if default is not None:
                return default
            elif blank:
                return result
            raise ValidationError("you cannot leave this question unanswered")
        try:
            if expec_type is bool:
                if result in self.accept_types:
                    return True
                return False
            return expec_type(result)
        except ValueError:
            raise ValidationError("Expected type '%s' for question input" % expec_type)


    def newline(self):
        print("")

    def choices(self, message:str, choices:dict|list|tuple, default=None) -> Any:
        self.output(message, "%", newline=True)
        # display the choices
        if type(choices) is dict:
            for key, data in choices.items():
                msg = data
                if type(data) is dict:
                    msg = data.get("msg")
                elif type(data) is tuple:
                    msg = data[0]
                self.output("%s : %s" % (key, msg), ">")

        elif type(choices) in (list, tuple):
            for opt in choices:
                self.output(opt, ">")
        self.newline()
        # get selection
        try:
            if type(choices) is dict:
                msg = "Enter options"
                if default is not None:
                    msg = "%s (%s)" % (msg, default)
                selected = self.question(msg, str)
                data = choices.get(selected,None)
                if data is None:
                    if default is not None:
                        return choices.get(default)
                    else:
                        raise IndexError()
                elif type(data) is dict:
                    callback = data.get("callback", None)
                    if callable(callback):
                        return callback()
                    result = data.get("result", selected)
                    return result
                elif type(data) is tuple and len(data) == 2:
                    msg, result = data
                    if callable(result):
                        return result()
                    return result
                else:
                    if callable(data):
                        return data()
                    return selected
            else:
                msg = "Enter option (%s-%s)" % (1,len(choices))
                if default is not None and type(default) is int:
                    msg = "%s (%s)" % (msg, default)
                selected = self.question(msg, int, default=default) 
                return choices[selected-1]
        except IndexError:
            self.output("Invalid choice", "error")
        except TypeError:
            pass