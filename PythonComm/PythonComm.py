
#add ads library for plc
import pyads

#ip address to connect plc
AMSNETID = "192.168.1.133.1.1"

#connection
plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)
plc.open()

#debugging statement, optional
print(f"Connected?: {plc.is_open}") 
print(f"Local Address? : {plc.get_local_address()}") 

#Enable PLC
getEnable=False
plc.write_by_name("GVL.stData.boEnable",True)
getEnable = plc.read_by_name("GVL.stData.boEnable")


setPos=0.0
setVelo=0.0
setAcc=0.0
setDec=0.0

getPos=0.0
getVelo=0.0
getAcc=0.0
getDec=0.0

setStart=False
getStart=False




#input motor values
def writeMotorValues():
    setPos = float(input("Enter Position:"))
    setVelo = float(input("Enter Velocity:"))
    setAcc  = float(input("Enter Acceleration:"))
    setDec  = float(input("Enter Deceleration:"))

    plc.write_by_name("GVL.stData.lrPosition",setPos)
    plc.write_by_name("GVL.stData.lrVelocity",setVelo)
    plc.write_by_name("GVL.stData.lrAcceleration",setAcc)
    plc.write_by_name("GVL.stData.lrDeceleration",setDec)

#get motor actual values
def readMotorValues():
    getPos=plc.read_by_name("GVL.stData.lrActualPos")
    getVelo=plc.read_by_name("GVL.stData.lrActualVelo")
    getAcc=plc.read_by_name("GVL.stData.lrActualAcc")

    print('Actual position:',getPos)
    print('Actual velocity:',getVelo)
    print('Actual acceleration:',getAcc)




#Start the motor control
while getEnable:
    if setStart==False:
        writeMotorValues()
        readMotorValues()
        setStart = bool(input("Enter Start:"))
    if setStart and not getStart:
        plc.write_by_name("GVL.stData.boStart",True)
        getStart=setStart

    movingDone = plc.read_by_name("MAIN.fbAbsolute.done")
    if  movingDone:
        setStart=False
        print('motor is done')
        plc.write_by_name("GVL.stData.boEnable",False)
        readMotorValues()
        plc.close()
        break



            




