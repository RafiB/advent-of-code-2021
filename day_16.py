HEX_TO_BIN = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

def hex_to_bin(hex_str):
    res = ""
    for c in hex_str:
        res += HEX_TO_BIN[c]
    return res


class Phase(object):
    PACKET = 1
    OPERATOR = 2
    NUMBERS = 3


def parse(remaining, single=False, i=0):
    # print(i*" ", "read", remaining, single)
    phase = Phase.PACKET

    answer = 0

    if not remaining:
        return answer, remaining

    while remaining:
        if all(c == "0" for c in remaining):
            break
        if phase == Phase.PACKET:
            packet_version, remaining = remaining[:3], remaining[3:]
            packet_version_int = 0
            for b in packet_version:
                packet_version_int = (packet_version_int << 1) + int(b)
            answer += packet_version_int

            packet_type_id, remaining = remaining[:3], remaining[3:]
            packet_type_id_int = 0
            for b in packet_type_id:
                packet_type_id_int = (packet_type_id_int << 1) + int(b)
            # print(i*" ", "new packet", packet_version_int, packet_type_id_int)
            if packet_type_id_int == 4:
                # print(i*" ", "literal")
                literal = 0
                while remaining[0] == "1":
                    bits, remaining = remaining[1:5], remaining[5:]
                    for b in bits:
                        literal = (literal << 1) + int(b)
                assert remaining[0] == "0"
                bits, remaining = remaining[1:5], remaining[5:]
                for b in bits:
                    literal = (literal << 1) + int(b)
                # print(i*" ", "is literal", literal)
                if single:
                    # print(i*" ", "answer", answer)
                    return answer, remaining
                phase = Phase.PACKET
            else:
                phase = Phase.OPERATOR
        elif phase == Phase.OPERATOR:
            # print(i*" ", "operator version", packet_version_int)
            length_type_id, remaining = remaining[0], remaining[1:]
            if length_type_id == "0":
                # print(i*" ", "op 0")
                length_in_bin, remaining = remaining[:15], remaining[15:]
                length = 0
                for b in length_in_bin:
                    length = (length << 1) + int(b)
                # print(i*" ", "15 bits", length_in_bin, length)

                sub_answer, _ = parse(remaining[:length], i=i+2)
                answer += sub_answer
                remaining = remaining[length:]
                # print(i*" ", "finished", length, remaining)

                if single:
                    # print(i*" ", "answer", answer)
                    return answer, remaining
                phase = Phase.PACKET
            else:
                # print(i*" ", "op 1")
                num_packets_in_bin, remaining = remaining[:11], remaining[11:]
                num_packets = 0
                for b in num_packets_in_bin:
                    num_packets = (num_packets << 1) + int(b)
                # print(i*" ", "11 bits", num_packets_in_bin, "read", num_packets, "packet")

                for _ in range(num_packets):
                    sub_answer, remaining = parse(remaining, single=True, i=i+2)
                    answer += sub_answer

                if single:
                    # print(i*" ", "answer", answer)
                    return answer, remaining
                phase = Phase.PACKET

        else:
            raise NotImplementedError()

    # print(i*" ", "answer", answer)
    return answer, remaining


def solve(hex_str):
    return parse(hex_to_bin(hex_str))[0]


def tests():
    assert hex_to_bin("D2FE28") == "110100101111111000101000"
    assert solve("8A004A801A8002F478") == 16
    assert solve("620080001611562C8802118E34") == 12
    assert solve("C0015000016115A2E0802F182340") == 23
    assert solve("A0016C880162017C3686B18A3D4780") == 31


if __name__ == "__main__":
    tests()
    print(solve("A059141803C0008447E897180401F82F1E60D80021D11A3DC3F300470015786935BED80A5DB5002F69B4298A60FE73BE41968F48080328D00427BCD339CC7F431253838CCEFF4A943803D251B924EC283F16D400C9CDB3180213D2D542EC01092D77381A98DA89801D241705C80180960E93469801400F0A6CEA7617318732B08C67DA48C27551C00F972830052800B08550A277416401A5C913D0043D2CD125AC4B1DB50E0802059552912E9676931530046C0141007E3D4698E20008744D89509677DBF5759F38CDC594401093FC67BACDCE66B3C87380553E7127B88ECACAD96D98F8AC9E570C015C00B8E4E33AD33632938CEB4CD8C67890C01083B800E5CBDAB2BDDF65814C01299D7E34842E85801224D52DF9824D52DF981C4630047401400042E144698B2200C4328731CA6F9CBCA5FBB798021259B7B3BBC912803879CD67F6F5F78BB9CD6A77D42F1223005B8037600042E25C158FE0008747E8F50B276116C9A2730046801F29BC854A6BF4C65F64EB58DF77C018009D640086C318870A0C01D88105A0B9803310E2045C8CF3F4E7D7880484D0040001098B51DA0980021F17A3047899585004E79CE4ABD503005E610271ED4018899234B64F64588C0129EEDFD2EFBA75E0084CC659AF3457317069A509B97FB3531003254D080557A00CC8401F8791DA13080391EA39C739EFEE5394920C01098C735D51B004A7A92F6A0953D497B504F200F2BC01792FE9D64BFA739584774847CE26006A801AC05DE180184053E280104049D10111CA006300E962005A801E2007B80182007200792E00420051E400EF980192DC8471E259245100967FF7E6F2CF25DBFA8593108D342939595454802D79550C0068A72F0DC52A7D68003E99C863D5BC7A411EA37C229A86EBBC0CB802B331FDBED13BAB92080310265296AFA1EDE8AA64A0C02C9D49966195609C0594223005B80152977996D69EE7BD9CE4C1803978A7392ACE71DA448914C527FFE140"))
