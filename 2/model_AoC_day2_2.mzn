% Data
int: max_length;
int: num_sequences;
array[1..num_sequences, 1..max_length] of int: sequences;

% Variables
array[1..num_sequences] of var bool: is_safe_sequences;
var int: num_safe = sum(is_safe_sequences);

% Predicates
predicate is_increasing(array[int] of int: sequence) =
	forall(i in 1..length(sequence) - 1)
		(sequence[i + 1] = 0 \/ (sequence[i] < sequence[i + 1])
	);

predicate is_decreasing(array[int] of int: sequence) =
	forall(i in 1..length(sequence) - 1)
		(sequence[i + 1] = 0 \/ (sequence[i] > sequence[i + 1])
	);

predicate is_diff_in_range(array[int] of int: sequence) =
	forall(i in 1..length(sequence) - 1)
		(sequence[i + 1] = 0 \/ (1 <= abs(sequence[i] - sequence[i + 1]) /\ abs(sequence[i] - sequence[i + 1]) <= 3)
	);

predicate is_safe(array[int] of int: sequence) =
	(is_increasing(sequence) \/ is_decreasing(sequence)) /\ is_diff_in_range(sequence);

predicate is_subset_safe(array[int] of int: sequence) =
	exists (removed_idx in 1..max_length) (
		is_safe([sequence[j] | j in 1..max_length where j != removed_idx /\ sequence[j] != 0])
	);

% Check if sequence is safe
constraint
	forall(i in 1..num_sequences)(
    	is_safe_sequences[i] <-> is_safe(sequences[i, 1..max_length]) \/ is_subset_safe(sequences[i, 1..max_length])
	);

solve satisfy;

output [
    "Safe rows: \(is_safe_sequences)\n",
    "Number of safe sequences: \(num_safe)"
];













/*output [
    "Number of safe sequences: \(num_safe)\n"
] ++ [
    "Sequence \(r): ["
    ++ concat([show(sequences[r, c]) ++ if c < max_length then ", " else "" endif | c in 1..max_length])
    ++ "] - " ++ (if fix(is_safe_sequences[r]) then "Safe" else "Not Safe" endif) ++ "\n"
    | r in 1..num_sequences
];*/