============================= test session starts =============================
platform win32 -- Python 3.12.12, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\joaoc\Projects\bgg-search-telegram-bot
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.12.0, cov-7.0.0
collected 2 items

tests\test_bgg_client.py FF                                              [100%]

================================== FAILURES ===================================
_________________ TestBGGClient.test_search_game_returns_list _________________

args = (<tests.test_bgg_client.TestBGGClient object at 0x0000019033B279B0>,)
keywargs = {}

    @wraps(func)
    def patched(*args, **keywargs):
>       with self.decoration_helper(patched,
                                    args,
                                    keywargs) as (newargs, newkeywargs):

..\..\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\unittest\mock.py:1393: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
..\..\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\contextlib.py:137: in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
..\..\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\unittest\mock.py:1375: in decoration_helper
    arg = exit_stack.enter_context(patching)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\contextlib.py:526: in enter_context
    result = _enter(cm)
             ^^^^^^^^^^
..\..\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\unittest\mock.py:1451: in __enter__
    self.target = self.getter()
                  ^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

name = 'bgg_client.requests'

    def resolve_name(name):
        """
        Resolve a name to an object.
    
        It is expected that `name` will be a string in one of the following
        formats, where W is shorthand for a valid Python identifier and dot stands
        for a literal period in these pseudo-regexes:
    
        W(.W)*
        W(.W)*:(W(.W)*)?
    
        The first form is intended for backward compatibility only. It assumes that
        some part of the dotted name is a package, and the rest is an object
        somewhere within that package, possibly nested inside other objects.
        Because the place where the package stops and the object hierarchy starts
        can't be inferred by inspection, repeated attempts to import must be done
        with this form.
    
        In the second form, the caller makes the division point clear through the
        provision of a single colon: the dotted name to the left of the colon is a
        package to be imported, and the dotted name to the right is the object
        hierarchy within that package. Only one import is needed in this form. If
        it ends with the colon, then a module object is returned.
    
        The function will return an object (which might be a module), or raise one
        of the following exceptions:
    
        ValueError - if `name` isn't in a recognised format
        ImportError - if an import failed when it shouldn't have
        AttributeError - if a failure occurred when traversing the object hierarchy
                         within the imported package to get to the desired object.
        """
        global _NAME_PATTERN
        if _NAME_PATTERN is None:
            # Lazy import to speedup Python startup time
            import re
            dotted_words = r'(?!\d)(\w+)(\.(?!\d)(\w+))*'
            _NAME_PATTERN = re.compile(f'^(?P<pkg>{dotted_words})'
                                       f'(?P<cln>:(?P<obj>{dotted_words})?)?$',
                                       re.UNICODE)
    
        m = _NAME_PATTERN.match(name)
        if not m:
            raise ValueError(f'invalid format: {name!r}')
        gd = m.groupdict()
        if gd.get('cln'):
            # there is a colon - a one-step import is all that's needed
            mod = importlib.import_module(gd['pkg'])
            parts = gd.get('obj')
            parts = parts.split('.') if parts else []
        else:
            # no colon - have to iterate to find the package boundary
            parts = name.split('.')
            modname = parts.pop(0)
            # first part *must* be a module/package.
            mod = importlib.import_module(modname)
            while parts:
                p = parts[0]
                s = f'{modname}.{p}'
                try:
                    mod = importlib.import_module(s)
                    parts.pop(0)
                    modname = s
                except ImportError:
                    break
        # if we reach this point, mod is the module, already imported, and
        # parts is the list of parts in the object hierarchy to be traversed, or
        # an empty list if just the module is wanted.
        result = mod
        for p in parts:
>           result = getattr(result, p)
                     ^^^^^^^^^^^^^^^^^^
E           AttributeError: module 'bgg_client' has no attribute 'requests'

..\..\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\pkgutil.py:528: AttributeError
___________ TestBGGClient.test_get_games_details_returns_thumbnails ___________

args = (<tests.test_bgg_client.TestBGGClient object at 0x0000019034A56A80>,)
keywargs = {}

    @wraps(func)
    def patched(*args, **keywargs):
>       with self.decoration_helper(patched,
                                    args,
                                    keywargs) as (newargs, newkeywargs):

..\..\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\unittest\mock.py:1393: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
..\..\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\contextlib.py:137: in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
..\..\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\unittest\mock.py:1375: in decoration_helper
    arg = exit_stack.enter_context(patching)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\contextlib.py:526: in enter_context
    result = _enter(cm)
             ^^^^^^^^^^
..\..\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\unittest\mock.py:1451: in __enter__
    self.target = self.getter()
                  ^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

name = 'bgg_client.requests'

    def resolve_name(name):
        """
        Resolve a name to an object.
    
        It is expected that `name` will be a string in one of the following
        formats, where W is shorthand for a valid Python identifier and dot stands
        for a literal period in these pseudo-regexes:
    
        W(.W)*
        W(.W)*:(W(.W)*)?
    
        The first form is intended for backward compatibility only. It assumes that
        some part of the dotted name is a package, and the rest is an object
        somewhere within that package, possibly nested inside other objects.
        Because the place where the package stops and the object hierarchy starts
        can't be inferred by inspection, repeated attempts to import must be done
        with this form.
    
        In the second form, the caller makes the division point clear through the
        provision of a single colon: the dotted name to the left of the colon is a
        package to be imported, and the dotted name to the right is the object
        hierarchy within that package. Only one import is needed in this form. If
        it ends with the colon, then a module object is returned.
    
        The function will return an object (which might be a module), or raise one
        of the following exceptions:
    
        ValueError - if `name` isn't in a recognised format
        ImportError - if an import failed when it shouldn't have
        AttributeError - if a failure occurred when traversing the object hierarchy
                         within the imported package to get to the desired object.
        """
        global _NAME_PATTERN
        if _NAME_PATTERN is None:
            # Lazy import to speedup Python startup time
            import re
            dotted_words = r'(?!\d)(\w+)(\.(?!\d)(\w+))*'
            _NAME_PATTERN = re.compile(f'^(?P<pkg>{dotted_words})'
                                       f'(?P<cln>:(?P<obj>{dotted_words})?)?$',
                                       re.UNICODE)
    
        m = _NAME_PATTERN.match(name)
        if not m:
            raise ValueError(f'invalid format: {name!r}')
        gd = m.groupdict()
        if gd.get('cln'):
            # there is a colon - a one-step import is all that's needed
            mod = importlib.import_module(gd['pkg'])
            parts = gd.get('obj')
            parts = parts.split('.') if parts else []
        else:
            # no colon - have to iterate to find the package boundary
            parts = name.split('.')
            modname = parts.pop(0)
            # first part *must* be a module/package.
            mod = importlib.import_module(modname)
            while parts:
                p = parts[0]
                s = f'{modname}.{p}'
                try:
                    mod = importlib.import_module(s)
                    parts.pop(0)
                    modname = s
                except ImportError:
                    break
        # if we reach this point, mod is the module, already imported, and
        # parts is the list of parts in the object hierarchy to be traversed, or
        # an empty list if just the module is wanted.
        result = mod
        for p in parts:
>           result = getattr(result, p)
                     ^^^^^^^^^^^^^^^^^^
E           AttributeError: module 'bgg_client' has no attribute 'requests'

..\..\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\pkgutil.py:528: AttributeError
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.12-final-0 _______________

Name            Stmts   Miss  Cover   Missing
---------------------------------------------
bgg_client.py      56     40    29%   16-19, 24-50, 55-56, 61-97
handlers.py       103    103     0%   1-196
main.py            27     27     0%   1-59
---------------------------------------------
TOTAL             186    170     9%
=========================== short test summary info ===========================
FAILED tests/test_bgg_client.py::TestBGGClient::test_search_game_returns_list
FAILED tests/test_bgg_client.py::TestBGGClient::test_get_games_details_returns_thumbnails
============================== 2 failed in 1.56s ==============================
