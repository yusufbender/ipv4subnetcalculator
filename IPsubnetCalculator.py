def subnet_calculator(ip_address, subnet_mask):
    # IP adresini ve alt ağı ayrıştırma
    ip_octets = ip_address.split('.')
    subnet_octets = subnet_mask.split('.')

    # IP adresi ve alt ağı binary formatına dönüştürme
    ip_binary = ''.join([bin(int(octet))[2:].zfill(8) for octet in ip_octets])
    subnet_binary = ''.join([bin(int(octet))[2:].zfill(8) for octet in subnet_octets])

    # Alt ağ ID'sini hesaplama
    network_address_binary = ''.join([str(int(ip_binary[i]) & int(subnet_binary[i])) for i in range(32)])
    network_address = '.'.join([str(int(network_address_binary[i:i+8], 2)) for i in range(0, 32, 8)])

    # Alt ağ yayın adresini hesaplama
    inverted_subnet_binary = ''.join(['1' if bit == '0' else '0' for bit in subnet_binary])
    broadcast_address_binary = ''.join([str(int(ip_binary[i]) | int(inverted_subnet_binary[i])) for i in range(32)])
    broadcast_address = '.'.join([str(int(broadcast_address_binary[i:i+8], 2)) for i in range(0, 32, 8)])

    # Kullanılabilir host sayısını hesaplama
    usable_hosts = 2 ** (32 - sum([bin(int(octet)).count('1') for octet in subnet_octets])) - 2

    # Kullanılabilir IP adres aralığını hesaplama
    first_usable_ip = network_address[:network_address.rfind('.')] + '.' + str(int(network_address.split('.')[-1]) + 1)
    last_usable_ip = broadcast_address[:broadcast_address.rfind('.')] + '.' + str(int(broadcast_address.split('.')[-1]) - 1)

    # CIDR notasyonunu hesaplama
    cidr_notation = sum([bin(int(octet)).count('1') for octet in subnet_octets])

    # Wildcard maskesini hesaplama
    wildcard_mask = '.'.join([str(255 - int(octet)) for octet in subnet_octets])

    return {
        "Network Address": network_address,
        "Broadcast Address": broadcast_address,
        "Usable Host IP Range": (first_usable_ip, last_usable_ip),
        "Total Hosts": 2**(32 - cidr_notation),
        "Usable Hosts": usable_hosts,
        "Binary Subnet Mask": subnet_mask,
        "Wildcard Mask": wildcard_mask,
        "CIDR Notation": f"/{cidr_notation}"
    }

# Kullanıcıdan IP adresi ve alt ağ maskesini al
ip_address = input("IP adresini girin (örnek: 192.168.1.1): ")
subnet_mask = input("Alt ağ maskesini girin (örnek: 255.255.255.0): ")

result = subnet_calculator(ip_address, subnet_mask)
for key, value in result.items():
    print(f"{key}: {value}")
