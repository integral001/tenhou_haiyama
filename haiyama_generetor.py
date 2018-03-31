import struct
import base64
from hashlib import sha512
import numpy as np

SIZE_OF_UINT32 = 4
SHA512_DIGEST_LENGTH = int(512 / 8 / SIZE_OF_UINT32)
RND_LENGTH = SHA512_DIGEST_LENGTH * 9 # = 144 > 136
SRC_LENGTH = RND_LENGTH * 2

mt = np.random.RandomState()

def b64seed_to_init(b64seed):
    """b64seed:str[3328?] -> init:u_int32[624]"""
    init_seed_byte = base64.b64decode(b64seed)
    init = struct.unpack("<624I", init_seed_byte)
    return init

def init_mt(init):
    """init:u_int32[624] -> ()"""
    mt.seed(init)

def mt_gen(size=SRC_LENGTH):
    """ () -> src:u_int32[SRC_LENGTH]"""
    src_byte = [mt.bytes(SIZE_OF_UINT32) for i in range(size)]
    src = [struct.unpack("<I", x)[0] for x in src_byte]
    return src

def src_to_rnd(src):
    """src:u_int32[SRC_LENGTH] -> rnd:u_int32[RND_LENGTH]"""
    rnd = []
    for i in range(int(RND_LENGTH / SHA512_DIGEST_LENGTH)):
        start = i * SHA512_DIGEST_LENGTH * 2
        stop = start + SHA512_DIGEST_LENGTH * 2
        input_src = struct.pack("<" + str(SHA512_DIGEST_LENGTH * 2) +"I", *src[start:stop])
        digest = sha512(input_src).digest()
        r_chunk = struct.unpack("<" + str(SHA512_DIGEST_LENGTH) + "I", digest)
        rnd += r_chunk
    return rnd

def rnd_to_yama(rnd):
    """rnd:u_int32[RND_LENGTH] -> yama:u_int32[136]"""
    yama = [i for i in range(136)]
    for i in range(136 - 1):
        suffle_index = i + rnd[i] % (136 - i)
        yama[i], yama[suffle_index] = yama[suffle_index], yama[i]
    return yama

def rnd_to_dice(rnd):
    """rnd:u_int32[RND_LENGTH] -> dice:u_int32[2]"""
    dice = [rnd[135] % 6 + 1, rnd[136] % 6 + 1]
    return dice

def disp_hai(yama):
    """yama:u_int32[136] -> hai:str[][136]"""
    hai_disp = ["<1m>", "<2m>", "<3m>", "<4m>", "<5m>", "<6m>", "<7m>", "<8m>", "<9m>",
               "<1p>", "<2p>", "<3p>", "<4p>", "<5p>", "<6p>", "<7p>", "<8p>", "<9p>",
               "<1s>", "<2s>", "<3s>", "<4s>", "<5s>", "<6s>", "<7s>", "<8s>", "<9s>",
               "<東>", "<南>", "<西>", "<北>", "<白>", "<發>", "<中>"]
    hai = [hai_disp[int(p/4)] for p in yama]
    return hai

def print_in_hex(int_list):
    hex_string_list = [hex(e).upper()[2:] for e in int_list]
    print(','.join(hex_string_list))

if __name__ == '__main__':
    from sample_data import ver_test_samples as samples
    # mt19937ar
    seed = samples["mt19937ar"]["seed"]
    init_mt(seed)
    rnd = mt_gen(138)
    yama = rnd_to_yama(rnd)
    dice = rnd_to_dice(rnd)
    if not(yama == samples["mt19937ar"]["yama"] and dice == samples["mt19937ar"]["dice"]):
        print("don't match in mt19937ar")


    # mt19937ar-sha512-n288
    seed = samples["mt19937ar-sha512-n288"]["seed"]
    init_mt(seed)
    src = mt_gen()
    rnd = src_to_rnd(src)
    yama = rnd_to_yama(rnd)
    dice = rnd_to_dice(rnd)
    if not(yama == samples["mt19937ar-sha512-n288"]["yama"] and dice == samples["mt19937ar-sha512-n288"]["dice"]):
        print("don't in mt19937ar-sha512-n288")

    # mt19937ar-sha512-n288-base64
    seed = samples["mt19937ar-sha512-n288-base64"]["seed"]
    init = b64seed_to_init(seed)
    init_mt(init)
    src = mt_gen()
    rnd = src_to_rnd(src)
    yama = rnd_to_yama(rnd)
    dice = rnd_to_dice(rnd)
    if not(yama == samples["mt19937ar-sha512-n288-base64"]["yama"] and dice == samples["mt19937ar-sha512-n288-base64"]["dice"]):
        print("don't in mt19937ar-sha512-n288-base64")
    
    print("done")

