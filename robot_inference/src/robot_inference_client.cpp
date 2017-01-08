#include "ros/ros.h"
#include "robot_inference/Inference.h"
#include <cstdlib>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>

using namespace std;

vector<int> load_observations(string filename)
{
  vector<int> observations;
  ifstream fin;
  fin.open(filename.c_str());
  if (fin.fail())
  {
    throw invalid_argument("fail to open the file");
  }
  for (int i = 0; fin.good(); i++)
  {
    stringstream linestream;
    string line;
    getline(fin, line);
    // skip meanlingless lines 
    if (line[0] == ' ' || line == "")
    {
      i--;
      continue;
    }
    linestream << line;
    int x,y;
    linestream >> x >> y;
    observations.push_back(x);
    observations.push_back(y);
    linestream.clear();
  }
  fin.close();
  return observations;
}

string mapping(int val)
{ 
  if (val == 4) return "right";
  else if (val == 3) return "left";
  else if (val == 1) return "up";
  else if (val == 2) return "down";
  else return "stay";
}

// define my own function to convert from int to string in ros standard c++03
string convert(int num)
{
  ostringstream convert;
  convert << num;
  return convert.str();
}

int main(int argc, char *argv[])
{
  ROS_INFO("file name of observations (put in the same folder)");
  ros::init(argc, argv, "robot_inference_client");
  if (argc < 2)
  {
    ROS_INFO("infer robot behavior from observations");
    return 1;
  }

  ros::NodeHandle n;
  ros::ServiceClient client = n.serviceClient<robot_inference::Inference>("inference");
  robot_inference::Inference srv;
  string filename = argv[1];
  vector<int> observations;
  try
  {
    observations = load_observations("test.txt");
  }
  catch(const invalid_argument& e)
  {
    ROS_ERROR("Invalid observation file");
    return 1;
  } 
  srv.request.observation = observations;

  if (client.call(srv))
  {
    vector<int> inference = srv.response.inference;
    string display = "\n";
    for (int i = 0; i < inference.size() / 3; i++)
    {
      display += "(" + convert(inference[3 * i]) + ", " + convert(inference[3 * i + 1]) + "), ";
      display += mapping(inference[3 * i + 2]) + "\n";
    }
    ROS_INFO("%s", display.c_str());
  }
  else
  {
    ROS_ERROR("Failed to call service robot_inference");
    return 1;
  }

  return 0;
}

