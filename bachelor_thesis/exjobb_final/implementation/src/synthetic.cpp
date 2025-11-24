
#include <fstream>
#include <vector>
#include <random>
#include <cmath>
#include <fstream>
#include <vector>
#include <random>
#include <cmath>
using namespace std;
int main() {
    const int L_bits =  1310720;           // adjust as ne
    const double H_target = 0.95;          // byt till känd entropy (bits)

    // Compute max-probability (0)
    double p_max = std::pow(2.0, -H_target);

    // bit (1) är 1 - p_max
    double p_rest = 1.0 - p_max;

    // Bernoulli distribution
    std::random_device rd;
    std::mt19937_64 rng(rd());
    std::bernoulli_distribution dist(p_max);

    std::vector<int> seq(L_bits);
    for (int i = 0; i < L_bits; ++i) {
        seq[i] = dist(rng) ? 0 : 1;
    }

    // Write the bit sequence to file
    std::ofstream out("../data_sets/160KB.txt");
    for (int bit : seq) {
        out << bit << '\n';
    }
    out.close();

    return 0;
}





// vector<int> generate_synthetic_sequence(int n, double noise_strength, int length) {
//     // 1. Create 2^n probabilities (near-uniform)
//     int num_symbols = 1 << n; // 2^n possible n-bit symbols
//     vector<double> probs(num_symbols, 1.0 / num_symbols);
//     cout << "probs[0]: " << probs[0] << endl;
//     cout << "probs[1]: " << probs[1] << endl;  
//     cout << "probs[2]: " << probs[2] << endl;


//     double p_max_uniform = *max_element(probs.begin(), probs.end());
//     cout << "p_max_uniform: " << p_max_uniform << endl;
//     double min_entropy_uniform = -log2(p_max_uniform);
//     cout << "True min-entropy: " << min_entropy_uniform / n << " bits\n";

//     // 2. Add Gaussian noise (avoid negative probabilities)
//     random_device rd;
//     mt19937 gen(rd());
//     normal_distribution<double> noise(0.0, noise_strength);
    
//     for (auto& p : probs) {
//         p += noise(gen);
//         if (p < 0) p = 0; // Clamp to 0
//     }

//     // 3. Renormalize
//     double sum = accumulate(probs.begin(), probs.end(), 0.0);
//     for (auto& p : probs) p /= sum;

//     // 4. Compute true min-entropy
//     double p_max = *max_element(probs.begin(), probs.end());
//     double min_entropy = -log2(p_max);
//     cout << "p_max: " << p_max << endl;
//     cout << "min-entropy after adding noice: " << min_entropy / n << " bits\n";

//     // 5. Generate a binary sequence by sampling symbols
//     discrete_distribution<int> dist(probs.begin(), probs.end());
//     vector<int> sequence;
//     for (int i = 0; i < length; ++i) {
//         int symbol = dist(gen);
//         // Convert symbol to n-bit binary (for binary input to MultiMCW)
//         for (int j = n - 1; j >= 0; --j) {
//             sequence.push_back((symbol >> j) & 1);
//         }
//     }

//     return sequence;
// }

// int main() {
//     int n = 8;            
//     double noise_strength = 0.003; // Controls min-entropy (higher = less uniform)
//     int length = 1000;       // Output sequence length in bytes

//     vector<int> sequence = generate_synthetic_sequence(n, noise_strength, length);

//     // Save to file for testing
//     ofstream out("../data_sets/synthetic_data_1.txt", ios::binary);
//     for (int bit : sequence) {
//         out.put(bit ? '1' : '0');
//     }
//     out.close();

//     cout << "Generated " << sequence.size() << " bits." << endl;
//     return 0;
// }







