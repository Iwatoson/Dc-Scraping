import json

with open("TraditionalColors_scrapy.json", "r") as file:
    colors = json.load(file)
    for index, color in enumerate(colors):
        want_parse_string: str = color["description"]
        ads_id = want_parse_string.find("(ads")
        delete_ads_string: str = want_parse_string
        if ads_id >= 0:
            delete_ads_string: str = want_parse_string[:ads_id]

        other_id = delete_ads_string.rfind("色見本")
        delete_other_string: str = delete_ads_string
        if other_id >= 0:
            delete_other_string: str = delete_ads_string[: other_id + len("色見本")]

        colors[index]["description"] = delete_other_string

    json.dump(
        colors,
        open("TraditionalColors_exact_description.json", "w"),
        ensure_ascii=False,
        indent=2,
    )
