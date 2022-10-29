#include<iostream>

using namespace std;

//Parent Class
class Vehicle
{

    public:

        void honk()
        {
            cout << "This vehicle can honk!" << endl;
        }

};

//Child Class
class Car: public Vehicle 
{

// Keeping variables Private (Access Specifier)
private:

    string Name;
    string Model;
    int Year;

public:

    // Declaring a Constructor
    Car(string name, string model, int year)
    {
        Name = name;
        Model = model;
        Year = year;
    }

    // Usual Method Implemented
    void carInfo()
    {
        cout << "This is " << Name << " having model " << Model << " of the year " << Year << endl;
    }

    // Method for Encapsulation
    string getName()
    {
        return Name;
    }

    void setName(string name)
    {
        Name = name;
    }

    // Method implemented for different action, Polymorphism
    void honk(){
        cout << "The " << Name << " makes a sound BEEEP !" << endl;
    }
};

int main()
{
    // Example for Class COnstructor use
    Car c1 = Car("BMW", "X5", 2012);
    Car c2 = Car("BMW", "X7", 2018);
    Car c3 = Car("Ford", "Mustang", 2015);

    // Encapsulation
    c1.setName("BWM");

    // Usual Class Method
    c1.carInfo();
    c2.carInfo();
    c3.carInfo();

    //Inheritance and Polymorphism
    c1.honk();

    return 0;
}