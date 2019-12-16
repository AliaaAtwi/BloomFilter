import math
import hashlib
import numbers


class BloomFilter:

    def __init__(self, num_words, num_bits):
        '''
        Creates a Bloom Filter with the specified number of bits.
        The number of hash functions used is automatically chosen to minimize
        the probability of false positives for the given number of bits and the
        number of words expected to be added to the filter.

        Args:
            num_words (int): number of words expected to be stored in filter
            num_bits (int) : number of bits to represent the filter contents

        '''
        BloomFilter._validate_num_words(num_words)
        BloomFilter._validate_num_bits(num_bits)
        self._num_words = num_words
        self._num_bits = num_bits
        self._false_positive_prob = BloomFilter._calculate_false_positive(
                                                        num_words, num_bits)
        self._num_hash = BloomFilter._calculate_num_hash(num_words, num_bits)          
        self._bit_array = [False]*num_bits
        # TODO: replace list of bools with a bitarray to reduce space overhead
    
    @property
    def num_words(self):
        '''int: number of words expected to be added to the filter'''
        return self._num_words

    @property
    def num_bits(self):
        '''int: Number of bits used in the filter'''
        return self._num_bits
    
    @property
    def false_positive_probability(self):
        '''float: theoretical false positive probability of the filter'''
        return self._false_positive_prob
     
    @property
    def num_hash(self):
        '''int: num of hash functions required to minimize false positives'''
        return self._num_hash
    
    @classmethod
    def with_false_positive_constraint(cls, num_words, probability):
        ''' 
        Factory method to create a filter given a false positive probability 
        constraint instead of a set number of bits. Calculates the number of 
        bits required to meet constraint assuming an optimal number of hash 
        functions.
        
        Args:
            num_words (int): capacity of filter
            probability (float): false probability constraint 
        
        Returns:
            An instance of a bloom filter
        '''
        BloomFilter._validate_num_words(num_words)
        BloomFilter._validate_probability(probability)
        num_bits = cls._calculate_num_bits(num_words, probability)
        return cls(num_words, num_bits)
    
    def add(self, word) -> None: 
        ''' 
        Adds a word to the filter, by computing k hashes: word -> [0, m-1]
        And setting the corresponding bits in the filter to 1.
        
        '''
        BloomFilter._validate_word(word)
        
        bit_indices = self._get_hashes(word)
        for i in bit_indices:
            self._bit_array[i] = True
            
    def query(self, word) -> bool: 
        ''' 
        Checks if a word is in the filter by calculating its hashes, and
        verifying if the corresponding indices in the bit array are all set.
        
        Args:
            word (string)  
            
        Returns:
            Boolean: True if word in filter
            
        '''
        BloomFilter._validate_word(word)
        
        bit_indices = self._get_hashes(word)        
        return all([self._bit_array[i] for i in bit_indices])
    
    def _get_hashes(self, word):
        '''Computes k hashes of a word to [0,m-1], k=num_hash
        
        To minimize false positives, the hash functions should be independent,
        and map words uniformly to [0, m-1]. 
        
        (Implemented here) For larger problems, we can use the results of "Less
        Hashing, Same Performace" by Kirsch et al (2007): Using two hash 
        functions, h1 and h2, we can generate k different hashes 
        g_i(x) = h_1(x) + i * h_2(x), without compromising asymptotic false 
        positive probability. 
        
        (TODO) For small problem sizes, it is possible to produce independent 
        hashes by taking k chunks of log2(m) bits from the output of a 'good' 
        hash function, ex: md5 (since its bits should have little correlation 
        with each other). This works as long as k*log2(m)<= width of output.
        
        Args:
            word (string)
            
        Returns:
            List of k hashes
        
        '''
        # Computes the md5 hash of the word, and slices it into two halves
        # to produce 'independent' hashes h1 and h2 
        h1 = int(hashlib.md5(word.encode()).hexdigest()[:15], 16)
        h2 = int(hashlib.md5(word.encode()).hexdigest()[16:], 16)
        
        return [(h1 + i*h2) % self._num_bits for i in range(1, self.num_hash+1)]
          
    @staticmethod
    def _calculate_num_bits(n, p): 
        ''' 
        Required number of bits to represent a vocabulary of size n 
        while staying within allowable false positive probability,
        assuming an optimal number of hash functions is used.
        
        Args:
            n (int): numbers of words to be stored in Bloom Filter 
            p (float): maximum allowable false positive probability
            
        Returns:
            m (int): length of bit array -(n * ln(p)) / (ln(2)^2)
            
        '''
        m = -(n * math.log(p))/(math.log(2)**2) 
        return math.ceil(m) 
  
    @staticmethod
    def _calculate_num_hash(n, m): 
        ''' 
        Number of hash functions that minimizes false positive probability
         
        Args:
            n (int): numbers of words to be stored in Bloom Filter 
            m (int): length of bit array
            
        Returns:
            k  (int): optimal number of hash functions = (m/n) * ln(2)
            
        '''
        # This formula is derived using approximations that assume large n
        # TODO: Think of more accurate alternatives for small problem sizes
        # TODO: when k is not an integer, check false positive prob for
        #      floor(k) and ceil(k), and return the more optimal one
        k = (m/n) * math.log(2)
        return int(k)
    
    @staticmethod
    def _calculate_false_positive(n, m):
        ''' 
        False positive probability for a given vocabulary size and number 
        of bits, assuming an optimal number of hash functions is used.
        
        Args:
            n (int): numbers of words to be stored in Bloom Filter 
            m (int): length of bit array
            
        Returns:
            p (float): false positive probability
            
        '''
        return math.exp(-(m/n) * (math.log(2)**2))
          
    @staticmethod
    def _validate_num_words(n):
        if not isinstance(n, int):
            raise TypeError("Number of words should be an integer")
        if n <= 0:
            raise ValueError("Number of words should be positive")
    
    @staticmethod
    def _validate_num_bits(m): 
        if not isinstance(m, int):
            raise TypeError("Length of bit array should be an integer")
        if m <= 0:
            raise ValueError("Length of bit array should be positive")
            
    @staticmethod
    def _validate_probability(p):    
        if not isinstance(p, numbers.Number):
            raise TypeError("Probability should be a number")
        if p <= 0 or p >= 1:
            raise ValueError("Probability should be a number in (0,1)")
    
    @staticmethod
    def _validate_word(w):
        if not isinstance(w, str):
            raise TypeError("Word should be a string")
            
    def __str__(self):
        return "Word Capacity = " + str(self.num_words) + "\n" \
                + "Number of bits = " + str(self.num_bits) + "\n"\
                + "False positive probability = " + \
                str(self.false_positive_probability)    