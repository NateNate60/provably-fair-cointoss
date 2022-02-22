# provably-fair-cointoss
A demonstration of how provably-fair games work, in the form of a coin toss guessing game

If you've ever heard of or visited one of the many online crypto casinos or one of those "Bitcoin dice" games that are everywhere these days, you might have noticed that they advertise that the games are "provably" (/pru:v.əbli:/) fair, as you can "prove" that the game is not rigged. Here's an explanation of what that means, and how you can make one yourself.

**Firstly, a game being provably fair does not mean that the** ***operator*** **is honest.** A game being provably fair does not, on its own, prevent ye olde scam where you send your crypto and it disappears, or where you win a bunch of money but the site won't let you withdraw it. A game being provable fair only prevents the operator from lying to you about, say, the result of dice rolls or roulette spins. The provably fair element protects the integrity of whatever system is being used to generate randomness. That is, it generates pseudo-random numbers in a way that can be *verified*, but not *predicted*. Obviously, if the random numbers can be *predicted*, then the player can cheat at the game.

All code snippets will be in Python. We will implement a simple game where the goal is to guess the result of a coin toss.

# Step 1: Generate a seed

Most systems use a cryptographic hash function to generate random-looking numbers. That's because we can take a random "seed" and then hash it to obscure the seed but still produce a random string of numbers. The first step is to select a random seed. The seed can be any length but must be at 16 bytes long, which is 128 bits. Most commonly we use 32 bytes (256 bits).

    seed = ""
    with open("/dev/random", "rb") as f :
        seed = f.read(32) #read 32 bytes of randomness

Note that I am reading from `/dev/random`. On Linux, this file contains randomness that is gathered from things like Wi-Fi static or noise from microphone input and mouse jiggles.

# Step 2: Hash the seed, then share it with the player

We use a cryptographic hash function to hash the seed, and then we share it with the player. Since the seed is used to generate the random numbers, at any time, the player can demand to see the actual seed and verify the random numbers generated using it, and sharing the hash ahead of time means that they can be sure that we shared the correct seed. This is explained later.

    import hashlib
    seedhash = hashlib.sha256() #We are using SHA-2, which is also used by BTC
    seedhash.update(seed) #feed the seed into the hash function
    seedhash = seedhash.hexdigest() #run the hash, output hexadecimal number

`seedhash` contains the SHA-256 hash of our randomly generated seed, which we share with the player. It is impossible for them to figure out the original seed because they would have to reverse the hash function. At any time, the player can ask to see the original seed, and we, the operator, must show them a seed value that has a SHA-256 hash equalling what we originally shared with them. The only figure we know that satisfies this property is the original seed. Finding something that isn't the seed would mean finding a hash collision for SHA-256. They can then use the seed that was shared with them to verify the sequence of random numbers that we generated using the seed. This is explained later.

If the player wants to see the seed, then that seed is no longer used in any future games. Instead, a new seed is generated. We must then, of course, share the new seed's hash with the player. The old seed is discarded after it's been revealed.

# Step 3: Use the seed to generate random numbers.

For each game, we will append a nonce to the seed which counts sequentially from zero. We then use a different cryptographic hash function to generate the random numbers.

    nonce = "0" #The nonce starts at 0
    # we add 1 to the nonce every time we need to generate another random number
    seed = bytearray.fromhex(seed + nonce) #append nonce to seed, convert from str to bytes
    randomnumberhash = hashlib.sha3_256() #SHA-3 is used by Ethereum
    randomnumberhash.update(seed)
    randomnumberhash = randomnumberhash.hexdigest() #run hash & convert to hex

`randomnumberhash` now contains a random-looking string of hex digits. 

For this example, we're making a coin-flipping game, so we can do something like this:

    result = ""
    if (int(randomnumberhash, 16) % 2 == 0) :
        #the random number is even
        result = "heads"
    else :
        result = "tails"
    
    print(result) 
    # or do whatever you want with the generated result
    # This code will vary depending on what your game is

The algorithm must be shown to the player so they can reproduce the game logic and verify that it was not manipulated (see below).

Ta-da! Provably-fair RNG!

# How to prove the game is not rigged

Let's say I'm a player of this coin-toss guessing game and I think that the game is being rigged. How can the operator prove that it's not?

1. I load into the game. The operator generates a seed and shares the seed's hash with me (see step 2 above)
2. I play a few games and record the results.
3. If I suspect manipulation, I ask the operator for the seed. The operator provides the seed to me.
4. After receiving the seed from the operator, I perform a SHA-256 hash on the seed to check whether it matches the hash I was previously given. It should match if the operator was being honest. If the hash does not match then this is conclusive evidence that the operator is less-than-fully honest, or that they did not implement that provably fair mechanism correctly (in which case they have no way of proving that the game was fair).
5. I append 0 to the seed and perform a SHA-3 hash on it. I then use the result generator algorithm that the operator has published to verify that this combination of seed and nonce indeed gives the result that I received in the 0th round that I played.
6. I append 1 to the seed and perform a SHA-3 hash on it, and then use the procedure in step 5 to verify the result of the 1st round.
7. I repeat the process for every round that I've played to verify that the seed provided indeed does generate the sequence of results that I actually got while playing.
8. I am satisfied that I wasn't cheated. If I want to continue playing, then the operator generates a new seed and shares the new seed's hash. The old seed can be discarded after I've verified the results that it generated.
