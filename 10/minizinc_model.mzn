include "globals.mzn";

% Data
int: num_row;
int: num_col;
array[1..num_row, 1..num_col] of int: matrix;
int: path_length;

predicate is_adj(Coord: c1, Coord: c2) =
	abs(c1.row - c2.row) = 1 /\ (c1.column - c2.column) = 0 \/
    abs(c1.column - c2.column) = 1 /\ (c1.row - c2.row) = 0;

% Variables
type Coord = record(var 1..num_row: row, var 1..num_col: column);
array[1..path_length] of var Coord: path;

% Constraints
constraint
  forall(i in 1..path_length) (
    matrix[path[i].row, path[i].column] = i - 1
  );

constraint
  forall(i in 1..path_length-1) (
    is_adj(path[i], path[i+1])
  );

solve::int_search([ if c == 1 then path[i].row else path[i].column endif | i in 1..path_length, c in 1..2 ], input_order, indomain_min) satisfy;

output ["(" ++ show(path[i].row) ++ ", " ++ show(path[i].column) ++ ")" ++ "  " ++ show(matrix[path[i].row, path[i].column]) ++ "\n" | i in 1..path_length];

