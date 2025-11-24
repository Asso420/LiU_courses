// ahmso698: Samarbetat med ahmha095, Ahmed Hadid, samma program

#include<iomanip>
#include<string>
#include<iostream>
#include<cmath>

using namespace std;

int nfactorial(int const val)
{
    int result{1};
    for(int i = 1; i<=val; i++){
        result *= i;
        }
    return result;
}

string mulstring(string const& w, int const m) 
{
    string mulw{""};
    for(int i{0}; i < m; i++)
    {
        mulw += w;
    };
    return mulw;
}

void swaptype(int& number, double& decimal)
{   
    double copy{0};   
    copy = decimal;
    decimal = number;
    number = ceil(copy); 
}

void calcstring(string const& fw,string const& sw,int& totall, double& meanl)
{
    int fwlenght; 
    int swlenght; 
    fwlenght = fw.size();
    swlenght = sw.size();
    totall = fwlenght + swlenght; 
    meanl = static_cast<double>(totall)/2;

}

void val1()
{
    int n;
    cout << "Mata in ett heltal: ";
    cin >> n;
    cout << "Fakulteten av " << n << " är " << nfactorial(n) << endl;
}

void val2()
{
    string word;
    int amount;
    cout << "Mata in en text och ett heltal: ";
    cin >> word;
    cin >> amount;
    cout << "Den multiplicerade texten är " << mulstring(word,amount) << endl;
}

void val3()
{
    int num;
    double dub;
    cout << "Mata in ett heltal och ett flyttal: ";
    cin >> num;
    cin >> dub;
    swaptype(num,dub);
    cout << "Heltalets värde är nu " << num << endl;
    cout << "Flyttalets värde är nu " << fixed << setprecision(1) << dub << endl;
}

void val4()
{
    string text1;
    string text2;
    int totallenght{0};
    double meanlenght{0};

    cout << "Mata in två ord: ";
    cin >> text1;
    cin >> text2;

    calcstring(text1,text2,totallenght,meanlenght);
    cout << "Totallängd: " << totallenght << endl;
    cout << "Medellängd: " << fixed << setprecision(1) << meanlenght << endl;
}

void menu(int& choice)
{
    while(true)
    { 
        cout << "1. Beräkna N-fakultet." << endl;
        cout << "2. Multiplicera en sträng." << endl;
        cout << "3. Byta värden på ett heltal och ett flyttal." << endl;
        cout << "4. Beräkna totala längden samt medellängden på två strängar." << endl;
        cout << "5. Avsluta programmet." << endl;
        cout << "Val: ";
        cin >> choice;
        if (choice<1 || choice>5 )
        {
            cout << "Fel val!" << endl;
        }
        else
       {
        break;
       }    
    } 
}


int main()
{   
    int choice{0};
    bool running{true}; 
    cout << "Välkommen till huvudmenyn!" << endl;
    while(running)
   { 
        menu(choice);
        if (choice == 1)
        {
           val1();
        }
        else if (choice == 2)
        {
           val2();
        }
        else if(choice == 3)
        {
            val3();
        }
        else if(choice == 4)
        {
            val4();
        }
        else if(choice == 5)
        {
            running = false;
            cout << "Ha en bra dag!" << endl;
        }
       
     } 
}