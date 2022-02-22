"""
Copyright (C) 2022 Nathan Lim (a.k.a NateNate60)
    This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
"""

import hashlib

def genseed () -> str :
    """
    Securely generate a random seed. Returns hex string
    """
    with open("/dev/random", "rb") as f :
        return f.read(32).hex()

def hashseed (seed: str) -> str :
    """
    Returns the SHA-256 hash of the seed as hex string
    """
    hash = hashlib.sha256()
    hash.update(bytes(seed, "ascii"))
    return hash.hexdigest()

def genrandom (seed: str, nonce: int) :
    """
    Generate the random number from a seed and a nonce. Returns hex string
    """
    seed = hex(int(seed, 16) + nonce)[2:] #NOTE: this is artimatic addition, not string concatenation but both are okay as long as it is disclosed to the player
    hash = hashlib.sha3_256()
    hash.update(bytes(seed, "ascii"))
    return hash.hexdigest()