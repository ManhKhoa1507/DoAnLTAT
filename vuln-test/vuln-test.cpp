#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <openssl/sha.h>

std::string str2hex(const unsigned char * string, int length)
{
    std::stringstream ss;
    for(int i = 0; i < length; i++)
    {
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)string[i];
    }

    return ss.str();
}

std::string sha256_digest(const std::string plaintext)
{
    unsigned char digest[SHA256_DIGEST_LENGTH];

    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, plaintext.c_str(), plaintext.size());
    SHA256_Final(digest, &sha256);

    return str2hex(digest, SHA256_DIGEST_LENGTH);
}

int main()
{
    std::string plaintext = "University of Information Technology";
    std::cout << "Plaintext: " << plaintext << "\n";

    std::string digest = sha256_digest(plaintext);
    std::cout << "SHA256 Digest " << digest << "\n";
}