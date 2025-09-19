from utils.util import recieve_messege_from_kafka


for mes in recieve_messege_from_kafka("row-track"):
    print(mes)