bgg_client.py:94: error: Dict entry 3 has incompatible type "str": "float"; expected "str": "str | None"  [dict-item]
tests\test_bgg_client.py:27: error: Argument 1 to "len" has incompatible type "Coroutine[Any, Any, list[dict[Any, Any]]]"; expected "Sized"  [arg-type]
tests\test_bgg_client.py:27: note: Maybe you forgot to use "await"?
tests\test_bgg_client.py:28: error: Value of type "Coroutine[Any, Any, list[dict[Any, Any]]]" is not indexable  [index]
tests\test_bgg_client.py:28: note: Maybe you forgot to use "await"?
tests\test_bgg_client.py:29: error: Value of type "Coroutine[Any, Any, list[dict[Any, Any]]]" is not indexable  [index]
tests\test_bgg_client.py:29: note: Maybe you forgot to use "await"?
tests\test_bgg_client.py:30: error: Value of type "Coroutine[Any, Any, list[dict[Any, Any]]]" is not indexable  [index]
tests\test_bgg_client.py:30: note: Maybe you forgot to use "await"?
tests\test_bgg_client.py:49: error: Unsupported right operand type for in ("Coroutine[Any, Any, dict[str, dict[str, str | None]]]")  [operator]
tests\test_bgg_client.py:49: note: Maybe you forgot to use "await"?
tests\test_bgg_client.py:50: error: Value of type "Coroutine[Any, Any, dict[str, dict[str, str | None]]]" is not indexable  [index]
tests\test_bgg_client.py:50: note: Maybe you forgot to use "await"?
handlers.py:64: error: Argument "key" to "sort" of "list" has incompatible type "Callable[[dict[Any, Any]], str | SupportsDunderLT[Any] | SupportsDunderGT[Any] | None]"; expected "Callable[[dict[Any, Any]], SupportsDunderLT[Any] | SupportsDunderGT[Any]]"  [arg-type]
handlers.py:64: error: Incompatible return value type (got "str | SupportsDunderLT[Any] | SupportsDunderGT[Any] | None", expected "SupportsDunderLT[Any] | SupportsDunderGT[Any]")  [return-value]
Found 9 errors in 3 files (checked 5 source files)
