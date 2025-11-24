#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <bitset>
#include <iterator>
#include <stdexcept>
#include <unordered_map>
#include <algorithm>
#include <iostream>
#include <iomanip>
#include <string>
#include <chrono>

using namespace std;

struct EstimateResult {
   const double pGlobal;
   const double pGlobalPrime;
   const double pLocal;
   const double minEntropy;
};

EstimateResult multiMostCommonWindowMinEntropy(const vector<int>& s, int k) {
    int L = s.size();
    cout << "Length of the sequence: " << L << endl;

    // cout << "s[ ";
    // for (int i = 0; i < L; ++i) {
    //     cout << s[i] << " " ;
    // }
    // cout << "] " << endl;

    // std::cout << " i |   frequent      |score-before |win(w)| pred |s[i]|  corr | score-after\n"
    //              "------------------------------------------------------------------------------\n";

    if (L == 0 || k < 1) {
        throw invalid_argument("Sequence must be nonempty and k>=1");
    }

    // according to the paper, the window sizes are:
    
    const int w1 = 63;
    const int w2 = 253;
    const int w3 = 1023;
    const int w4 = 4095;
    

    // the example in NIST 
    // const int w1 = 3;
    // const int w2 = 5;
    // const int w3 = 7;
    // const int w4 = 9;


    const int w[4] = { w1, w2, w3, w4 };
    int N = L - w1;
    
    if (N <= 0) {
        throw invalid_argument("Sequence too short for w1=63");
    }
    vector<bool> correct(N, false);
    // 2. Scoreboard & state
    int scoreboard[4] = {0,0,0,0};
    int winner = 0;  

    // 3. Main pass
    for (int i = w1; i < L; ++i) {
        // cout << i << endl;
        int preScore[4] = {scoreboard[0], scoreboard[1], scoreboard[2], scoreboard[3]};
        int preWinner = winner;
        int freqVal[4] = {-1, -1, -1, -1};
        
        const int w_offsets[4] = {i - w1, i - w2, i - w3, i - w4}; 
        for (int j = 0; j < 4; ++j) {
            if (i >= w[j]) {
                unordered_map<int, int> count, lastPos; 
                for (int p = w_offsets[j]; p < i; ++p) {
                    count[s[p]]++;
                    lastPos[s[p]] = p;
                }
                int bestSym = -1, bestCount = -1, bestLast = -1;
                for (auto& [sym, c] : count) {
                    if (c > bestCount || (c == bestCount && lastPos[sym] > bestLast)) {
                        bestCount = c;
                        bestLast = lastPos[sym];
                        bestSym = sym;
                    }
                }
                freqVal[j] = bestSym;
            }
        }
    
        int prediction = freqVal[winner];
        bool wasCorrect = (prediction == s[i]);
        correct[i - w1] = wasCorrect;
    
        for (int j = 0; j < 4; ++j) {
            if (freqVal[j] == s[i]) {
                ++scoreboard[j];
                if (scoreboard[j] >= scoreboard[winner]) {
                    winner = j;
                }
            }
        }
    
        // std::string predStr = (prediction >= 0) ? std::to_string(prediction) : "--";
    
        // std::cout << std::setw(3) << (i ) << " | ("
        //           << std::setw(2) << (freqVal[0] >= 0 ? std::to_string(freqVal[0]) : "--") << ", "
        //           << std::setw(2) << (freqVal[1] >= 0 ? std::to_string(freqVal[1]) : "--") << ", "
        //           << std::setw(2) << (freqVal[2] >= 0 ? std::to_string(freqVal[2]) : "--") << ", "
        //           << std::setw(2) << (freqVal[3] >= 0 ? std::to_string(freqVal[3]) : "--")
        //           << ") | (" << preScore[0] << "," << preScore[1] << "," << preScore[2] << "," << preScore[3]
        //           << ") |  " << (preWinner + 1) << "  |  " << std::setw(2) << predStr
        //           << "  |  " << std::setw(2) << s[i] << "  |   " << (wasCorrect ? 1 : 0)
        //           << "   | (" << scoreboard[0] << "," << scoreboard[1] << "," << scoreboard[2] << "," << scoreboard[3] << ")\n";
    }

    // for (int i = 0; i < N; i++) {
    //     if (i % 1000 == 0) { // Sample some outputs
    //         cout << "correct[" << i << "] = " << correct[i] << endl;
    //     }
    // }

    // 4. Count correct predictions
    int C = count(correct.begin(), correct.end(), true);
   // cout << "Correct predictions: " << C << " of " << N << " (positions " << w1 << " to " 
    //<< (L-1) << ")" << endl;
    double pGlobal = double(C) / double(N);

    // 5. Upper 99% CI on pGlobal
    double pGlobalPrime;
    if (C == 0) {
        pGlobalPrime = 1.0 - pow(0.01, 1.0 / N);
    } else {
        double z  = 2.576;  // Z_{1-0.005}
        double se = sqrt(pGlobal * (1.0 - pGlobal) / (N - 1));
        pGlobalPrime = min(1.0, pGlobal + z * se);
    }

    // 6. Local performance: longest run of ones in correct
    int maxRun = 0, run = 0;
    for (bool c : correct) {
        if (c) {
            ++run;
            maxRun = max(maxRun, run);
        } else {
            run = 0;
        }
    }
    int r = maxRun + 1;

    // 6b. Binary‐search solve for pLocal
    auto evalLogF = [&](double p) {
        double q    = 1.0 - p;
        double x    = 1.0;
        double pPow = pow(p, r);
        for (int j = 1; j <= 10; ++j) {
            x = 1.0 + q * pPow * pow(x, r + 1);
        }
        double num  = 1.0 - p * x;
        double den1 = r + 1.0 - r * x;
        if (num <= 0.0 || den1 <= 0.0 || q <= 0.0 || x <= 0.0)
            return -numeric_limits<double>::infinity();
        return log(num)
             - log(den1)
             - log(q)
             - (N + 1) * log(x);
    };
    double logTarget = log(0.99);
    double lo = 0.0, hi = 1.0, mid = 0.0;
    for (int it = 0; it < 50; ++it) {
        mid = 0.5 * (lo + hi);
        double g = evalLogF(mid) - logTarget;
        if (g > 0) lo = mid; else hi = mid;
    }
    double pLocal = 0.5 * (lo + hi);

    // 7. Final min‐entropy
    double maxP       = max({ pGlobalPrime, pLocal, 1.0 / k });
    double minEntropy = -log2(maxP);

    return { pGlobal, pGlobalPrime, pLocal, minEntropy };
}

vector<int> loadBlocks(const string& filename) {
    ifstream file(filename);
    vector<int> blocks;
    string line;
    vector<int> bits;

    // 1) Read each text line
    while (getline(file, line)) {
        for (char c : line) {
            if (c == '0' || c == '1' || c == '2')
                bits.push_back(c - '0');
        }
    }
    return bits;

}



// vector<int> loadBlocks(const string& filename) {
//     // 1) Open in binary mode
//     ifstream file(filename, ios::binary);
//     if (!file) {
//         std::cerr << "Error: Could not open '" << filename << "'\n";
//         return {};
//     }

//     // 2) Read exactly 8 bytes (64 bits)
//     constexpr size_t NUM_BYTES = 1000; 
//     unsigned char buffer[NUM_BYTES];
//     file.read(reinterpret_cast<char*>(buffer), NUM_BYTES);
//     std::streamsize bytesRead = file.gcount();
//     if (bytesRead <= 0) {
//         std::cerr << "Error: No data read (file may be empty)\n";
//         return {};
//     }

//     // 3) Extract bits
//     vector<int> bits;
//     bits.reserve(bytesRead * 8);
//     for (streamsize i = 0; i < bytesRead; ++i) {
//         // For each byte, extract bits 7→0
//         for (int bit = 7; bit >= 0; --bit) {
//             bits.push_back((buffer[i] >> bit) & 0x1);
//         }
//     }

//     return bits;
// }


int main() {
    auto start = chrono::high_resolution_clock::now();
    //const string filename = "../datasets/data.bin"; // to read the raw binary file data.bin
    //const string filename = "../data_sets/MCW_NIST_Example.txt"; // to read as string the sample_data.txt (example in NIST)
    const string filename = "../data_sets/128KB.txt"; // to read the synthetic data generated by the script
    auto blocks = loadBlocks(filename);

    if (blocks.empty()) {
        cerr << "No blocks loaded.\n";
        return 1;
    }

    //cout << "Total bit blocks read: " << blocks.size() << "\n";

    int k = 2;

    auto res = multiMostCommonWindowMinEntropy(blocks, k);
    cout << std::fixed;
    cout 
        //  << "P_global       = " << res.pGlobal       << "\n"
        //  << "P_global_prime = " << res.pGlobalPrime  << "\n"
        //  << "P_local        = " << res.pLocal        << "\n"
         << "Min-entropy    = " << res.minEntropy    << " bits\n";

    auto end = chrono::high_resolution_clock::now();
    
    cout << "Time taken: " << chrono::duration<double>(end - start).count() << " seconds\n";


    return 0;
}









