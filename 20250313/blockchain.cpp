#include <iostream>
#include <string>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <openssl/sha.h>

using namespace std;

namespace Blockchain {
    // Function to calculate SHA-256 hash
    string calculateHash(const string& input) {
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256_CTX sha256;
        SHA256_Init(&sha256);
        SHA256_Update(&sha256, input.c_str(), input.length());
        SHA256_Final(hash, &sha256);
        
        stringstream ss;
        for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
            ss << hex << setw(2) << setfill('0') << static_cast<int>(hash[i]);
        }
        return ss.str();
    }

    // Block structure
    class Block {
    public:
        // Block Header
        string blockHeader;
        string prevBlockHash;
        time_t timestamp;
        int nonce;
        string blockDataHash;
        
        // Block Data - In a real blockchain, this would be a list of transactions
        string blockData;
        
        // Pointer to next block in the chain
        Block* nextBlock;
        
        // Constructor
        Block(const string& header, const string& prevHash, time_t time, 
              int nonceValue, const string& dataHash, const string& data)
            : blockHeader(header), prevBlockHash(prevHash), timestamp(time),
              nonce(nonceValue), blockDataHash(dataHash), blockData(data), nextBlock(nullptr) {}
    };

    // Function to display block information
    void displayBlock(Block* block) {
        cout << "Block Header: " << block->blockHeader << endl;
        cout << "Previous Block Hash: " << block->prevBlockHash << endl;
        cout << "Timestamp: " << ctime(&block->timestamp);
        cout << "Nonce: " << block->nonce << endl;
        cout << "Block Data Hash: " << block->blockDataHash << endl;
        cout << "Block Data: " << block->blockData << endl;
        cout << "-----------------------------------" << endl;
    }

    // Function to create a new block
    Block* createBlock(Block* previousBlock, const string& blockHeader, int nonce, const string& data) {
        time_t currentTimestamp = time(nullptr);
        
        // Create string to hash for blockDataHash
        stringstream ss;
        ss << blockHeader << currentTimestamp << nonce << data;
        string blockDataHash = calculateHash(ss.str());
        
        // Create new block
        Block* newBlock = new Block(
            blockHeader,
            previousBlock->blockDataHash,
            currentTimestamp,
            nonce,
            blockDataHash,
            data
        );
        
        // Link the previous block to this new block
        previousBlock->nextBlock = newBlock;
        
        return newBlock;
    }

    // Class to manage the blockchain
    class Chain {
    private:
        Block* genesisBlock;
        Block* latestBlock;
        
    public:
        // Constructor
        Chain() {
            // Create Genesis Block
            string genesisBlockHeader = "GenesisBlock";
            string genesisData = "Genesis Block Data";
            string genesisBlockHash = calculateHash(genesisBlockHeader + genesisData);
            
            genesisBlock = new Block(
                genesisBlockHeader,
                "None", // Genesis block has no previous block
                time(nullptr),
                0,
                genesisBlockHash,
                genesisData
            );
            
            latestBlock = genesisBlock;
        }
        
        // Destructor
        ~Chain() {
            // Clean up memory
            Block* currentBlock = genesisBlock;
            while (currentBlock != nullptr) {
                Block* temp = currentBlock;
                currentBlock = currentBlock->nextBlock;
                delete temp;
            }
        }
        
        // Add a new block to the chain
        void addBlock(const string& blockHeader, int nonce, const string& data) {
            latestBlock = createBlock(latestBlock, blockHeader, nonce, data);
        }
        
        // Display the entire blockchain
        void displayChain() {
            Block* currentBlock = genesisBlock;
            int blockCount = 0;
            
            while (currentBlock != nullptr) {
                cout << "Block #" << blockCount << ":\n";
                displayBlock(currentBlock);
                currentBlock = currentBlock->nextBlock;
                blockCount++;
            }
        }
        
        // Get the genesis block
        Block* getGenesisBlock() {
            return genesisBlock;
        }
        
        // Get the latest block
        Block* getLatestBlock() {
            return latestBlock;
        }
    };
}

// Main function
int main() {
    using namespace Blockchain;
    
    // Create blockchain
    Chain blockchain;
    
    cout << "Genesis block created:\n";
    displayBlock(blockchain.getGenesisBlock());
    
    // Interactive loop to add blocks
    while (true) {
        string blockHeader;
        cout << "Enter block header (or type 'exit' to stop): ";
        getline(cin, blockHeader);
        
        if (blockHeader == "exit") {
            break;
        }
        
        int nonce;
        cout << "Enter nonce for block '" << blockHeader << "': ";
        cin >> nonce;
        cin.ignore(); // Clear the newline character
        
        string blockData;
        cout << "Enter data for block '" << blockHeader << "': ";
        getline(cin, blockData);
        
        // Add new block to the chain
        blockchain.addBlock(blockHeader, nonce, blockData);
        
        cout << "\nBlock added to the chain:\n";
        displayBlock(blockchain.getLatestBlock());
    }
    
    // Display the entire blockchain
    cout << "\nDisplaying entire blockchain:\n";
    blockchain.displayChain();
    
    return 0;
}