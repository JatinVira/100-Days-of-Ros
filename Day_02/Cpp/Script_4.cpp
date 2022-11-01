#include<iostream>

using namespace std;

class myClass
{
    public:
        int age;
        string name;

        void myMethod()
        {
            cout << "Hello, my age is " << age << " and my name is " << name << endl;
        }

        myClass(int Age, string Name)
        {
            age = Age;
            name = Name;
        }
};

int main()
{

    myClass testClass1 = myClass(21,"Jatin");
    testClass1.myMethod();

    return 0;
}