# import time
# import functools
# import logging

# logger = logging.getLogger(__name__)


# def measure_latency(func):
#     @functools.wraps(func)
#     async def wrapper(*args, **kwargs):
#         start = time.perf_counter()

#         try:
#             return await func(*args, **kwargs)
#         finally:
#             latency = time.perf_counter() - start
#             logger.info(msg=f"Function {func.__name__!a} executed in {latency:.6f} seconds.")
#     return wrapper



# import time
# import functools
# import inspect
# import logging

# logger = logging.getLogger(__name__)


# def measure_latency(func):

#     if inspect.iscoroutinefunction(func):

#         @functools.wraps(func)
#         async def async_wrapper(*args, **kwargs):
#             start = time.perf_counter()

#             try:
#                 return await func(*args, **kwargs)
#             finally:
#                 latency_ms = (
#                     time.perf_counter() - start
#                 ) * 1000

#                 logger.info(
#                     "function=%s latency_ms=%.2f",
#                     func.__qualname__,
#                     latency_ms,
#                 )

#         return async_wrapper

#     @functools.wraps(func)
#     def sync_wrapper(*args, **kwargs):
#         start = time.perf_counter()

#         try:
#             return func(*args, **kwargs)
#         finally:
#             latency_ms = (
#                 time.perf_counter() - start
#             ) * 1000

#             logger.info(
#                 "function=%s latency_ms=%.2f",
#                 func.__qualname__,
#                 latency_ms,
#             )

#     return sync_wrapper