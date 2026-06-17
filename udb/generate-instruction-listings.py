import argparse
import yaml

def build_database(files):
    db = {}

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            item = yaml.safe_load(f)
            if not ('kind' in item and 'name' in item):
                raise Exception("database entries must contain keys 'name' and 'kind'")
            if item['name'] in db.setdefault(item['kind'], {}):
                raise Exception(f"duplicate database entry '{item['name']}' of type '{item['kind']}'")
            db[item['kind']][item['name']] = item

    return db

def extensions_implied_by(ext):
    if 'requirements' not in ext:
        return []

    def traverse_extensions(x):
        key = next(iter(x))
        value = x[key]
        match key:
            case 'param':
                return []

            case 'idl()':
                return []

            case 'name':
                return [value]

            case 'not':
                return []

            case 'xlen':
                return []

            case 'extension':
                return traverse_extensions(value)

            case 'anyOf' | 'oneOf':
                return [item for sublist in map(traverse_extensions, value) for item in sublist]

            case 'allOf':
                if any('xlen' in d for d in value):
                    index = next((i for i, d in enumerate(value) if 'xlen' in d))
                    xlen = value[index]['xlen']
                    res = traverse_extensions({key: [d for d in value if 'xlen' not in d]})
                    #return list(map(lambda x: f"{x} (RV{xlen})", res))
                    return res

                return [item for sublist in map(traverse_extensions, value) for item in sublist]

            case _:
                raise Exception(f"unknown key {key}")

    return traverse_extensions(ext['requirements'])

def extensions_defined_in(inst):
    def traverse_extensions(x):
        key = next(iter(x))
        value = x[key]
        match key:
            case 'name':
                return [value]

            case 'not':
                return []

            case 'extension':
                return traverse_extensions(value)

            case 'anyOf' | 'oneOf':
                return [item for sublist in map(traverse_extensions, value) for item in sublist]

            case 'allOf':
                if any('xlen' in d for d in value):
                    index = next((i for i, d in enumerate(value) if 'xlen' in d))
                    xlen = value[index]['xlen']
                    res = traverse_extensions({key: [d for d in value if 'xlen' not in d]})
                    return list(map(lambda x: f"{x} (RV{xlen})", res))

                res = [item for sublist in map(traverse_extensions, value) for item in sublist]
                return ['_'.join(res)]

            case _:
                raise Exception(f"unknown key {key}")

    return traverse_extensions(inst['definedBy'])

def compute_extension_dependencies(exts):
    deps = {e['name']: [] for e in exts}
    for e in exts:
        implications = extensions_implied_by(e)
        for e2 in implications:
            deps[e2].append(e['name'])
    return deps

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "yamls",
        nargs="*",
        help="Extensions and instructions to include",
    )

    args = parser.parse_args()

    db = build_database(args.yamls)

    for inst in db['instruction'].values():
        print(inst['name'] + " " + str(extensions_defined_in(inst)))

    for ext in db['extension'].values():
        print(ext['name'] + " " + str(extensions_implied_by(ext)))

    ext_deps = compute_extension_dependencies(db['extension'].values())
    print(ext_deps)

    #print(extensions_implied_by(db['extension']['Zca']))
    #print(extensions_implied_by(db['extension']['C']))
    #print(extensions_dependent_on('Zca', db['extension']))

if __name__ == "__main__":
    main()
