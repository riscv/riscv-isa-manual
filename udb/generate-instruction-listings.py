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

def extensions_defined_in(inst):
    def helper(x):
        key = next(iter(x))
        value = x[key]
        match key:
            case 'name':
                return [value]
            case 'extension':
                return helper(value)
            case 'anyOf' | 'oneOf':
                return [item for sublist in map(helper, value) for item in sublist]
            case 'allOf':
                value = {k: v for d in x[key] for k, v in d.items()}
                if len(value) == 2 and 'xlen' in value and 'extension' in value:
                    res = helper(value['extension'])
                    return list(map(lambda x: f"{x} (RV{value['xlen']})", res))
                if len(value) == 2 and 'not' in value and 'name' in value:
                    return helper(value)
                if len(value) == 1 and 'name' in value:
                    return helper(value)
                raise Exception(f"{inst['name']} has unrecognized 'allOf' pattern {value}")
            case _:
                raise Exception(f"{inst['name']} has unknown 'definedBy' key {key}")

    return helper(inst['definedBy'])

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

if __name__ == "__main__":
    main()
