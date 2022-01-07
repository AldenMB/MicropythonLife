
// Upon instantiation: 
// store the size (width by height)
// allocate an array of uint_least8_t, initialized to zero
typedef index unsigned int;
typedef cell uint8_t;
struct life {
	index I, J;
	cell board[];
};

// provide an interface to set and get them
bool cell_at(life const *l, index i, index j){
	return l->board[i][j];
}
void cell_set(life *l, index i, index j, bool value){
	l->board[i][j] = value;
}

// provide a function to loop through, putting the next state in the 2s place (second least significant bit). Then shift all the bits.
void step(life *l){
	index I = l->I;
	index J = l->J;
	cell board[] = l->board;
	for(index i=0; i < I; ++i){
		for(index j=0; j < J; ++j){
			uint8_t sum = 0;
			for(int8_t dx = -1; dx < 2; ++dx){
				for(int8_t dy = -1; dy < 2; ++dy){
					sum += board[(i+dx)%I][(j+dy)%J] & 1;
				}
			}
			// Wikipedia:
			// if the sum of all nine fields in a given neighbourhood is three,
			// the inner field state for the next generation will be life; 
			// if the all-field sum is four, the inner field retains its current state;
			// and every other sum sets the inner field to death. 
			if(sum == 3){
				board[i][j] |= (1 << 1);
			}
			else if(sum == 4){
				board[i][j] |= (board[i][j] << 1);
			}
		}
	}
	for(index i=0; i < I; ++i){
		for(index j=0; j < J; ++j){
			board[i][j] >>= 1;
		}
	}
}

// bonus: provide a function to compare two instances
bool all_same(life const *a, life const *b){
	if (a->I != b->I){
		return false;
	}
	if (a->J != b->J){
		return false;
	}
	for(index i=0; i < a->I; ++i){
		for(index j=0; j < a->J; ++j){
			if(a->board[i][j] != b->board[i][j]){
				return false;
			}
		}
	}
	return true;
}