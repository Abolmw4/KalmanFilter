import requests

ADRESS = "http://127.0.0.1:8000"

def main():
    all_data = [{"Id": 1, "radar_info":{"X": 150,"Y": 250,"V_X": 25, "V_Y": 35}}, {"Id": 2, "radar_info":{"X": 250,"Y": 350,"V_X": 35, "V_Y": 45}},
                {"Id": 3, "radar_info":{"X": 250, "Y": 250, "V_X": 25, "V_Y": 35}}, {"Id": 4, "radar_info":{"X": 76, "Y": 111, "V_X": 54, "V_Y": 85}}]
    for item in all_data:
        result = requests.post(ADRESS+"/save", json=item)
        print(result.status_code, result.text)
    print("**********************")
    result = requests.get(ADRESS+"/dbinfo")
    print(result.status_code, result.text)
    result = requests.get(ADRESS+"/estimate/2")
    print("********************")
    print(result.status_code, result.text)

if __name__ == "__main__":
    main()