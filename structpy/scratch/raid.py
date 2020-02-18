

if __name__ == '__main__':

    disks = [
        [int(x) for x in "11110000"],
    [int(x) for x in "11111000"],
    [int(x) for x in "00111111"],
    [int(x) for x in "00000001"]
    ]

    def block(string):
        return [int(x) for x in string]

    def xor(l1, l2):
        result = []
        for i in range(len(l1)):
            result.append(l1[i] ^ l2[i])
        return result

    result = list(disks[0])
    for disk in disks[1:]:
        result = xor(result, disk)

    def new_parity(old_parity, new_data, old_data):
        return xor(old_parity, xor(new_data, old_data))

    print(new_parity(
        block('00110110'), block('10101010'), block('11110000'
                                                    '')
    ))