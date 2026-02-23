include "globals.mzn";

int: grid_size;
int: num_byte;
array[1..num_byte, 1..2] of int: byte;

int: max_path_len = grid_size * grid_size;

type Coord = record(var -1..grid_size: row, var -1..grid_size: col);
array[1..(max_path_len)] of var Coord: path;

% -------------------- PREDICATES --------------------
predicate is_null_coord(Coord: c) =
	c.row = -1 \/ c.col = -1;

predicate is_adj(Coord: c1, Coord: c2) =
	abs(c1.row - c2.row) = 1 /\ (c1.col - c2.col) = 0 \/
    abs(c1.col - c2.col) = 1 /\ (c1.row - c2.row) = 0;

% -------------------- CONSTRAINTS --------------------
% No coordinate containing a single -1
constraint
	forall(i in 1..max_path_len) (
		(path[i].row * path[i].col >= 0)
	);

% Null coordinates only at the end
constraint
	forall(i in 1..max_path_len)(
		if is_null_coord(path[i]) then
			forall(j in i + 1..max_path_len)(
				is_null_coord(path[j])
			)
		endif
	);

% No null coordinate before valid coordinate
constraint
	forall(i in 2..max_path_len)(
		if not is_null_coord(path[i]) then
			not is_null_coord(path[i - 1])
		endif
	);

% Start at top left and end at bottom right
constraint
	path[1].row = 0 /\ path[1].col = 0;

constraint
  exists(i in 1..max_path_len) (
    path[i].row = grid_size /\ path[i].col = grid_size
  );

constraint
	forall(i in 1..max_path_len - 1) (
		if path[i].row = grid_size /\ path[i].col = grid_size then
			is_null_coord(path[i + 1])
		endif
	);

% Coordinates must be adjacent
constraint
	forall(i in 1..max_path_len - 1) (
		if not is_null_coord(path[i]) /\ not is_null_coord(path[i + 1]) then
			is_adj(path[i], path[i + 1])
		endif
	);

/*
% Coordinates can't be a corrupted byte
constraint
	forall(i in 1..max_path_len) (
		not table([path[i].row, path[i].col], byte)
	);
 

% Coordinates must be unique
array[1..max_path_len] of var int: hash;

constraint
	forall(i in 1..max_path_len)(
		hash[i] =
			if path[i].row = -1 then 0
			else path[i].row * (grid_size + 1) + path[i].col + 1
			endif
	);

constraint
    alldifferent_except_0(hash);
*/

% -------------------- SOLVE --------------------
% Maximize number of null coordinate
% solve::int_search([ if c == 1 then path[i].row else path[i].col endif | i in 1..max_path_len, c in 1..2 ], input_order, indomain_min) maximize sum([is_null_coord(path[i]) | i in 1..max_path_len]);

solve::int_search([ if c == 1 then path[i].row else path[i].col endif | i in 1..max_path_len, c in 1..2 ], input_order, indomain_min) satisfy;

output ["(" ++ show(path[i].row) ++ ", " ++ show(path[i].col) ++ ")" ++ "\n" | i in 1..max_path_len where fix(path[i].row) != -1 /\ fix(path[i].col) != -1];
	
	
	

  
  
  
  
  
  
  