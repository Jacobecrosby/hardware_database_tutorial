from modules.db_utils import authenticate_user_itkdb
from modules.reception_module import enter_serial_numbers,get_comp_info
import datetime

def update_test_type_tutorial(client,meta_data,test_type):
    component = client.get("getComponent", json={"component": meta_data["serialNumber"]})  
    
    if component["currentStage"]["code"] != test_type:
      print("Updating component stage to", test_type)
      set_stage = {
        "component": meta_data["serialNumber"],
        "stage": test_type,
        "rework": False,
        "comment": "updated stage to connectivity on "+str(datetime.datetime),
        "history": True
      }
      client.post("setComponentStage",json=set_stage)
      print("Stage updated!")

    

def main():
    itkdb_client = authenticate_user_itkdb()
    single = True
    serial_number = enter_serial_numbers(single)
    meta_data = get_comp_info(itkdb_client,serial_number)
    slac_options = ["SHIPPING_TO_SLAC","RECEPTION_SLAC"]
    print("\nChoose which SLAC stage to update to:")
    for k, v in enumerate(slac_options):
        print(f"For {v}, press {k}")
    while True:
        try:
            selection = input("\nInput Selection: ")
            option = slac_options[int(selection)]
            break
        except (ValueError, IndexError):
            print("Invalid Input. Try again.")
    print(f"Selected {option}\n")
    update_test_type_tutorial(itkdb_client,meta_data,option)
    

    

if __name__ == '__main__':
  main()