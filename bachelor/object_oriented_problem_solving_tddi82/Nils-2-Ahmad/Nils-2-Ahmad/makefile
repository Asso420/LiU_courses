FLAGS = -std=c++17 -Wall -Wextra
LIBS = -lsfml-graphics -lsfml-audio -lsfml-window -lsfml-system
OBJDIR := objdir
OBJS = $(OBJDIR)/main.o $(OBJDIR)/Manager.o $(OBJDIR)/Game_state.o $(OBJDIR)/Game.o $(OBJDIR)/Menu_state.o $(OBJDIR)/End_state.o $(OBJDIR)/Player.o $(OBJDIR)/Wall.o $(OBJDIR)/Object.o $(OBJDIR)/Barrel.o $(OBJDIR)/Bomb.o $(OBJDIR)/Abilities.o $(OBJDIR)/Enemy.o $(OBJDIR)/ZigZagEnemy.o $(OBJDIR)/ChaseEnemy.o
CCPATH = implemetation_files



game.out: $(OBJS)
	g++ $(FLAGS) -o ./game.out $(OBJS) $(LIBS)
$(OBJDIR)/main.o: $(CCPATH)/main.cc dir
	g++ -c $(CCPATH)/main.cc -o $(OBJDIR)/main.o
$(OBJDIR)/Player.o: $(CCPATH)/Player.cc dir
	g++ -c $(CCPATH)/Player.cc -o $(OBJDIR)/Player.o
$(OBJDIR)/Wall.o: $(CCPATH)/Wall.cc dir
	g++ -c $(CCPATH)/Wall.cc -o $(OBJDIR)/Wall.o
$(OBJDIR)/Object.o: $(CCPATH)/Object.cc dir
	g++ -c $(CCPATH)/Object.cc -o $(OBJDIR)/Object.o
$(OBJDIR)/Manager.o: $(CCPATH)/Manager.cc dir
	g++ -c $(CCPATH)/Manager.cc -o $(OBJDIR)/Manager.o
$(OBJDIR)/Game_state.o: $(CCPATH)/Game_state.cc dir
	g++ -c $(CCPATH)/Game_state.cc -o $(OBJDIR)/Game_state.o
$(OBJDIR)/Game.o: $(CCPATH)/Game.cc dir
	g++ -c $(CCPATH)/Game.cc -o $(OBJDIR)/Game.o
$(OBJDIR)/Menu_state.o: $(CCPATH)/Menu_state.cc dir
	g++ -c $(CCPATH)/Menu_state.cc -o $(OBJDIR)/Menu_state.o
$(OBJDIR)/End_state.o: $(CCPATH)/End_state.cc dir
	g++ -c $(CCPATH)/End_state.cc -o $(OBJDIR)/End_state.o
$(OBJDIR)/Barrel.o: $(CCPATH)/Barrel.cc dir
	g++ -c $(CCPATH)/Barrel.cc -o $(OBJDIR)/Barrel.o
$(OBJDIR)/Bomb.o: $(CCPATH)/Bomb.cc dir
	g++ -c $(CCPATH)/Bomb.cc -o $(OBJDIR)/Bomb.o
$(OBJDIR)/Abilities.o: $(CCPATH)/Abilities.cc dir
	g++ -c $(CCPATH)/Abilities.cc -o $(OBJDIR)/Abilities.o
$(OBJDIR)/Enemy.o: $(CCPATH)/Enemy.cc dir
	g++ -c $(CCPATH)/Enemy.cc -o $(OBJDIR)/Enemy.o
$(OBJDIR)/ZigZagEnemy.o: $(CCPATH)/ZigZagEnemy.cc dir
	g++ -c $(CCPATH)/ZigZagEnemy.cc -o $(OBJDIR)/ZigZagEnemy.o
$(OBJDIR)/ChaseEnemy.o: $(CCPATH)/ChaseEnemy.cc dir
	g++ -c $(CCPATH)/ChaseEnemy.cc -o $(OBJDIR)/ChaseEnemy.o	
dir:
	@mkdir -p $(OBJDIR)
.PHONY: all clean
all: clean game.out run
clean:
	@ \rm -rf ./objdir/*.o *.gch *.out core
run: game.out
	./game.out
