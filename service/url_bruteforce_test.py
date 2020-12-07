from random import choice

SMALL_CHARS = "abcdefghijklmnopqrstuvwxyz"
LARGE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"


def generate_tokens(url_len, alphabet, runs):
    chars = list(alphabet)
    token_set = set()

    run_id = 0
    while run_id < runs:
        token = ''.join(choice(chars) for _ in range(url_len))
        if token in token_set:
            continue
        token_set.add(token)
        run_id += 1

    return token_set


def brute_force_short_urls(url_len, alphabet, tokens, runs):
    chars = list(alphabet)
    hits = 0

    for _ in range(runs):
        token = ''.join(choice(chars) for _ in range(url_len))
        if token in tokens:
            # print(token)
            hits += 1

    return hits


def main():
    res_list = list()
    tokens_v1 = generate_tokens(3, SMALL_CHARS, 15000)
    v1_list = list()
    for _ in range(10):
        v1_list.append(tokens_v1.pop())
    # print("V1 ( len = 3 || charset = a-z ): {0}".format(", ".join(v1_list)))
    print("V1 ( len = 3 || charset = a-z ):")
    res_list.append(brute_force_short_urls(3, SMALL_CHARS, tokens_v1, 15000))
    print("Brute-force hits: {0} \n".format(res_list[-1]))

    tokens_v2 = generate_tokens(3, SMALL_CHARS + LARGE_CHARS, 15000)
    v2_list = list()
    for _ in range(10):
        v2_list.append(tokens_v2.pop())
    # print("V2 ( len = 3 || charset = a-zA-Z ): {0}".format(", ".join(v2_list)))
    print("V2 ( len = 3 || charset = a-zA-Z ):")
    res_list.append(
        brute_force_short_urls(3, SMALL_CHARS + LARGE_CHARS, tokens_v2, 15000))
    print("Brute-force hits: {0} \n".format(res_list[-1]))

    tokens_v3 = generate_tokens(3, SMALL_CHARS + LARGE_CHARS + NUMBERS, 15000)
    v3_list = list()
    for _ in range(10):
        v3_list.append(tokens_v3.pop())
    # print("V3 ( len = 3 || charset = a-zA-Z0-9 ): {0}".format(", ".join(v3_list)))
    print("V3 ( len = 3 || charset = a-zA-Z0-9 ):")
    res_list.append(
        brute_force_short_urls(3, SMALL_CHARS + LARGE_CHARS + NUMBERS, tokens_v3,
                               15000))
    print("Brute-force hits: {0} \n".format(res_list[-1]))

    tokens_v4 = generate_tokens(4, SMALL_CHARS, 15000)
    v4_list = list()
    for _ in range(10):
        v4_list.append(tokens_v4.pop())
    # print("V4 ( len = 4 || charset = a-z ): {0}".format(", ".join(v4_list)))
    print("V4 ( len = 4 || charset = a-z ):")
    res_list.append(
        brute_force_short_urls(4, SMALL_CHARS, tokens_v4, 15000))
    print("Brute-force hits: {0} \n".format(res_list[-1]))

    tokens_v5 = generate_tokens(4, SMALL_CHARS + LARGE_CHARS + NUMBERS, 15000)
    v5_list = list()
    for _ in range(10):
        v5_list.append(tokens_v5.pop())
    # print("V5 ( len = 4 || charset = a-zA-Z0-9 ): {0}".format(", ".join(v5_list)))
    print("V5 ( len = 4 || charset = a-zA-Z0-9 ):")
    res_list.append(
        brute_force_short_urls(4, SMALL_CHARS + LARGE_CHARS + NUMBERS, tokens_v5,
                               15000))
    print("Brute-force hits: {0} \n".format(res_list[-1]))
    return res_list


if __name__ == "__main__":
    run_count = 5
    tmp_list = [0] * 5
    print(tmp_list)
    for _ in range(run_count):
        tmp = main()
        for idx in range(5):
            tmp_list[idx] += tmp[idx]
    print(tmp_list)
    for idx in range(len(tmp_list)):
        tmp_list[idx] /= (run_count * 150)

    print("% Hits as follows:")
    print(tmp_list)
