from wsimple.api import wsimple

#NOTES:
# - WS limits to approximately 7 trades per hour

def get_otp():
    return input("Enter otpnumber: \n>>>")

email = str(input("Enter email: \n>>>"))
password = str(input("Enter password: \n>>>"))

ws = Wsimple(email, password, otp_callback=get_otp)

# always check if wealthsimple is working (return True if working or an error)
if ws.is_operational(): 
  # check the current operation status of internal Wealthsimple Trade
  print(ws.current_status())

