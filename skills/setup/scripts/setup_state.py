#!/usr/bin/env python3
"""Private Ad Remaker preferences and product state, with no network operations."""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

VERSION = 1
ROUTES = {
    'research': {'free', 'deferred', 'trendtrack', 'brandsearch', 'meta_ads'},
    'generation': {'free', 'deferred', 'higgsfield', 'pika', 'fal', 'kie-ai'},
    'delivery': {'free', 'deferred', 'meta_ads'},
}
BRIEF_FIELDS = {'name', 'url', 'audience', 'markets', 'competitors', 'approved_claims', 'asset_paths', 'sources'}
SECRET = re.compile(r'(?i)(?:bearer\s+\S+|(?:api[_ -]?key|password|access[_ -]?token|client[_ -]?secret)\s*[:=]|sk-[a-zA-Z0-9_-]{16,}|gh[pousr]_[a-zA-Z0-9]{20,})')


class StateError(ValueError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def ordinary_path(value):
    path = Path(value).expanduser().absolute()
    if any(p.is_symlink() for p in [path, *path.parents]):
        raise StateError('Symlink state paths are not supported.')
    return path.resolve()


def state_root(runtime, override=None, profile_home=None):
    if override:
        root = ordinary_path(override)
    elif runtime == 'hermes':
        active = profile_home or os.environ.get('HERMES_HOME')
        if not active:
            raise StateError('Identify the active installed Hermes profile home first; no default-profile guess.')
        root = ordinary_path(active) / 'ad-remaker-state'
    else:
        base = os.environ.get('XDG_CONFIG_HOME') or str(Path.home() / '.config')
        root = ordinary_path(base) / 'ad-remaker' / runtime
    source = Path(__file__).resolve().parents[3]
    active = profile_home or os.environ.get('HERMES_HOME')
    manifest = source / 'distribution.yaml'
    installed_profile_state = (runtime == 'hermes' and active
                               and ordinary_path(active) == source
                               and root == source / 'ad-remaker-state'
                               and manifest.is_file()
                               and re.search(r'^source:\s*\S+', manifest.read_text(), re.MULTILINE))
    if (root == source or source in root.parents) and not installed_profile_state:
        raise StateError('State must be outside the distribution or installed Skill tree.')
    for parent in [root, *root.parents]:
        if parent == source and installed_profile_state:
            continue
        if (parent / '.codex-plugin').exists() or (parent / '.claude-plugin').exists():
            raise StateError('State must be outside plugin sources and caches.')
    return root


def empty():
    return {'schema_version': VERSION, 'complete': False, 'routes': {}, 'fallback': 'ask', 'connections': {}}


def safe_text(value):
    if not isinstance(value, str) or len(value) > 10000 or SECRET.search(value):
        raise StateError('Expected bounded non-secret text. Keep credentials in client storage.')
    return value


def validate_routes(routes):
    if not isinstance(routes, dict) or any(k not in ROUTES or not isinstance(v, str) or v not in ROUTES[k] for k, v in routes.items()):
        raise StateError('Invalid stage or route.')


def validate_brief(brief):
    if not isinstance(brief, dict) or set(brief) - BRIEF_FIELDS:
        raise StateError('Unknown brief fields; credentials and arbitrary configuration are prohibited.')
    if not isinstance(brief.get('name'), str) or not brief['name'].strip():
        raise StateError('A confirmed product name is required.')
    for key, value in brief.items():
        if key in {'name', 'url', 'audience'}:
            safe_text(value)
        else:
            if not isinstance(value, list) or len(value) > 100 or not all(isinstance(v, str) for v in value):
                raise StateError('Brief lists must contain at most 100 text entries.')
            for item in value:
                safe_text(item)


def validate(data, project=False):
    if not isinstance(data, dict) or type(data.get('schema_version')) is not int or data['schema_version'] != VERSION:
        raise StateError('Incompatible schema. Original file preserved; choose a fresh private state directory or migrate explicitly.')
    if project:
        if set(data) - {'schema_version', 'products', 'pending_task'} or not isinstance(data.get('products'), dict):
            raise StateError('Invalid project state.')
        safe_text(data.get('pending_task', ''))
        for key, item in data['products'].items():
            product_id(key)
            if not isinstance(item, dict) or set(item) != {'brief', 'routes'}:
                raise StateError('Invalid product record.')
            validate_brief(item['brief']); validate_routes(item['routes'])
    else:
        if set(data) != set(empty()) or type(data['complete']) is not bool or not isinstance(data['fallback'], str) or data['fallback'] not in {'ask', 'free'}:
            raise StateError('Invalid preference state.')
        validate_routes(data['routes'])
        if data['complete'] and set(data['routes']) != set(ROUTES):
            raise StateError('Completed state needs an explicit free, deferred or provider choice for every stage.')
        if not isinstance(data['connections'], dict):
            raise StateError('Invalid connection history.')
        vendors = set.union(*ROUTES.values()) - {'free', 'deferred'}
        for key, value in data['connections'].items():
            if key not in vendors or not isinstance(value, dict) or set(value) != {'status', 'checked_at'}:
                raise StateError('Invalid connection evidence.')
            if not isinstance(value['status'], str) or value['status'] not in {'selected', 'configured', 'verified', 'blocked'}:
                raise StateError('Invalid connection status.')
            safe_text(value['checked_at'])
            try:
                datetime.fromisoformat(value['checked_at'])
            except ValueError as error:
                raise StateError('Invalid evidence date.') from error


def load(path, project=False):
    ordinary_path(path)
    if not path.exists():
        return {'schema_version': VERSION, 'products': {}, 'pending_task': ''} if project else empty()
    if path.is_symlink() or not path.is_file():
        raise StateError('State must be an ordinary private file.')
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        validate(data, project)
        return data
    except (OSError, UnicodeError, json.JSONDecodeError, StateError) as error:
        raise StateError(f'Cannot load {path}: {error}. Original preserved; do not overwrite it.') from error


def save(path, data, project=False):
    ordinary_path(path)
    validate(data, project)
    if path.is_symlink():
        raise StateError('Refusing symlink write.')
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, name = tempfile.mkstemp(prefix='.setup-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def locked(root):
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = root / '.lock'
    if path.is_symlink():
        raise StateError('Refusing symlink lock.')
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(fd, 'r+b') as stream:
        if os.name == 'nt':
            import msvcrt
            if not path.stat().st_size:
                stream.write(b'0'); stream.flush()
            stream.seek(0); msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name == 'nt':
                stream.seek(0); msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def product_id(value):
    if not isinstance(value, str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', value):
        raise StateError('Product ID must be lowercase letters/digits/hyphens, at most 64 characters.')
    return value


def project_file(root, project):
    digest = hashlib.sha256(str(Path(project).expanduser().resolve()).encode()).hexdigest()
    return root / 'projects' / (digest + '.json')


def effective(user, product=None, task=None):
    result = dict(user['routes'])
    if product:
        result.update(product['routes'])
    if task:
        validate_routes(task); result.update(task)
    return result


def run(args):
    root = state_root(args.runtime, args.state_dir, args.profile_home)
    workspace = Path(args.project).expanduser().resolve()
    if root == workspace or workspace in root.parents:
        raise StateError('Private state must be outside the working project Git tree.')
    user_path = root / 'setup.json'
    project_path = project_file(root, args.project)
    # Read-only status/resolve never creates a state directory.
    mutation = args.action not in {'status', 'resolve'}
    def operation():
        user = load(user_path)
        project = load(project_path, True)
        if args.action == 'choose':
            for stage in ROUTES:
                value = getattr(args, stage)
                if value:
                    user['routes'][stage] = value
            if args.free:
                user['routes'] = dict.fromkeys(ROUTES, 'free')
            if args.fallback:
                user['fallback'] = args.fallback
            validate(user); save(user_path, user)
        elif args.action == 'complete':
            if set(user['routes']) != set(ROUTES):
                raise StateError('Answer or explicitly defer each stage before completing setup.')
            user['complete'] = True; save(user_path, user)
        elif args.action == 'task':
            project['pending_task'] = safe_text(args.task)
            save(project_path, project, True)
        elif args.action == 'product':
            key = product_id(args.product)
            brief = json.loads(args.brief)
            validate_brief(brief)
            routes = json.loads(args.overrides) if args.overrides is not None else project['products'].get(key, {}).get('routes', {})
            validate_routes(routes)
            project['products'][key] = {'brief': brief, 'routes': routes}
            save(project_path, project, True)
        elif args.action == 'connection':
            user['connections'][args.provider] = {'status': args.status, 'checked_at': now()}
            save(user_path, user)
        elif args.action == 'resolve':
            if not args.product and len(project['products']) > 1:
                raise StateError('Multiple products: select a product before resolving routes.')
            key = args.product or next(iter(project['products']), None)
            if key and key not in project['products']:
                raise StateError('Unknown product; validate its brief first.')
            task = json.loads(args.task_routes) if args.task_routes else {}
            return {'complete': user['complete'], 'product': key, 'routes': effective(user, project['products'].get(key), task), 'fallback': user['fallback'], 'connection_check_required': True}
        return {'state_dir': str(root), 'preferences': user, 'project': project,
                'connection_history_is_current': False}
    if mutation:
        with locked(root):
            return operation()
    return operation()


class SetupParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        # Clients often place shared flags after the action. Normalize only our
        # four known global options; argparse still validates every argument.
        words = list(sys.argv[1:] if args is None else args)
        globals_, remainder = [], []
        i = 0
        while i < len(words):
            if words[i] in {'--runtime', '--state-dir', '--profile-home', '--project'}:
                globals_.append(words[i])
                if i + 1 < len(words):
                    globals_.append(words[i + 1]); i += 2
                else:
                    i += 1
            else:
                remainder.append(words[i]); i += 1
        return super().parse_args(globals_ + remainder, namespace)


def parser():
    p = SetupParser(description=__doc__)
    p.add_argument('--runtime', required=True, choices=['claude', 'codex', 'hermes'])
    p.add_argument('--state-dir', help='Explicit private root, outside sources/caches (also for isolated tests).')
    p.add_argument('--profile-home', help='Active installed Hermes home, identified by the client.')
    p.add_argument('--project', required=True, help='Canonical working project directory, never the plugin root.')
    actions = p.add_subparsers(dest='action', required=True)
    actions.add_parser('status')
    choice = actions.add_parser('choose')
    choice.add_argument('--free', action='store_true')
    choice.add_argument('--fallback', choices=['ask', 'free'])
    for stage, routes in ROUTES.items():
        choice.add_argument('--' + stage, choices=sorted(routes))
    actions.add_parser('complete')
    task = actions.add_parser('task'); task.add_argument('--task', required=True)
    product = actions.add_parser('product')
    product.add_argument('--product', required=True); product.add_argument('--brief', required=True)
    product.add_argument('--overrides')
    connection = actions.add_parser('connection')
    connection.add_argument('--provider', choices=sorted(set.union(*ROUTES.values()) - {'free', 'deferred'}), required=True)
    connection.add_argument('--status', choices=['selected', 'configured', 'verified', 'blocked'], required=True)
    resolve = actions.add_parser('resolve')
    resolve.add_argument('--product'); resolve.add_argument('--task-routes')
    return p


def main():
    try:
        print(json.dumps(run(parser().parse_args()), ensure_ascii=False))
        return 0
    except (StateError, OSError, json.JSONDecodeError) as error:
        print(f'Setup state error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
