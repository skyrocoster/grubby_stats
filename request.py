import requests

open_dota = "https://api.opendota.com/api"

# unparsed = [
#     "6716802570",
#     "6718329621",
#     "6722993185",
#     "6736044582",
#     "6732892968",
#     "6734464068",
#     "6734538586",
#     "6723027063",
#     "6727799177",
#     "6716855691",
#     "6732691359",
#     "6729701542",
#     "6718501548",
#     "6732960432",
#     "6718242738",
#     "6722855866",
#     "6716894964",
#     "6729748219",
# ]

# for i in unparsed:
#     x = requests.post(f"{open_dota}/request/{i}")
#     print(x.text)

x = requests.get(f"{open_dota}/constants")
print(x.text)
