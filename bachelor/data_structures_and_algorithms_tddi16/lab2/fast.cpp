#include "image.h"
#include "window.h"
#include "load.h"
#include <chrono>
#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

using std::cout;
using std::cerr;
using std::endl;
using std::string;
using std::vector;
using std::unordered_map;

/**
 * Class that stores a summary of an image.
 *
 * This summary is intended to contain a high-level representation of the
 * important parts of an image. I.e. it shall contain what a human eye would
 * find relevant, while ignoring things that the human eye would find
 * irrelevant.
 *
 * To approximate human perception, we store a series of booleans that indicate
 * if the brightness of the image has increased or not. We do this for all
 * horizontal lines and vertical lines in a downsampled version of the image.
 *
 * See the lab instructions for more details.
 *
 * Note: You will need to use this data structure as the key in a hash table. As
 * such, you will need to implement equality checks and a hash function for this
 * data structure.
 */
class Image_Summary {
public:
    // Horizontal increases in brightness.
    vector<bool> horizontal;

    // Vertical increases in brightness.
    vector<bool> vertical;
public:
    bool operator==(const Image_Summary& other) const
    {
        if(horizontal == other.horizontal && vertical == other.vertical)
        {
            return true;
        }
        else return false;
    }
};

namespace std
{
    template <>
    struct hash<Image_Summary>
    {
        size_t operator()(const Image_Summary &to_hash) const
        {
            size_t hash {0};
            /*
            size_t horizontal_hash_one {0};
            size_t horizontal_hash_two {0};
            size_t vertical_hash_one {0};
            size_t vertical_hash_two {0};
            size_t horizontal_hash {0};
            size_t vertical_hash {0};

            for (int i = 0; i < to_hash.horizontal.size() /2; i++)
            {
                horizontal_hash_one = (horizontal_hash_one << 1) | size_t(to_hash.horizontal[i]);
            }
            for (int i = to_hash.horizontal.size() / 2; i < to_hash.horizontal.size(); i++)
            {
                horizontal_hash_two = (horizontal_hash_two << 1) | size_t(to_hash.horizontal[i]);
            }

            horizontal_hash = horizontal_hash_one ^ horizontal_hash_two;
            for (int i = 0; i < to_hash.vertical.size() /2; i++)
            {
                vertical_hash_one = (vertical_hash_one << 1) | size_t(to_hash.vertical[i]);
            }
            for (int i = to_hash.horizontal.size() / 2; i < to_hash.horizontal.size(); i++)
            {
                vertical_hash_two = (vertical_hash_two << 1) | size_t(to_hash.vertical[i]);
            }
            vertical_hash = vertical_hash_one ^ vertical_hash_two;
            hash = horizontal_hash ^ vertical_hash;
            */
           for(size_t i = 0; i < to_hash.horizontal.size(); i++)
           {
                hash = (hash << 1) ^ size_t(to_hash.horizontal[i]);
           }
            for(size_t i = 0; i < to_hash.vertical.size(); i++)
           {
                hash = (hash << 1) ^ size_t(to_hash.vertical[i]);
           }
            return hash;
        }
    };
}

// Compute an Image_Summary from an image. This is described in detail in the
// lab instructions.
Image_Summary compute_summary(const Image &image) {
    const size_t summary_size = 8;
    Image_Summary result;
    //Image shrunk{image};
    Image shrunk = image.shrink(summary_size +1, summary_size+1);
     for(size_t y = 0; y < shrunk.height(); y++){
        for(size_t  x = 0; x < shrunk.width() -1; x++){
            result.horizontal.push_back(shrunk.pixel(x+1, y).brightness() > shrunk.pixel(x,y).brightness());
            result.vertical.push_back(shrunk.pixel(x, y+1).brightness() > shrunk.pixel(x,y).brightness());
        }
    }   

    // TODO: Finish the implementation.
    // The lines below are here to avoid warnings. They can be removed.
    //(void)image;
    //(void)summary_size;

    return result;
}

int main(int argc, const char *argv[]) {
    WindowPtr window = Window::create(argc, argv);

    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " [--nopause] [--nowindow] <directory>" << endl;
        cerr << "Missing directory containing files!" << endl;
        return 1;
    }

    vector<string> files = list_files(argv[1], ".jpg");
    cout << "Found " << files.size() << " image files." << endl;

    if (files.size() <= 0) {
        cerr << "No files found! Make sure you entered a proper path!" << endl;
        return 1;
    }

    auto begin = std::chrono::high_resolution_clock::now();

    /**
     * TODO:
     * - For each file:
     *   - Load the file
     *   - Compute its summary
     */
    window->show_single("Loading images...", load_image(files[0]), false);
    unordered_map<Image_Summary, vector<string>> image_summaries;
    for (const auto &file : files)
    {
        Image_Summary summary = compute_summary(load_image(file));
        image_summaries[summary].push_back(file);
    }

    auto end = std::chrono::high_resolution_clock::now();
    cout << "Total time: "
         << std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count()
         << " milliseconds." << endl;

    /**
     * TODO:
     * - Display sets of files with equal summaries
     */
        for (const auto &entry : image_summaries) {
        const vector<string> &duplicateFiles = entry.second;

        if (duplicateFiles.size() > 1) {
            window -> report_match(duplicateFiles);
        }
    }

    return 0;
}
