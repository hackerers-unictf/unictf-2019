#!/usr/bin/python3
import binascii
import csv
import hashlib
import sys

def s256(msg):
    # string hex sha256 of a string or hex string message
    try:
        return hashlib.sha256(binascii.unhexlify(msg)).hexdigest()
    except:
        return hashlib.sha256(msg.encode('utf-8')).hexdigest()


def kth_bit(n, k):
    # flag of the kth bit
    # e.g. k(8,1) == 0; k(8,3) == 1
    return 1 if n & (1 << (k)) else 0


def group_by_n(s, n=2):
    # takes a list or tuple and chunks it up into pairs or other n
    # e.g. (1,2,3,4,5,6) -> ((1,2),(3,4),(5,6))
    return [s[i:i + n] for i in range(0, len(s), n)]


def bit_stream_from_msg(msg):
    # given a hex string msg, generate a stream of 1 and 0
    # e.g. 'e8' -> (0,0,0,1,0,1,1,1)
    newmsg = int(msg, 16)
    for i in range(4 * len(msg))[::-1]:
        yield kth_bit(newmsg, i)


def make_top_hash_from_leaves(tree):
    # combine an ordered list key pairs to a top level public key.
    if len(tree) < 2:
        return tree[0]
    else:
        return make_top_hash_from_leaves(
            [s256(a + b) for a, b in group_by_n(tree)]
        )


def make_top_hash_from_others(initial, others):
    # traverse asymmetic segments of public key signature to get public key
    top_hash = initial
    for rank, other in others:
        if int(rank):
            top_hash = s256(other + top_hash)
        else:
            top_hash = s256(top_hash + other)
    return top_hash


def msg_to_hashes(msg, signature):
    # turn a message with signature into an ordered list of key pairs
    bit_stream = bit_stream_from_msg(msg)
    sign_stream = group_by_n(signature, 2)
    return_stream = []
    for bit, sign in zip(bit_stream, sign_stream):
        if bit:
            return_stream.append(sign[0])
            return_stream.append(s256(sign[1]))
        else:
            return_stream.append(s256(sign[0]))
            return_stream.append(sign[1])
    return return_stream

def msg_internal_validity(msg, identity):
    # test zuccoin transaction message validity
    msg_list = msg.split(' ')
    return msg_list[0] == identity and \
        msg_list[1] == 'sent' and \
        float(msg_list[2]) < 500 and \
        msg_list[3] == 'zuccoins' and \
        msg_list[4] == 'to' and \
        len(msg_list[5]) == 64 and \
        len(msg_list) == 6

def parse_signed_message(msg_w_signature):
    # separate a formatted message and signature into components
    if (len(msg_w_signature) >= 524) and ((len(msg_w_signature)%2) == 0):
        top_identity = msg_w_signature[0]
        if len(top_identity) == 64:
            msg = msg_w_signature[1]
            if msg_internal_validity(msg, top_identity) == True:
                h_msg = s256(msg)
                signature = msg_w_signature[2:514]
                others = group_by_n(msg_w_signature[514:])
                for other in others:
                    if int(other[0]) == 0 or int(other[0]) == 1:
                        return (top_identity, h_msg, signature, others)
    print("Failed to parse message, make sure you have inserted the right")
    print("colums needed; copy and paste may not work, try to pipe directly")
    return (False, False, False, False)

def verify_signed_message(msg_w_signature):
    # return the public key used to sign a message
    identity, h_msg, signature, others = parse_signed_message(msg_w_signature)
    if identity == False or h_msg == False or others == False:
        return (False, True)
    initial = make_top_hash_from_leaves(msg_to_hashes(h_msg, signature))
    top = make_top_hash_from_others(initial, others)
    return (identity, top)

def read_identities(filename):
    known_identities = set()
    with open(filename, 'r') as infile:
        for row in infile:
            known_identities.add(row[:-1])
    known_identities = list(known_identities)
    return known_identities

def is_known_identity(identity, identities):
    if identity in identities:
        print(identity + " This is a known identity")
        sys.stdout.flush()
        return True
    return False

def save_signature(signature):
    with open('new_signatures.csv', 'a') as fd:
        fd.write(signature + '\n')
        fd.close()

def is_known_signature(signature):
    with open('new_signatures.csv', 'r') as fd:
        incsv = csv.reader(fd)
        for row in incsv:
            str_row = "".join(row)
            if str_row == signature:
                return True
    return False

def read_record():
    print("Insert your signature in csv form: ")
    sys.stdout.flush()
    signature = str(sys.stdin.readline())
    signature = signature.split(",");
    signature[len(signature)-1] = "".join(signature[len(signature)-1].splitlines())
    print("Received Signature:")
    print("\n".join(signature))
    print("Signature length: " + str(len(signature)))
    return signature;

def calc_signature(filename):
    known_identities = read_identities(filename)
    signature = read_record()
    if not is_known_identity(signature[0], known_identities):
        a, b = verify_signed_message(signature)
        if (a == b):
            print('good signature')
            if is_known_signature(",".join(signature)):
                print('This signature is good but already used')
                sys.stdout.flush()
                return
            save_signature(",".join(signature))
            sys.stdout.flush()
            with open('flag') as fd:
                for row in fd:
                    print(row)
                    sys.stdout.flush()
        else:
            print('bad signature {}')
            sys.stdout.flush()


def main():
    filename = 'identities'
    calc_signature(filename)

if __name__ == '__main__':
    main()
