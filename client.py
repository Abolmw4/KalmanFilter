import json

import requests

ADRESS = "http://127.0.0.1:8000"

def main():

    all_data = {"radars":[{"trackID": 1,'X': 123, 'Y':111, 'V_X':80, 'V_Y':88}, {'trackID':2, 'X': 223, 'Y':211, 'V_X':20, 'V_Y':82}]}
    result = requests.post(ADRESS+"/save", data=json.dumps(all_data))
    print(result.status_code, result.text)
    # data = {"trackID": 5,'X': 23, 'Y':112, 'V_X':54, 'V_Y':22}
    # result = requests.post(ADRESS + "/save", data=json.dumps(data))
    # print(result.status_code, result.text)
    result = requests.get(ADRESS+"/2")
    print(result.status_code, result.text)

    result = requests.get(ADRESS + "/result/2")
    print(result.status_code, result.text)


if __name__ == "__main__":
    main()