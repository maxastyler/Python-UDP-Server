from helpers import *

class Connection:
    def __init__(self):
        self.s_number=0
        self.rs_number=0
        self.ack_field=5
    def receive_data(self, data): 
        new_rs=int.from_bytes(data[0:4], BYTE_ORDER)
        self.ack_check(new_rs)
        
    def ack_check(self, new_rs):
        if check_higher(new_rs, self.rs_number):
            if new_rs<self.rs_number:
                ack_shift=new_rs+INT32_MAX+1-self.rs_number
            else:
                ack_shift=new_rs-self.rs_number
            if ack_shift>=ACK_FIELD_LENGTH:
                self.ack_field=0
            else:
                self.ack_field=(self.ack_field<<ack_shift)%(1<<ACK_FIELD_LENGTH)
            self.rs_number=new_rs
        else:
            if self.rs_number<new_rs:
                ack_point=self.rs_number+INT32_MAX+1-new_rs
            else:
                ack_point=self.rs_number-new_rs
            if ack_point>0 and ack_point<=ACK_FIELD_LENGTH:            
                self.ack_field |= 1<<(ack_point-1)

if __name__=='__main__':
    c=Connection()
