============================= test session starts =============================
platform win32 -- Python 3.12.12, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\joaoc\Projects\bgg-search-telegram-bot\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\joaoc\Projects\bgg-search-telegram-bot
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.12.0, asyncio-1.3.0, cov-7.0.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 2 items

tests/test_bgg_client.py::TestBGGClient::test_search_game_returns_list PASSED [ 50%]
tests/test_bgg_client.py::TestBGGClient::test_get_games_details_returns_thumbnails PASSED [100%]

=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.12-final-0 _______________

Name            Stmts   Miss  Cover   Missing
---------------------------------------------
bgg_client.py      56      3    95%   55-56, 62
handlers.py       103    103     0%   1-196
main.py            27     27     0%   1-59
---------------------------------------------
TOTAL             186    133    28%
============================== 2 passed in 1.02s ==============================
