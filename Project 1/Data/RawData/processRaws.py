import json

# This only ever needs to run once. To process the 
def main():
    startfile = "graphic_novels_raw.json"
    endfile = "../graphic_novels.json"
    f = open(startfile, 'r')
    data = dict()
    for line in f:
        d = json.loads(line)
        key = d["book_id"]
        value = d["title"]
        data[key] = value
    f.close()

    f = open(endfile, 'w')
    json.dump(data, f)
    f.close()


main()
