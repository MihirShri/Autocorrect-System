from collections import defaultdict


with open('WSJ_02-21.pos', 'r') as f:
    lines = f.readlines()

lelo = "''"

numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "-", ".", "\\", '`', '$', '&', "'"]

words_normal = [line.split('\t')[0] for line in lines]
words_l = [k.lower() for k in words_normal]
words_o = [m for m in words_l if m != '\n']
words = [a for a in words_o if len(a) > 1 and a[0] not in numbers and a[1] not in numbers]
words.sort()

counter = defaultdict(int)
for word1 in words:
    counter[word1] += 1

vocab = [w for w, v in counter.items()]
vocab.sort()


def get_prob(words_list):
    words_dict = {}
    words_prob = {}
    for word in words_list:
        words_dict[word] = words_dict.get(word, 0) + 1

    for word in words_dict.keys():
        words_prob[word] = words_dict[word] / sum(words_dict.values())

    return words_prob


def delete_letter(word):
    split_l = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    delete_l = [L + R[1:] for L, R in split_l if R]

    return delete_l


def switch_letter(word):
    split_l = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    switch_l = [L + R[1] + R[0] + R[2:] for L, R in split_l if len(R) > 1]

    return switch_l


def replace_letter(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    split_l = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    replace_l = [L + S + R[1:] for L, R in split_l if R for S in letters]
    replace_set = set(replace_l)
    replace_set.remove(word)
    replace_l = sorted(list(replace_set))

    return replace_l


def insert_letter(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    split_l = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    insert_l = [L + S + R for L, R in split_l for S in letters]

    return insert_l


def edit_one_letter(word, allow_switches=True):
    edit_one_set = set()
    edit_one_set.update(delete_letter(word))
    if allow_switches:
        edit_one_set.update(switch_letter(word))
    edit_one_set.update(replace_letter(word))
    edit_one_set.update(insert_letter(word))

    return edit_one_set


def edit_two_letters(word, allow_switches=True):
    edit_two_set = set()
    edit_one_set = edit_one_letter(word, allow_switches)
    for w in edit_one_set:
        if w:
            edit_two_set.update(edit_one_letter(w, allow_switches))

    return edit_two_set


def get_correct(word, prob, vocab, n=3):
    suggestions = (word in vocab and word) or edit_one_letter(word).intersection(vocab) or \
                  edit_two_letters(word).intersection(vocab)
    n_best_unsorted = [(w, prob[w]) for w in list(suggestions)]
    n_best = sorted(n_best_unsorted, key=lambda x: x[1], reverse=True)[:n]

    return n_best


probs = get_prob(words)

print()
print("A simple autocorrect system.")
print()
my_word = input("Enter a misspelled word: ")
correct_word = get_correct(my_word, probs, vocab)
print("Instead of " + my_word + ", You meant: ")
for i, word in enumerate(correct_word):
    print(f"{word[0]} with probability: {word[1]:.6f}")
