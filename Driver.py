from BloomFilter import BloomFilter


def populate_filter(bloom_filter):

    n = bloom_filter.num_words
    for i in range(n):
        bloom_filter.add(str(i))
    print("Added " + str(n) + " words to bloom filter.\n")


def test_false_negative(bloom_filter):

    print("Querying for items previously added to the filter:")
    n = bloom_filter.num_words
    num_hits = sum([bloom_filter.query(str(i)) for i in range(n)])
    print(str(num_hits) + " out of " + str(n) + " words found.\n")


def test_false_positive(bloom_filter):

    print("Querying for 10,000 new words never added to the filter:")
    n = bloom_filter.num_words
    num_hits = sum([bloom_filter.query(str(i)) for i in range(n, n+10000)])
    print("The empirical false positive rate is " + str(num_hits/(10000)))


def main():

    # Example 1
    print("\n\nExample 1 - A Bloom filter that uses 400 bits to store up to" +
          " 100 words:\n")
    bloom1 = BloomFilter(100, 400)
    populate_filter(bloom1)
    test_false_negative(bloom1)
    test_false_positive(bloom1)

    # Example 2
    print("\n\nExample 2 - A Bloom filter that stores up to 1000 words with" +
          " a false positive probability less than 0.01:\n")
    bloom2 = BloomFilter.with_false_positive_constraint(1000, 0.01)
    populate_filter(bloom2)
    test_false_negative(bloom2)
    test_false_positive(bloom2)

if __name__ == "__main__":
    main()