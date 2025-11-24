// ahmso698: Samarbetat med ahmha095, Ahmed Hadid, samma program
#include<iomanip>
#include<string>
#include<iostream>
#include<vector>
#include<algorithm>

using namespace std;

struct runner
{
    string firstname;
    string lastname;
    string club;      
    vector<double> times{};    
};

runner find_fastest(vector<runner>& fixvec)
{
    runner shortestrunner;
    double shortesttime{0};
    int deleteat;

    for (int i = 0; i < fixvec.size(); i++)
    {
        if (i == 0)
        {
            shortestrunner = fixvec.at(0);
            shortesttime = fixvec.at(0).times.at(0);
            deleteat = 0;
        }
        else
        {
            if (fixvec.at(i).times.at(0) < shortesttime)
            {
                shortestrunner = fixvec.at(i);
                shortesttime = fixvec.at(i).times.at(0);
                deleteat = i;
            };  
        };  
    };
    fixvec.erase(fixvec.begin()+deleteat);
    return shortestrunner;
}

void sortvec(vector<runner> & sortvec)
{
    vector<runner> tempvec{};
    vector<runner> copyvec;
    copyvec = sortvec;

    for (runner& r : copyvec)
    {
        sort(begin(r.times),end(r.times));
    };
    
    for (size_t i = 0; i < sortvec.size(); i++)
    {
        tempvec.push_back(find_fastest(copyvec));
    };
    
    sortvec = tempvec;
    
}

void print(vector<runner> const& runvec)
{
   for(runner r : runvec)
    {
        cout << setw(9) << r.lastname << setw(10) << r.firstname << setw(16) << r.club << ":";
        for (double t : r.times)
        {
            cout << " " << fixed << setprecision(2) << t;
        };
        
        cout << endl;
    };
}

void get_runners(string const& info, vector<runner>& runvec)
{
    runner person;
    string cname;

    person.firstname = info;
    cin >> person.lastname;
    getline(cin,cname); //bruh
    person.club = cname;
    person.times = {};

    runvec.push_back(person);
}

void get_time(runner& run)
{
    double time;

    while(true)
    {
        cin >> time;

        if(time == -1.00)
        {
            break;
        };

        run.times.push_back(time);
    };
}


int main()
{   
    string fname{0}; 
    cout << "Mata in deltagare:" << endl;

    vector<runner> runners{};
    while(true)
    {
        cin >> fname;
        if(fname == "KLAR")
        {
            break;
        }
    
        get_runners(fname,runners);
    };

    for(runner& r : runners)
    {   
        cout << "Tider " << r.firstname << ": ";
        get_time(r);
    };

    cout << "Efternamn   Förnamn           Klubb: Tider" << endl;
    cout << "==========================================" << endl;
    sortvec(runners);
    print(runners);
}