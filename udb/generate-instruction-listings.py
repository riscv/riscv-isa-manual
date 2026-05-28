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
    if 'definedBy' not in inst:
        raise Exception(f"{inst['name']} missing 'definedBy' key")

    def helper(x):
        if len(x) != 1:
            raise Exception(f"{inst['name']} has malformed 'definedBy' key")
        key = next(iter(x))
        value = x[key]
        match key:
            case 'extension':
                return value
            case 'anyOf':
                return map(helper, value)
            case 'allOf':
                if len(value) == 2 and 'xlen' in value and 'extension' in value:
                    return f"{value['extension']} (RV{value['xlen']})"
                print(inst['definedBy'])
                raise value
            case _:
                raise Exception(f"{inst['name']} has unknown 'definedBy' key {key}")

    helper(inst['definedBy'])

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
        extensions_defined_in(inst)

if __name__ == "__main__":
    main()
