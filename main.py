from subnetting import BySubnet, ByHost

def by_subnet(ip_address, mask):
    BySubnet(ip_address, mask)


def by_host(ip_address, mask):
    ByHost(ip_address, mask)

CHOICES = {
    1: by_subnet,
    2: by_host,
}

while True:
    print("MENU")
    print("[1] BY NUMBER OF SUBNETS")
    print("[2] BY NUMBER OF HOSTS")
    print("[3] EXIT")
    print("------------------")

    choice = int(input("ENTER YOUR CHOICE: "))

    if choice == 3:
        exit()

    ip_address = str(input("ENTER GIVEN IP ADDRESS: "))
    mask = int(input("ENTER SUBMASK (CIDR): "))

    if choice in CHOICES:
        CHOICES[choice](ip_address, mask)
    else:
        print("Invalid")

    