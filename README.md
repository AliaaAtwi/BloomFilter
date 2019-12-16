# Bloom Filter Implementation

Allows the user to create a Bloom filter by specifying either:
1) A word capacity and a number of bits. 
2) A word capacity and a desired max false positive probability.

The remaining parameters (namely the number of hash functions to use, and in case 2, the number of bits) are then derived to minimize the probability of false positives.

To minimize false positives, the hash functions used should be independent, and should map words uniformly to bits. This implementation uses the results of "Less Hashing, Same Performance" by Kirsch et al (2007): Using two hash functions, h1 and h2, we can generate k different hashes g_i(x) = h_1(x) + i * h_2(x), without compromising asymptotic false positive probability.

### Running the driver program:

The driver program creates two bloom filters, one from a number of bits constraint, and the other from a false positive probability constraint. It populates them with words, and then tests their false positive and false negative probability rates empirically.

In command line:
python Driver.py

### Syntax to instantiate Bloom filters:

from BloomFilter import BloomFilter <br /> <br />
#A bloom filter with 200 bits, and a capacity of 100 words <br />
bloom1 = BloomFilter(100,200) <br /> <br />
#A filter with a false positive probability of 0.1, and a capacity of 100 words<br />
bloom2 = BloomFilter.with_false_positive_constraint(100,0.1)

### Synatx to add a word to a filter:
bloom1.add("A String")

### Synatx to query the filter for a word:
result = bloom1.query("A String") #result is a boolean 
