#include "Vehicle.h"
#include <iostream>
#include <string>

Vehicle::Vehicle(){
  make = "COP3503";
  model = "Rust Bucket";
  year = 1900;
  price = 0;
  mileage = 0;
}

Vehicle::Vehicle(std::string make1, std::string model1, int year1, int price1, int mileage1) {
  make = make1;
  model = model1;
  year = year1;
  price = price1;
  mileage = mileage1; 
}

void Vehicle::Display() {
  std::cout << year << make << model << price << mileage << std::endl;
}

std::string Vehicle::GetYearMakeModel(){
  return std::to_string(year) + make + model;
}

int Vehicle::GetPrice() {
  return price;
}

Showroom::Showroom(std::string name1, unsigned int capacity1){
  name = name1;
  capacity = capacity1;
}

std::vector<Vehicle> Showroom::GetVehicleList(){
  return vehicles;
}

void Showroom::AddVehicle(Vehicle vehicle1){ 
  if (vehicles.size() <= capacity) {
    vehicles.push_back(vehicle1);
  }
  else{
    std::cout << "Showroom is full! Cannot add " << vehicle1.GetYearMakeModel() << std::endl;  
  }
}

void Showroom::ShowInventory() {
  for (int i = 0; i < vehicles.size(); i++){
    vehicles[i].Display();
  }
}

int Showroom::GetInventoryValue(){
  int total = 0;
  for (int i = 0; i < vehicles.size(); i++){
    total += vehicles[i].GetPrice();
  return total;
  }
}
Dealership::Dealership(std::string name1, unsigned int capacity1){
  name = name1;
  capacity = capacity1;
}

void Dealership::addShowRoom(Showroom showroom1){
  if (showrooms.size() <= capacity){
    showrooms.push_back(showroom1)
  }
  else{
    std::cout << "Dealership is full, can't add another showroom!" std::endl
  }
}
float Dealership::GetAveragePrice(){
  float toal=0;
  int count = 0;

  for (int i = 0; i < showrooms.size(); i++){
    std::vector<Vehicle> vehicle_list = showrooms[i].GetVehicleList()
    for (int j = 0; j < showrooms.size(); j++){
      total+= vlist[j].GetPrice();
      count += 1;
    }
  
  if (count = 0){
    return 0
  }
  float avg = total/count;
  return avg
  }
}

void Dealership::ShowInventory() {
  if (showrooms.size() > 0){
    for (int i=0; i < showrooms.size(); i+=1) {
      showrooms[i].ShowInventory

      std::cout << "Average car price: $" << GetAveragePrice() << std:endl;
    }
  }
  else{
    std::cout << name <<" is empty!" << std::endl;
    std::cout << "Average car price: $0.00" << std:endl;
  }
}


#include <string>
#include <vector>

class Vehicle{
  std::string make;
  std::string model;

  int year;
  float price; 
  int mileage;

public:
  Vehicle();
  Vehicle(std::string make, std::string model, int year, int price, int mileage);

  void Display();
  std::string GetYearMakeModel();
  int GetPrice();
};

class Showroom {
  std::string name;
  std::vector<Vehicle> vehicles;
  unsigned int capacity;
public:
  Showroom(std::string name = "Unamed Showroom", unsigned int capacity = 0);
  std::vector<Vehicle> GetVehicleList();
  void AddVehicle(Vehicle v);
  void ShowInventory();
  int GetInventoryValue();

};

class Dealership {
  std::string name;
  std::vector<Showroom> showroooms;
  unsigned int capacity;
public:
  Dealership(std::string name = "Generic Dealership", unsigned int capacity = 0);
  
  void AddShowroom(Showroom s);
  float GetAveragePrice();
  void ShowInventor();

};