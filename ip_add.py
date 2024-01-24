import pandas as pd
from tabulate import tabulate

class Address:
    def __init__(self, o1, o2, o3, o4):
        self.o1 = o1
        self.o2 = o2
        self.o3 = o3
        self.o4 = o4

class Mask:
    def __init__(self, n1, n2, n3, n4):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4

class Octet:
    def __init__(self, num_of_host, prefix, delta, sub_mask):
        self.num_of_host = num_of_host
        self.prefix = prefix
        self.delta = delta
        self.sub_mask = sub_mask

def main():
    ip_add = Address(93, 78, 145, 62)
    prefix = 18
    noh = [131, 4144, 29, 268, 1098, 2072, 253, 525, 8090, 2088, 63, 722, 1027, 332, 5078, 178, 111, 1927, 192, 3]

    # Sort the list of hosts in descending order
    noh.sort(reverse=True)

    # Define constants
    FILENAME_ALL = "table_all.txt"
    FILENAME_EXCLUDED = "table_excluded.txt"

    # File handling
    table_all = pd.DataFrame(columns=["GIVEN", "PREFIX", "DELTA", "IP ADDRESS", "BRC ADDRESS", "SUBNET", "NOUHA", "NOWA", "WCM"])
    table_excluded = pd.DataFrame(columns=["GIVEN", "PREFIX", "DELTA", "IP ADDRESS", "SUBNET"])

    # Octet information
    oc = [
        # 4th Octet
        Octet(2, 30, 4, Mask(255, 255, 255, 252)),
        Octet(6, 29, 8, Mask(255, 255, 255, 248)),
        Octet(14, 28, 16, Mask(255, 255, 255, 240)),
        Octet(30, 27, 32, Mask(255, 255, 255, 224)),
        Octet(62, 26, 64, Mask(255, 255, 255, 192)),
        Octet(126, 25, 128, Mask(255, 255, 255, 128)),
        Octet(254, 24, 1, Mask(255, 255, 255, 0)),
        # 3rd Octet
        Octet(510, 23, 2, Mask(255, 255, 254, 0)),
        Octet(1022, 22, 4, Mask(255, 255, 252, 0)),
        Octet(2046, 21, 8, Mask(255, 255, 248, 0)),
        Octet(4094, 20, 16, Mask(255, 255, 240, 0)),
        Octet(8190, 19, 32, Mask(255, 255, 224, 0)),
        Octet(16382, 18, 64, Mask(255, 255, 192, 0)),
        Octet(32766, 17, 128, Mask(255, 255, 128, 0)),
        Octet(65534, 16, 1, Mask(255, 255, 0, 0)),
        # 2nd Octet
        Octet(131070, 15, 2, Mask(255, 254, 0, 0)),
        Octet(262142, 14, 4, Mask(255, 252, 0, 0)),
        Octet(524286, 13, 8, Mask(255, 248, 0, 0)),
        Octet(1048574, 12, 16, Mask(255, 240, 0, 0)),
        Octet(2097150, 11, 32, Mask(255, 224, 0, 0)),
        Octet(4194302, 10, 64, Mask(255, 192, 0, 0)),
        Octet(8388606, 9, 128, Mask(255, 128, 0, 0)),
        Octet(16777214, 8, 1, Mask(255, 0, 0, 0)),
        # 1st Octet
        Octet(33554430, 7, 2, Mask(254, 0, 0, 0)),
        Octet(67108862, 6, 4, Mask(252, 0, 0, 0)),
        Octet(134217726, 5, 8, Mask(248, 0, 0, 0)),
        Octet(268435454, 4, 16, Mask(240, 0, 0, 0)),
        Octet(536870910, 3, 32, Mask(224, 0, 0, 0)),
        Octet(1073741822, 2, 64, Mask(192, 0, 0, 0)),
        Octet(2147483646, 1, 128, Mask(128, 0, 0, 0)),
    ]


    # Find prefix and retrieve subnet mask
    for o in oc:
        if o.prefix == prefix:
            subnet = o.sub_mask
            break
    else:
        print("Prefix not found.")
        return

    print(f"IP ADD: {ip_add.o1}.{ip_add.o2}.{ip_add.o3}.{ip_add.o4}/{prefix}")
    print(f"SUBNET MASK: {subnet.n1}.{subnet.n2}.{subnet.n3}.{subnet.n4}")

    # Network
    new_ip = Address(ip_add.o1 & subnet.n1, ip_add.o2 & subnet.n2, ip_add.o3 & subnet.n3, ip_add.o4 & subnet.n4)
    print(f"NETWORK: {new_ip.o1}.{new_ip.o2}.{new_ip.o3}.{new_ip.o4}\n")

    # Print and write data for each host
    print("TABLE_ALL:")
    for host in noh:
        for o in oc:
            if o.num_of_host >= host:
                new_ip = Address(ip_add.o1 & o.sub_mask.n1, ip_add.o2 & o.sub_mask.n2, ip_add.o3 & o.sub_mask.n3, ip_add.o4 & o.sub_mask.n4)
                br_add = Address(new_ip.o1, new_ip.o2, new_ip.o3, new_ip.o4 - 1 if o.sub_mask.n4 != 0 else 255)
                subnet = o.sub_mask

                # Append for FILENAME_ALL
                table_all = table_all._append({
                    "GIVEN": host,
                    "PREFIX": o.prefix,
                    "DELTA": o.delta,
                    "IP ADDRESS": f"{new_ip.o1}.{new_ip.o2}.{new_ip.o3}.{new_ip.o4}",
                    "BRC ADDRESS": f"{br_add.o1}.{br_add.o2}.{br_add.o3}.{br_add.o4}",
                    "SUBNET": f"{subnet.n1}.{subnet.n2}.{subnet.n3}.{subnet.n4}",
                    "NOUHA": o.num_of_host,
                    "NOWA": o.num_of_host - host,
                    "WCM": f"{255 - subnet.n1}.{255 - subnet.n2}.{255 - subnet.n3}.{255 - subnet.n4}"
                }, ignore_index=True)

                # Append for FILENAME_EXCLUDED
                table_excluded = table_excluded._append({
                    "GIVEN": host,
                    "PREFIX": o.prefix,
                    "DELTA": o.delta,
                    "IP ADDRESS": f"{new_ip.o1}.{new_ip.o2}.{new_ip.o3}.{new_ip.o4}",
                    "SUBNET": f"{subnet.n1}.{subnet.n2}.{subnet.n3}.{subnet.n4}",
                }, ignore_index=True)
                break

    print(tabulate(table_all, headers='keys', tablefmt='fancy_grid', showindex=False))
    print("\n")

    # Write DataFrame to CSV file
    table_all.to_csv(FILENAME_ALL, index=False, sep='\t')
    table_excluded.to_csv(FILENAME_EXCLUDED, index=False, sep='\t')

if __name__ == "__main__":
    main()
