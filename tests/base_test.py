import os
import sys
import logging
import argparse
import inspect


def get_calling_module():
    '''Hacky little function to get the module name which is calling the
    function'''
    caller = inspect.stack()[2]
    globals_ = caller[0].f_globals

    module = os.path.splitext(os.path.basename(caller[1]))[0]

    if globals_.get('__package__'):
        package = globals_.get('__package__')
        return '%s.%s' % (package, module)
    else:
        return module


def get_module(module_name):
    '''Smart import wrapper which gets foo if you ask for foo and bar if you
    ask for foo.bar'''
    module_name = module_name.rsplit('.', 1)
    if module_name[1:]:
        package_name, module_name = module_name
        package = __import__(package_name, fromlist=[module_name])
        return getattr(package, module_name)
    else:
        return __import__(module_name)


def main(*argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v',
        '--verbosity',
        action='count',
        help='Increase verbosity',
    )
    parser.add_argument(
        'modules',
        nargs='*',
        default=[get_calling_module()],
    )

    args = parser.parse_args(argv or sys.argv)
    if args.verbosity > 1:
        level = logging.DEBUG
    elif args.verbosity:
        level = logging.INFO
    else:
        level = logging.WARN

    logger = logging.getLogger('')
    logger.setLevel(level)
    logger.addHandler(logging.StreamHandler())

    for module_name in args.modules:
        module = get_module(module_name)
        for k, v in module.__dict__.items():
            if k.startswith('test_') and hasattr(v, '__call__'):
                print 'Running %r' % k
                v()

