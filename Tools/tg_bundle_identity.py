"""Give cloned bundles independent serialized-file identities.

Unity checks CAB names, not just the outer bundle filename or m_Name. Preserve
external donor references, but rewrite this bundle's own streaming paths.
"""
import hashlib

def unique_files(env, identity):
    # Derive from the logical identity alone so repeated builds stay stable.
    stem = 'CAB-' + hashlib.md5(identity.encode()).hexdigest()
    mapping = {name: stem + ('.' + name.split('.', 1)[1] if '.' in name else '')
               for name in env.file.files if name.startswith('CAB-')}
    def rewrite(value):
        if isinstance(value, str):
            for old, new in sorted(mapping.items(), key=lambda p: -len(p[0])):
                value = value.replace(old, new)
            return value
        if isinstance(value, dict): return {key: rewrite(item) for key, item in value.items()}
        if isinstance(value, list): return [rewrite(item) for item in value]
        if isinstance(value, tuple): return tuple(rewrite(item) for item in value)
        return value
    for asset in env.assets:
        for obj in asset.objects.values():
            tree = obj.read_typetree()
            updated = rewrite(tree)
            if updated != tree: obj.save_typetree(updated)
        for external in asset.externals: external.path = rewrite(external.path)
        asset.name = mapping.get(asset.name, asset.name)
    env.file.files = {mapping.get(name, name): value for name, value in env.file.files.items()}

