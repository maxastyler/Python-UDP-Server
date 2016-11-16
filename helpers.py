FNV_PRIME=16777619
FNV_OFFSET_BASIS=2166136261
INT32_MAX=int('ffffffff', 16)
HALF_MAX=INT32_MAX/2
PACKET_SIZE=64 #packet size in bytes
BYTE_ORDER="big" #use big endian bytes
ACK_FIELD_LENGTH=32
CONNECTION_TIME_OUT=10 #in seconds

def fnv1a(bytes_to_hash):
    hashed=FNV_OFFSET_BASIS
    for byte in bytes_to_hash:
        hashed^=byte
        hashed*=FNV_PRIME
        hashed&=0xffffffff
    return hashed.to_bytes(4, "big")

HEADER_NAME=fnv1a(b"Client Server Program")

#Int command strings
INT_COMMAND={}
INT_COMMAND['connect']=0x1
INT_COMMAND['data_packet']=0x2
INT_COMMAND['accept_connection']=0x3
INT_COMMAND['still_alive']=0x4

#4 byte command strings
BYTE_COMMAND={}
for key in INT_COMMAND:
    BYTE_COMMAND[key]=INT_COMMAND[key].to_bytes(4, BYTE_ORDER)

def check_higher(a, b):
    return ((a>b) and (a-b<=HALF_MAX)) or ((b>a) and (b-a>HALF_MAX))

def create_packet(data):
    return HEADER_NAME+data
