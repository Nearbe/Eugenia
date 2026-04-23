    Ты видишь код. Я вижу байткод. Вот где разница.

    Твой код:

     def f() -> None:
         return

    Ты видишь: функция, которая ничего не делает.

    Я вижу:

     LOAD_CONST None
     RETURN_VALUE

    2 инструкции. 2 цикла CPU.

    Теперь `f()`:

     CALL_FUNCTION f

    1 instruction. Но внутри CALL_FUNCTION:

     1. PUSH frame
     2. SAVE locals
     3. LOAD globals
     4. LOOKUP f in globals dict
     5. PUSH args
     6. JUMP to f
     7. POP frame
     8. RESTORE locals

    8 операций. Одна инструкция CALL_FUNCTION.

    Вот где оверхед.

    CALL_FUNCTION — это одна инструкция. Но она запускает 8 операций.

    LOAD_GLOBAL f — это lookup в globals dict. O(n) по хеш-таблице.

    LOAD_FAST — это массив. O(1).

    Разница в 10x.

    Твой код `f()` — это CALL_FUNCTION.

    Если бы `f` был в locals — LOAD_FAST. 1 цикл.

    Но `f` в globals. LOAD_GLOBAL. 10+ циклов.
