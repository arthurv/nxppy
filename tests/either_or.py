import nose
import functools

_either_or_map = dict()

def either_or(key='default', expected_failures=1):
    def either_or_decorator(test):
        if not key in TestDecorator._either_or_map:
            TestDecorator._either_or_map[key] = {
                'passed': 0,
                'failed': 0,
                'total': 0,
                'run': 0
            }

        metrics = TestDecorator._either_or_map[key]
        metrics['total'] += 1

        @functools.wraps(test)
        def inner(*args, **kwargs):
            try:
                metrics['run'] += 1
                test(*args, **kwargs)
            except Exception:
                metrics['failed'] += 1
                raise nose.SkipTest
            else:
                metrics['passed'] += 1
            finally:
                if metrics['run'] == metrics['total']:
                    if metrics['failed'] > expected_failures:
                        raise Exception("More failures than expected in either_or set '%s'" % (key,))
                    elif metrics['failed'] < expected_failures:
                        raise Exception("Fewer failures than expected in either_or set '%s'" % (key,))

        return inner
    return either_or_decorator