#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <bitset>
#include <iterator>
#include <stdexcept>
#include <chrono>
#include <array>

using namespace std;
static constexpr int b = 6;
const int d = 4; 
const double c_val = 0.5907;   // Constant from step 5.
const double z_conf = 2.576;   // Confidence multiplier (for 99% confidence).
const int two_pow_b   = 1 << b; // 2^b = 64


// double compute_g(double z, int d, int total_blocks) {
//     int v = total_blocks - d;
    
//     double sum = 0.0;
//     for (int t = d + 1; t <= total_blocks; t++) {
//         double innerSum = 0.0;
//         // For u = 1 to t-1
//         for (int u = 1; u < t; u++) {
//             // F(z,t,u) = log2(z) * (z^u * (1-z)^(t-u-1))
//             innerSum += log2(u) * (z * z * pow(1.0 - z, u - 1));
//         }
//         innerSum += log2(t) * (z * pow(1.0 - z, t - 1));
//         sum += innerSum;
//     }
//     return sum / v;
// }

double compute_g(double z, int d, int total_blocks) {
    int v = total_blocks - d;
    
    // Allocate memory
    double* log2_precalc = new double[total_blocks + 1];  
    double* pow_precalc = new double[total_blocks];       
    
    // Initialize first element 
    pow_precalc[0] = 1.0;  // (1-z)^0 = 1
    
    // Combined precalculation loop
    for (int i = 1; i < total_blocks; i++) {
        log2_precalc[i] = log2(i);
        pow_precalc[i] = pow_precalc[i-1] * (1.0 - z);
    }
    // Handle the last log2 value separately
    log2_precalc[total_blocks] = log2(total_blocks);
    
    double sum = 0.0;
    for (int t = d + 1; t <= total_blocks; t++) {
        double innerSum = 0.0;
        for (int u = 1; u < t; u++) {
            innerSum += log2_precalc[u] * (z * z * pow_precalc[u - 1]);
        }
        innerSum += log2_precalc[t] * (z * pow_precalc[t - 1]);
        sum += innerSum;
    }
    
    // Clean up
    delete[] log2_precalc;
    delete[] pow_precalc;
    
    return sum / v;
}


double binary_search_p(double X_prime, int d, int total_blocks, double tol = 1e-16, int max_iter = 100)
{
    double lower = pow(2.0, -b);
    double upper = 1.0;
    auto f = [&](double pp) 
    {
        double qq = (1.0 - pp) / (two_pow_b - 1);
        return compute_g(pp, d, total_blocks) + (two_pow_b - 1) * compute_g(qq, d, total_blocks) - X_prime;
    };
    double f_lo = f(lower), f_hi = f(upper);
    // std::cerr << "DEBUG: f(2^-" << b << ")=" << f_lo
    // << ", f(1)=" << f_hi << "\n";

    if (f_lo * f_hi > 0) 
    {
        std::cerr << "WARNING: f has same sign at both ends; result may be invalid.\n";
    }

    double p = lower;
    for (int iter = 0; iter < max_iter; ++iter) 
    {
        p = 0.5 * (lower + upper);
        double f_p = f(p);
            // convergence on function value OR interval size
        if (fabs(f_p) < tol || (upper - lower) < tol) 
        {
            break;
        }
        if (f_p > 0) 
        {
            lower = p;
        } else 
        {
            upper = p;
        }
    }
    return 0.5 * (lower + upper);
}

double compute_comp_min_entropy(const std::vector<int>& S_prime) 
{
    int total_blocks = S_prime.size();
   // cout << "Total blocks: " << total_blocks << "\n";
    if (total_blocks <= d) {
        std::cerr << "Not enough data blocks\n";
        return 1.0;
    }

    // Step 2: Init dictionary
    array<int, two_pow_b> dict{}; 
   // cout << "Dictionary size: " << dict.size() << "\n";
    
    for (int i = 0; i < d; ++i) {
        dict[S_prime[i]] = i +1;
    }

    // Step 3: Build D
    vector<int> D;
    D.reserve(total_blocks - d);
    for (int i = d; i < total_blocks; ++i) {
        int block = S_prime[i];
        if (dict[block] != 0) {
            D.push_back(i - (dict[block] -1));
        } else {
            D.push_back(i + 1);
        }
        dict[block] = i +1;
    }

    int v = total_blocks - d;
    //cout << "v= " << v << "\n";
    // Step 4: stats on D
    double sum_log = 0, sum_log_sq = 0;
    for (int x : D) {
        double L = std::log2(x);
        sum_log    += L;
        sum_log_sq += L*L;
    }
    double X = sum_log / v;
  //  cout << "Sample Mean (X): " << X << "\n";
    double variance = (sum_log_sq / (v - 1)) - (X*X);
  //  cout << "Sample Variance: " << variance << "\n";
    double theta    = c_val * sqrt(variance);
   // cout << "Sample Std Dev (theta): " << theta << "\n";
    double X_prime  = X - (z_conf * theta / sqrt(v));
   // cout << "Lower Bound (X_prime): " << X_prime << "\n";

    // Step 5: binary search & final entropy
    double p = binary_search_p(X_prime, d, total_blocks);
   // cout << "p=" << p << "\n";


    double minEntropy;
    if (p <= 0) {
        minEntropy = 1.0;
    } else {
        minEntropy = -log2(p) / b;
    }
    return minEntropy;
};


/* to read  the raw binary file data.bin, 
*/

// vector<int> loadBlocks(const string& filename) {
//     // 1) Open the file
//     ifstream file(filename, std::ios::binary);
//     if (!file.is_open()) {
//         std::cerr << "Error: Could not open file " << filename << "\n";
//         return {};  // return an empty vector on error
//     }

//     // 2) Read up to 64 bytes
//     constexpr size_t MAX_BYTES = 10000; // 5 KB  
//     unsigned char buffer[MAX_BYTES];
//     file.read(reinterpret_cast<char*>(buffer), MAX_BYTES);
//     streamsize bytesRead = file.gcount();
//     if (bytesRead <= 0) {
//         cerr << "Error: No data read (file may be empty)\n";
//         return {};
//     }

//     // 3) Compute how many bits—and thus how many full b-bit blocks—we have
//     size_t totalBits = static_cast<size_t>(bytesRead) * 8;
//     size_t number_blocks = totalBits / b;   // any leftover bits at end are dropped

//     // 4) Unpack bit-by-bit into blocks
//     vector<int> blocks;
//     blocks.reserve(number_blocks);
//     for (size_t bi = 0; bi < number_blocks; ++bi) {
//         int blockVal = 0;
//         for (int bitPos = 0; bitPos < b; ++bitPos) {
//             size_t bitIndex = bi * b + bitPos;  
//             unsigned char byte = buffer[bitIndex / 8];
//             // extract the (7 - (bitIndex % 8))’th bit of that byte:
//             int bit = (byte >> (7 - (bitIndex % 8))) & 1;
//             blockVal = (blockVal << 1) | bit;
//         }
//         blocks.push_back(blockVal);
//     }


//     return blocks;
// }


/* to test the sample_data.txt file, uncomment the following function
*/
vector<int> loadBlocks(const string& filename) {
    ifstream file(filename);
    vector<int> blocks;
    string line;
    vector<int> bits;
    
    // 1) Read each text line
    while (getline(file, line)) {
        for (char c : line) {
            if (c == '0' || c == '1')
                bits.push_back(c - '0');
        }
    }
    // 2) Group into blocks of b bits
    cout << "bits size: " << bits.size() << "\n";
    size_t number_blocks = bits.size() / b;
    blocks.reserve(number_blocks);
    for (size_t i = 0; i < number_blocks; ++i) {
        int v = 0;
        for (int j = 0; j < b; ++j) {
            v = (v << 1) | bits[i*b + j];
        }
        blocks.push_back(v);
    }
    return blocks;
}

/* the command to compile: g++ .\comp_estimator.cpp -o .\comp.exe
*/

int main() {

    auto start = chrono::high_resolution_clock::now();
    // cout << "2^b = " << two_pow_b << "\n";

    //const string filename = "../data_sets/data.bin"; // to read the raw binary file data.bin
    //const string filename = "../data_sets/comp_NIST_example.txt"; // to read as string the sample_data.txt (example in NIST)
    const string filename = "../data_sets/160KB.txt"; // to read the synthetic data generated by the script
    auto blocks = loadBlocks(filename);
    if (blocks.empty()) {
        cerr << "No blocks loaded.\n";
        return 1;
    }

    // cout << "Total bit blocks read: " << blocks.size() << "\n";

    // only the first 100 blocks:
    size_t first_100 = 100;
    for (size_t i = 0; i < min(first_100, blocks.size()); ++i) {
        int val = blocks[i];
        // cout << "Block " << i 
        //           << ": int=" << val 
        //           << "  bits=" << bitset<b>(val)
        //           << "\n";
    }
    double min_entropy = compute_comp_min_entropy(blocks);
    cout << "Estimated min-entropy: " << min_entropy << "\n";
    auto end = chrono::high_resolution_clock::now();
    
    cout << "Time taken: " << chrono::duration<double>(end - start).count() << " seconds\n";

    return 0;
}