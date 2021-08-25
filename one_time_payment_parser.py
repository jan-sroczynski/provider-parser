import json
import requests

BEARER_TOKEN = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjQzMzQwYzg3LWNhZjItNDg5ZS1hMzk0LTk3MWE3MzRkMTBmMSIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Mjk4ODIwNDEsImlhdCI6MTYyOTg4MDI0MSwiaXNzIjoidGluazovL2F1dGgiLCJqdGkiOiI1NTg0ZTJlYS04MmVhLTQ3MzUtOTUzNi02MTdkYzNkNmM5ZDEiLCJzY29wZXMiOlsicHJvdmlkZXJzOnJlYWQiLCJsaW5rLXNlc3Npb246cmVhZCIsInBheW1lbnQ6d3JpdGUiLCJ0cmFuc2ZlcjpleGVjdXRlIiwiYXV0aG9yaXphdGlvbjpncmFudCIsImxpbmstc2Vzc2lvbjp3cml0ZSIsInBheW1lbnQ6cmVhZCIsInRyYW5zZmVyOnJlYWQiXSwic3ViIjoidGluazovL2F1dGgvY2xpZW50LzdjZWU3NjJlMDBiYjQ5ZmQ5MmJkYWEwM2NjNWJjM2E5IiwidGluazovL2FwcC9pZCI6ImU0NGMxM2Q0MTRmODRlNDQ5ZTNmOTY0MTFlMzE0YWMwIiwidGluazovL2FwcC92ZXJpZmllZCI6ImZhbHNlIn0.PN3xvDwyfMHVbAyTahftCZ9dUVKh-wN5ONCVwXUB0WQmdilZjjSatZlKO3rw4TJKyZCE35fSliJt8uttYZqsEg'
HEADERS = {'Authorization': f'Bearer {BEARER_TOKEN}'}

RULES_DICT = {
  "REMITTANCE_INFORMATION_TYPE": 0,
  "REMITTANCE_INFORMATION_VALUE": 1,
  "REFERENCE_REMITTANCE_INFORMATION_VALUE": 2,
  "UNSTRUCTURED_REMITTANCE_INFORMATION_VALUE": 3,
  "GIRO_UNSTRUCTURED_REMITTANCE_INFORMATION_VALUE": 4,
  "INTRA_BANK_TRANSFER_CUTOFF_TIME": 5,
  "INTER_BANK_TRANSFER_CUTOFF_TIME": 6,
  "GIRO_CUTOFF_TIME": 7,
  "SOURCE_MESSAGE": 8,
  "RECIPIENT_NAME_VALUE": 9,
  "SOURCE_ACCOUNT_REQUIRED_BEFORE_REDIRECT": 10,
  "HAS_DOUBLE_REDIRECT": 11,
}

provider_list = json.load(open('providers.json'))['providers']


def parse_rule(a_rule):
  operator = a_rule.get('operator')
  value = a_rule.get('value')
  if isinstance(value, list):
    return f"{operator}: {', '.join(value)}"
  return f'{operator}: {value}'


def add_to_index(table, ind, value):
  if table[ind] == '':
    table[ind] = value
  else:
    table[ind] += f'| {value}'


csv_file = open('out.csv', 'w')
all_rules = []
for provider in provider_list:
  print(provider)
  url = f'https://api.staging.oxford.tink.com/api/v1/payments/providers/{provider}/payment-conditions'

  request = requests.get(url, headers=HEADERS)
  rules_list = ['' for _ in range(len(RULES_DICT))]
  if request is not None and request.status_code == 200:
    rules = request.json().get('conditions')
    for rule in rules:
      rule_name = rule.get('rule')
      index = RULES_DICT[rule_name]
      add_to_index(rules_list, index, parse_rule(rule))
  all_rules.append(rules_list)
  rules_list.insert(0, provider)
  csv_file.write('; '.join(rules_list))
  csv_file.write('\n')
