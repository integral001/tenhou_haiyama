import mjlog_reader as mlr
import haiyama_generetor as hyg

def game_sim_sha512(seed, shuffle_ver, num_round):
    game = []
    if shuffle_ver == "mt19937ar-sha512-n288-base64":
        init = hyg.b64seed_to_init(seed)
    elif shuffle_ver == "mt19937ar-sha512-n288":
        init = seed
    hyg.init_mt(init)
    for _ in range(num_round):
        src = hyg.mt_gen()
        rnd = hyg.src_to_rnd(src)
        yama = hyg.rnd_to_yama(rnd)
        dice = hyg.rnd_to_dice(rnd)
        game.append({"yama:": yama, "yama_disp": hyg.disp_hai(yama), "dice": dice})
    return game

def game_sim_wo_sha512(seeds):
    game = []
    for seed in seeds:
        hyg.init_mt(seed)
        rnd = hyg.mt_gen(138)
        yama = hyg.rnd_to_yama(rnd)
        dice = hyg.rnd_to_dice(rnd)
        game.append({"yama": yama, "yama_disp": hyg.disp_hai(yama), "dice": dice})
    return game

def game_sim(seed, shuffle_ver, num_round=1):
    if shuffle_ver in ["mt19937ar-sha512-n288", "mt19937ar-sha512-n288-base64"]:
        game = game_sim_sha512(seed, shuffle_ver, num_round)
        return game
    elif shuffle_ver in ["mt19937ar"]:
        game = game_sim_wo_sha512(seed)
        return game
    else:
        pass

def yama_generetor(b64_seed):
    init = hyg.b64seed_to_init(b64_seed)
    hyg.init_mt(init)
    while True:
        src = hyg.mt_gen()
        rnd = hyg.src_to_rnd(src)
        yama = hyg.rnd_to_yama(rnd)
        dice = hyg.rnd_to_dice(rnd)
        yield {"yama":yama, "dice":dice}

def game_sim_from_mjlog(path):
    xml = mlr.read_mjlog(path)
    seed = mlr.get_seed(xml)
    shuffle_ver = mlr.get_shuffle_ver(xml)
    num_round = mlr.count_round(xml)
    game = game_sim(seed,shuffle_ver, num_round)
    return game

if __name__ == '__main__':
    paths = [
        "mjlog/2008092000gm-0009-0000-10db094d&tw=0.mjlog",
        "mjlog/2009090100gm-00a9-0000-6920f1ac&tw=3.mjlog",
        "mjlog/2016022509gm-0009-0000-b327da61.mjlog",
    ]

    games = []
    for path in paths:
        game = game_sim_from_mjlog(path)
        games.append(game)
    
    from sample_data import ver_test_samples as samples
    seed = samples["mt19937ar-sha512-n288-base64"]["seed"]
    max_round = 10
    num_round = 0
    gend_game = []
    for game in yama_generetor(seed):
        num_round += 1
        if num_round > max_round:
            break
        gend_game.append(game)

    print("done")
