#include <iostream>
#include <fstream>
#include <string>
#include <deque>
#include <vector>
#include <cstdlib>
using namespace std;

/* Number of food pellets that must be eaten to win. */
const int kMaxFood = 20;

/* Constants for the different tile types. */
const char kEmptyTile = ' ';
const char kWallTile = '#';
const char kFoodTile = '$';
const char kSnakeTile = '*';

const char* kMapFileName = "map.txt";

/* A struct encoding a point in a two-dimensional grid. */
struct pointT {
    int row, col;
};

/* A struct containing relevant game information. */
struct gameT {
    vector<string> world; // The playing field
    int numRows, numCols; // Size of the playing field
    deque<pointT> snake; // The snake body
    int dx, dy; // The snake direction
    int numEaten; // How much food we've eaten.
};

void printVector(deque<pointT>& v){
    cout << "deque size:" << v.size() << endl;
    deque<pointT>::const_iterator it = v.begin();
    for (it; it != v.end(); ++it){
        cout << it->row << "," << it->col << " ";
    }

    cout << endl;
}

void addSnakeTile(gameT &game, int row) {
    int col = game.world[row].find(kSnakeTile);
    if(col != string::npos) {
        pointT head;
        head.row = row;
        head.col = col;
        game.snake.push_back(head);
    }
}

void LoadWorld(gameT& game, ifstream& input) {
    input >> game.numRows >> game.numCols;
    cout << "Reading number of rows:" << game.numRows << ",number of columns:" << game.numCols << endl;
    game.world.resize(game.numRows);
    input >> game.dx >> game.dy;
    cout << "Reading start point of snake, x:" << game.dx << ",y:" << game.dy << endl;
    cout << "Loading map data ..." << endl;
    for(int row = 0; row < game.numRows; ) {
        string tempStr;
        getline(input, tempStr);
        if (string::npos != tempStr.find(kWallTile)) {
            game.world[row] = tempStr; 
            cout << game.world[row] << endl;
            addSnakeTile(game, row);
            row++;
        }
    }
    game.numEaten = 0;
}

void InitializeGame(gameT& game) {
    ifstream input;

    srand(static_cast<unsigned int>(time(NULL)));
    cout << "Try to load map from file: " << kMapFileName <<endl;;
    input.open(kMapFileName, std::ifstream::in);
    if (!input.is_open()){
        cout << "Failed to open map file" << endl;
    }
    LoadWorld(game, input);
    printVector(game.snake);
}

const double kWaitTime = 0.5; // Pause 0.1 seconds between frames
void Pause() {
    clock_t startTime = clock(); // clock_t is a type which holds clock ticks.
    while(static_cast<double>(clock() - startTime) / CLOCKS_PER_SEC < kWaitTime);
}

const string kClearCommand = "clear";
void PrintWorld(gameT& game) {
    system(kClearCommand.c_str());
    for(int row = 0; row < game.numRows; ++row)
        cout << game.world[row] << endl;
    cout << "Food eaten: " << game.numEaten << endl;
}

void DisplayResult(gameT& game) {
    PrintWorld(game);
    if(game.numEaten == kMaxFood)
        cout << "The snake ate enough food and wins!" << endl;
    else
        cout << "Oh no! The snake crashed!" << endl;
}

bool InWorld(pointT& pt, gameT& game) {
    return pt.col >= 0 && pt.row >= 0 && pt.col < game.numCols && pt.row < game.numRows;
}

bool Crashed(pointT headPos, gameT& game) {
    return !InWorld(headPos, game) || game.world[headPos.row][headPos.col] == kSnakeTile || 
                 game.world[headPos.row][headPos.col] == kWallTile;
}

bool RandomChance(double probability) {
    return (rand() / (RAND_MAX + 1.0)) < probability;
}

pointT GetNextPosition(gameT& game, int dx, int dy){
    pointT result = game.snake.front();
    result.row += dy;
    result.col += dx;
    return result;
}

const double kTurnRate = 0.2; // 20% chance to turn each step.
void PerformAI(gameT& game) {
    
    /* Figure out where we will be after we move this turn. */
    pointT nextHead = GetNextPosition(game, game.dx, game.dy);
    /* If that hits a wall or we randomly decide to, turn the snake. */
    if(Crashed(nextHead, game) || RandomChance(kTurnRate)) {
        int leftDx = -game.dy;
        int leftDy = game.dx;
        int rightDx = game.dy;
        int rightDy = -game.dx;
        /* Check if turning left or right will cause us to crash. */
        bool canLeft = !Crashed(GetNextPosition(game, leftDx, leftDy), game);
        bool canRight = !Crashed(GetNextPosition(game, rightDx, rightDy), game);

        bool willTurnLeft = false;
        if(!canLeft && !canRight)
            return; // If we can't turn, don't turn.
        else if(canLeft && !canRight)
            willTurnLeft = true; // If we must turn left, do so.
        else if(!canLeft && canRight)
            willTurnLeft = false; // If we must turn right, do so.
        else
            willTurnLeft = RandomChance(0.5); // Else pick randomly

        game.dx = willTurnLeft? leftDx : rightDx;
        game.dy = willTurnLeft? leftDy : rightDy;
    }
}

void PlaceFood(gameT& game) {
    while(true) {
         int row = rand() % game.numRows;
         int col = rand() % game.numCols;
         /* If the specified position is empty, place the food there. */
        if(game.world[row][col] == kEmptyTile) {
            game.world[row][col] = kFoodTile;
            return; 
        }
    }   
} 

bool MoveSnake(gameT& game) {
    pointT nextHead = GetNextPosition(game, game.dx, game.dy);
    if(Crashed(nextHead, game))
        return false;
    bool isFood = (game.world[nextHead.row][nextHead.col] == kFoodTile);
    game.world[nextHead.row][nextHead.col] = kSnakeTile;
    game.snake.push_front(nextHead);
    if(!isFood) {
         game.world[game.snake.back().row][game.snake.back().col] = kEmptyTile;
         game.snake.pop_back();
    } else {
         ++game.numEaten;
        PlaceFood(game);
    }
    return true;
}

void RunSimulation(gameT& game) {
    /* Keep looping while we haven't eaten too much. */
    while(game.numEaten < kMaxFood) {
        PrintWorld(game); // Display the board
        PerformAI(game); // Have the AI choose an action
        if(!MoveSnake(game)) // Move the snake and stop if we crashed.
            break;
        Pause(); // Pause so we can see what's going on.
    }
    //DisplayResult(game); // Tell the user what happened
}

/* The main program. Initializes the world, then runs the simulation. */
int main() {
    gameT game;
    InitializeGame(game);
    RunSimulation(game);
    return 0;
}
