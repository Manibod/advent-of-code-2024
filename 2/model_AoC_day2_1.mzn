% data
int: max_length;
int: num_sequences;
array[1..num_sequences, 1..max_length] of int: sequences;

% variables
array[1..num_sequences] of var bool: is_safe_sequences;

% predicates
predicate correct_zero_padding(array[int] of int: sequence) =
	forall(i in 1..max_length-1) (
        (sequence[i] = 0) -> (sequence[i+1] = 0)
    );

predicate is_increasing(array[int] of int: sequence) =
	forall(i in 1..length(sequence) - 1)
		(sequence[i + 1] = 0 \/ (sequence[i] < sequence[i+1]));

predicate is_decreasing(array[int] of int: sequence) =
	forall(i in 1..length(sequence) - 1)
		(sequence[i + 1] = 0 \/ (sequence[i] > sequence[i+1]));

predicate is_diff_in_range(array[int] of int: sequence) =
	forall(i in 1..length(sequence) - 1)
		(sequence[i + 1] = 0 \/ (1 <= abs(sequence[i] - sequence[i + 1]) /\ abs(sequence[i] - sequence[i + 1]) <= 3));

predicate is_safe(array[int] of int: sequence) =
	(is_increasing(sequence) \/ is_decreasing(sequence)) /\ is_diff_in_range(sequence);

% contraint: 0s only at the end
constraint
    forall(i in 1..num_sequences) (
        correct_zero_padding(sequences[i, 1..])
    );
   
% constraint: check if sequence is safe
constraint
	forall(i in 1..num_sequences)(
    	is_safe_sequences[i] <-> is_safe(sequences[i, 1..max_length])
	);

var int: num_safe = sum(is_safe_sequences);

solve satisfy;

output [
    "Number of safe sequences: \(num_safe)\n",
    "Safe rows: \(is_safe_sequences)"
];

/*output [
    "Number of safe sequences: \(num_safe)\n"
] ++ [
    "Sequence \(r): ["
    ++ concat([show(sequences[r, c]) ++ if c < max_length then ", " else "" endif | c in 1..max_length])
    ++ "] - " ++ (if fix(is_safe_sequences[r]) then "Safe" else "Not Safe" endif) ++ "\n"
    | r in 1..num_sequences
];*/