# Use with generators

**iter_model** allows to decorate generator so that it returns SyncIter\AsyncIter on output.

## Example

=== "SyncIter"
    ```python
    from iter_model import SyncIter, sync_iter
    
    @sync_iter
    def fibonacci_numbers(n: int) -> SyncIter[int]:
        """Generator of Fibonacci numbers"""
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b
    
    
    for number in fibonacci_numbers().take_while(lambda x: x < 100):  # The generator receives the SyncIter methods
        print(number)
    
    ```

=== "AsyncIter"

    ```python
    import asyncio
    
    from iter_model import AsyncIter, async_iter
    
    
    @async_iter
    async def fibonacci_numbers(n: int) -> AsyncIter[int]:
        """Generator of Fibonacci numbers"""
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b
    
    
    async def main():
        async for number in fibonacci_numbers().take_while(lambda x: x < 100):  # The generator receives the AsyncIter methods
            print(number)
    
    
    asyncio.run(main())
    ```
