import functools
from flask import request

def _filter_query(model, query, filter_spec):
    filters = [f.split(',') for f in filter_spec.split(';')]
    for f in filters:
        if len(f) < 3 or (len(f) > 3 and f[1] != 'in'):
            continue
        if f[1] == 'in':
            f = [f[0], f[1], f[2:]]
        ops = {'eq': '__eq__', 'ne': '__ne__', 'lt': '__lt__', 'le': '__le__',
               'gt': '__gt__', 'ge': '__ge__', 'in': 'in_', 'like': 'like'}
        if hasattr(model, f[0]) and f[1] in ops.keys():
            column = getattr(model, f[0])
            op = ops[f[1]]
            query = query.filter(getattr(column, op)(f[2]))
    return query

def _sort_query(model, query, sort_spec):
    sort = [s.split(',') for s in sort_spec.split(';')]
    for s in sort:
        if hasattr(model, s[0]):
            column = getattr(model, s[0])
            if len(s) == 2 and s[1] in ['asc', 'desc']:
                query = query.order_by(getattr(column, s[1])())
            else:
                query = query.order_by(column.asc())
    return query

def collection(model):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            query = f(*args, **kwargs)
            # filtering and sorting
            filter = request.args.get('filter')
            if filter:
                query = _filter_query(model, query, filter)
                return query
            sort = request.args.get('sort')
            if sort:
                query = _sort_query(model, query, sort)
                return query
        return wrapped
    return decorator
