
class BySubnet:
    def __init__(self, ip_address, mask):
        #inputs
        number_of_subnets = int(input("ENTER NUMBER OF SUBNETS: "))
        
        #step 1
        decremented_subnets = number_of_subnets - 1 
        binary_equi = self.decimal_to_bin(decremented_subnets) 
        additional_bits = len(binary_equi)

        print(f"{number_of_subnets} - 1 = {decremented_subnets} -> {binary_equi}")

        #step 2
        original_mask = self.masking(mask)
        new_mask = self.masking(mask, additional_bits)

        print(f"ORIGINAL SUBNET MASK:   {original_mask} -> {self.convert_mask(original_mask)}")
        print(f"NEW SUBNET MASK:        {new_mask} -> {self.convert_mask(new_mask)}")

        #step 3
        octet, increment_value = self.get_increment_value(new_mask)
        print(f"INCREMENT VALUE: {increment_value}")

        #step 4
        network_addresses = self.get_network_address(ip_address, increment_value, octet)
        broadcast_addresses = self.get_broadcast_address(network_addresses, increment_value, octet)
        usable_ips = self.get_usable_ips(network_addresses, broadcast_addresses)
        
        print(f"N.A                             USABLE IPs                 B.A")
        for na, ui, ba in zip(network_addresses, usable_ips, broadcast_addresses):
            print(f"{na}{(20 - len(na)) * ' '}{ui[0]}{(16 - len(ui[0])) * ' '}-> {ui[1]}{(20 - (len(ui[1])) ) * ' '}{ba}")
            

    def decimal_to_bin(self, number) -> str:
        return bin(number).replace("0b", '')
    

    def masking(self, mask, additional_bits=0) -> str:
        bit_mask = []
        counter = 1
        mask += additional_bits

        for i in range(32):
            if i < mask:
                bit_mask.append('1')    
            else:
                bit_mask.append('0')
            
            if (i + 1) % 8 == 0 and i != 31:
                bit_mask.append('.')

            counter += 1

        return ''.join(bit_mask)


    def convert_mask(self, bit_mask) -> str:
        bit_mask = bit_mask.split('.')
        convert_mask = []
        for _ in bit_mask:
            convert_mask.append(str(int(_, 2)))
        
        return '.'.join(convert_mask)


    def get_increment_value(self, mask) -> list:
        mask = mask.split('.')

        for i, _ in enumerate(mask):
            if ('0' in _ and '1' in _) or mask[i+1] == "00000000":
                octet = i
                break 
        
        bits = list(mask[octet])
        bits.reverse()
        increment = []
        for bit in bits:
            increment.append(int(bit))

            if bit == '1':
                break

        increment.reverse()

        increment_value = [octet, int(''.join(map(str, increment)), 2)]

        return increment_value


    def get_network_address(self, network_address, increment_value, octet) -> list:
        address = network_address.split('.')
        address = list(map(int, address))

        network_addresses = []
        for _ in range(5):  # Adjust the range as needed
            network_addresses.append('.'.join(map(str, address)))
            address[octet - 4] += increment_value
            for i in range(3, -1, -1):
                if address[i] >= 256:
                    address[i] = 0
                    if i > 0:
                        address[i - 1] += 1

        return network_addresses


    def get_broadcast_address(self, network_addresses, increment_value, octet) -> list:
        broadcast_addresses = []

        for item in network_addresses:
            network_address = item.split('.')
            network_address = [int(o) for o in network_address]

            network_address[octet] += increment_value - 1

            for i in range(3, -1, -1):
                if network_address[i] >= 256:
                    if i > 0:
                        network_address[i - 1] += network_address[i] // 256
                    network_address[i] %= 256

            for i in range(octet + 1, 4):
                network_address[i] = 255

            broadcast_addresses.append('.'.join(map(str, network_address)))

        return broadcast_addresses

    def get_usable_ips(self, network_addresses, broadcast_addresses) -> list:
        usable_ips = []


        for item in zip(network_addresses, broadcast_addresses):
            first_usable_ip = item[0].split('.')
            first_usable_ip = list(map(int, first_usable_ip))
            first_usable_ip[3] += 1

            last_usable_ip = item[1].split('.')
            last_usable_ip = list(map(int, last_usable_ip))
            last_usable_ip[3] -= 1

            usable_ips.append(['.'.join(map(str, first_usable_ip)), '.'.join(map(str,last_usable_ip))])
        
        return usable_ips


class ByHost:
    def __init__(self, ip_address, mask):
    #inputs
        number_of_hosts = int(input("ENTER NUMBER OF HOSTS: "))
        
        #step 1
        binary_equi = self.decimal_to_bin(number_of_hosts) 
        additional_bits = len(binary_equi)

        print(f"{number_of_hosts} -> {binary_equi}")

        #step 2
        original_mask = self.masking(mask)
        new_mask = self.masking(mask, additional_bits)

        print(f"ORIGINAL SUBNET MASK:   {original_mask} -> {self.convert_mask(original_mask)}")
        print(f"NEW SUBNET MASK:        {new_mask} -> {self.convert_mask(new_mask)}")

        #step 3
        octet, increment_value = self.get_increment_value(new_mask)
        print(f"INCREMENT VALUE: {increment_value}")

        #step 4
        network_addresses = self.get_network_address(ip_address, increment_value, octet)
        broadcast_addresses = self.get_broadcast_address(network_addresses, increment_value, octet)
        usable_ips = self.get_usable_ips(network_addresses, broadcast_addresses)
        
        print(f"N.A                             USABLE IPs                 B.A")
        for na, ui, ba in zip(network_addresses, usable_ips, broadcast_addresses):
            print(f"{na}{(20 - len(na)) * ' '}{ui[0]}{(16 - len(ui[0])) * ' '}-> {ui[1]}{(20 - (len(ui[1])) ) * ' '}{ba}")
            


    def decimal_to_bin(self,number) -> str:
        return bin(number).replace("0b", '')


    def masking(self,mask, additional_bits=0) -> str:
        bit_mask = []
        counter = 1
        mask += abs((32 - additional_bits) - mask) if additional_bits > 0 else additional_bits

        for i in range(32):
            if i < mask:
                bit_mask.append('1')    
            else:
                bit_mask.append('0')
            
            if (i + 1) % 8 == 0 and i != 31:
                bit_mask.append('.')

            counter += 1

        return ''.join(bit_mask)


    def convert_mask(self,bit_mask) -> str:
        bit_mask = bit_mask.split('.')
        convert_mask = []
        for _ in bit_mask:
            convert_mask.append(str(int(_, 2)))
        
        return '.'.join(convert_mask)


    def get_increment_value(self,mask) -> list:
        mask = mask.split('.')

        for i, _ in enumerate(mask):
            if ('0' in _ and '1' in _) or mask[i+1] == "00000000":
                octet = i
                break 
        
        bits = list(mask[octet])
        bits.reverse()
        increment = []
        for bit in bits:
            increment.append(int(bit))

            if bit == '1':
                break

        increment.reverse()

        increment_value = [octet, int(''.join(map(str, increment)), 2)]

        return increment_value


    def get_network_address(self,network_address, increment_value, octet) -> list:
        address = network_address.split('.')
        address = list(map(int, address))

        network_addresses = []
        for _ in range(5):  # Adjust the range as needed
            network_addresses.append('.'.join(map(str, address)))
            address[octet - 4] += increment_value
            for i in range(3, -1, -1):
                if address[i] >= 256:
                    address[i] = 0
                    if i > 0:
                        address[i - 1] += 1

        return network_addresses


    def get_broadcast_address(self,network_addresses, increment_value, octet) -> list:
        broadcast_addresses = []

        for item in network_addresses:
            network_address = item.split('.')
            network_address = [int(o) for o in network_address]

            network_address[octet] += increment_value - 1

            for i in range(3, -1, -1):
                if network_address[i] >= 256:
                    if i > 0:
                        network_address[i - 1] += network_address[i] // 256
                    network_address[i] %= 256

            for i in range(octet + 1, 4):
                network_address[i] = 255

            broadcast_addresses.append('.'.join(map(str, network_address)))

        return broadcast_addresses

    def get_usable_ips(self,network_addresses, broadcast_addresses) -> list:
        usable_ips = []


        for item in zip(network_addresses, broadcast_addresses):
            first_usable_ip = item[0].split('.')
            first_usable_ip = list(map(int, first_usable_ip))
            first_usable_ip[3] += 1

            last_usable_ip = item[1].split('.')
            last_usable_ip = list(map(int, last_usable_ip))
            last_usable_ip[3] -= 1

            usable_ips.append(['.'.join(map(str, first_usable_ip)), '.'.join(map(str,last_usable_ip))])
        
        return usable_ips