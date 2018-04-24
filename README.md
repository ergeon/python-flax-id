# Flax ID

Flax ID is an algorithm for generating unique distributed ids, made to be used
at ezHome Inc.

Conceptually it belongs to the family of "Flake ID" algorithms.

For an overview of the idea, see, for example:

1. [http://yellerapp.com/posts/2015-02-09-flake-ids.html](http://yellerapp.com/posts/2015-02-09-flake-ids.html)

## Design Goals

We wanted an algorithm with the following characteristics:

1. Completely distributed, requires no co-ordination
2. Generates ids that are unique, with very high probability
3. Generates ids that can be roughly ordered according to the time of creation
4. Ids have a nice string representation
5. Works the same across different languages and platforms

Multiple implementations exist but not all of them satisfy the above criteria,
and the details of implementations vary wildly (most notably in the length and
composition of the data), and we couldn't find a solution that was implemented
the same way in different languages.

Some of the candidates considered:

* Python: [simpleflake](https://github.com/SawdustSoftware/simpleflake)
* Javascript: [flake-idgen](https://www.npmjs.com/package/flake-idgen)

As a result, we decided to write our own algorithm, which gives us the
following benefits:

1. We control the exact parameters of the id generation (e.g. bit lengths)
2. We can describe the algorithm very precisely, which makes writing
implementations in different languages straightforward, as opposed to trying
to decipher the intents of the algorithm creators

We found inspiration (and some validation) for this approach in this article
by Firebase:
[The 2^120 Ways to Ensure Unique Identifiers](https://www.firebase.com/blog/2015-02-11-firebase-unique-identifiers.html)

TODO: Add explanation of what is wrong with UUID (spoiler: mostly ordering).

## Implementation Details

### Composition

The Flax ID contains 96 bits, of which first 40 bits are the timestamp, and
the next 56 bits are random.
This gives 2^56 possible unique ids per millisecond.

The number 96 was chosen on the following grounds:

1. It is divisible by 6, so can be rendered as base64-encoded string without
padding
2. It is divisible by 8, so it can be represented as a byte array
3. It leaves enough room for the random part

We save some space on the timestamp component by using a custom epoch start
(we start on 2015-01-01), which allows us to use 40 bits, instead of 42 to
represent the timestamp for the next 30+ years.


    Here is the structure of the example id:

    | 00000      10111001010010101010101001010001111   01110110100000001100101110001011101110011011110111000001 |
    | (padding)             timestamp                |                        randomness                        |
    |                  40                            |                            56                            |

    (Padding is necessary when there is less than 40 bits in the timestamp, e.g. the elapsed time since the epoch
     is still relatively small)

    And here is the rendering with our modified Base64 alphabet:

    000001 011100 101001 010101 010100 101000 111101 110110 100000 001100 101110 001011 101110 011011 110111 000001
       0      R      d      K      J      c      x      q      V      B      i      A      i      Q      r      0

### Representation

The canonical representation of the Flax ID is Base64-encoded, URL safe string
(16 characters).
We're using the slightly modified Base64 alphabet, which gives us the
guaranteed lexicographical ordering of the strings thus produced (Firebase does
the same)

    "-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"

### The algorithm

The algorithm is defined as follows:

1. Take a timestamp, as a number of milliseconds since the beginning of our
epoch
2. Combine it, by means of left binary shift with 56 random bits
3. Represent the number as binary string, applying padding, if necessary, so
the total number of bits is 96
4. Encode the binary string using the Base64 alphabet above, taking each 6
bits to represent a number

## Installation

    $ pip install python-flax-id

## Development

### Running tests

As usual run:

    $ make test

### Publishing new release

To publish new release you need to,

1. Bump version number according to [SemVer](http://semver.org/) in
   `flax_id/__init__.py` file and put a log into *ChangeLog* section below
2. Wait for your code is tested on Circle CI & merged to `master`
3. Create new Git tag with version number as `vX.Y.Z` and push it to remote
4. Publish new release to pypi

#### Git Tag Snippet

    git tag -a vX.Y.Z -m 'X.Y.Z Release'
    git push --tags

## Changelog

### 1.0.0 (2018-04-24)

- Initial public release

