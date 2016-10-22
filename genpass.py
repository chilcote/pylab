#!/usr/bin/python
"""Returns a 'memorable' password to facilitate typing off another computers screen
Originally designed for making long/semi-complex, but easier to type passwords
"""
# ref: https://gist.github.com/arubdesu/a3d0087438da6d0f77ab


import optparse
import gzip
from random import randrange, choice


def chunkstring(string, length):
    """list the comprehendo, my friendo"""
    return (string[0+i:length+i] for i in range(0, len(string), length))

# Read in a range of the same words Password Assistant uses, much thanks to frogor
def words_in_range(short, loong):
    """Given a low and high length, return a list of words provided on OS X"""
    words_path = '/System/Library/Frameworks/SecurityInterface.framework/Resources/pwa_dict_en.gz'
    words_file = gzip.open(words_path, 'rb')
    # seek(essentially) to the second 'table' of data that tells you beginning/ends of words
    #pylint: disable=unused-variable
    ignore = words_file.read(512)
    # build our word length counts with the 64 sections as indexes, with the values
    # represented in the file as hex - ergo the '16', which int converts
    word_counts = dict()
    for num_of_letters_index in range(64):
        word_counts[num_of_letters_index] = int(words_file.read(8).strip(), 16)
    keys = sorted(word_counts.keys())

    results = []
    for counts in keys:
        this_count = word_counts[counts]
        if this_count > 0:
            # Only look for words if word count is more than 0
            # read (the number of words * word length) bytes
            raw_words = words_file.read(this_count*counts)
            # chunk them up by word length
            words = chunkstring(raw_words, counts)
            for word in words:
                if len(word) >= short and len(word) <= loong:
                    try:
                        word.decode('ascii')
                        results.append(word)
                    #pylint: disable=bare-except
                    except:
                        pass
    words_file.close()
    return results

def main():
    """gimme some main"""
    #pylint: disable=invalid-name
    p = optparse.OptionParser()
    p.set_usage("""Usage: %prog [options]""")
    p.add_option('--shortest', '-s', dest='shortest_number', default=6, type=int,
                 help="""(Integer) Number of letters in shortest words to randomly choose.""")
    p.add_option('--longest', '-l', dest='longest_number', default=10, type=int,
                 help="""(Integer) Number of letters in longest words to randomly choose.""")
    p.add_option('--total', '-t', dest='total_length', default=22, type=int,
                 help="""(Integer) Total number of letters in final password.""")
    #pylint: disable=unused-variable
    options, arguments = p.parse_args()
    scoped_words = words_in_range(options.shortest_number, options.longest_number)
    full_len = len(scoped_words)
    front, back = (scoped_words[randrange(0, full_len)], scoped_words[randrange(0, full_len)])
    diff_string = ''
    if len(front + back) < options.total_length:
        difference = options.total_length - len(front + back)
        while difference > 4:
            #pylint: disable=anomalous-backslash-in-string
            diff_string += choice('!@#$%&*+=-<>?/\:')
            difference -= 1
        #pylint: disable=unused-variable
        for diff in range(difference):
            diff_string += str(randrange(5, 10, 2))
    final_password = ''.join([front, diff_string, back])
    print final_password

if __name__ == '__main__':
    main()
