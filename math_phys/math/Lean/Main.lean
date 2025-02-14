import «P1»

def main : IO Unit :=
  IO.println s!"Hello, {hello}!"

axiom wwp (n : Nat) : ∃ n, n + 1 > n
