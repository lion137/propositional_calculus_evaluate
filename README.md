Propositional Calculus calculator written in Python. It takes an expression (of propositional logic) in form:    
```(A && (A =>B) => B)```    
Only single letters (capital or small) can be used as operands, the only symbol parser recognizes are:    
```&&``` - and;    
```||``` - or;    
```=>``` - implication;   
```<=>```- biconditional ( if only if);    
```~```  - negation.    
This only one file and contains repl - after running, it displays promt asking for expression to evaluate;    
after entering a proper propositional logic formula program displays, very selfexplanatory communicates:    
```Formula is tautology```;    
```Formula is satisfiable```;    
```Formula is not satisfiable``` - means, that negation of the formula is a tautology.    
Could be also used online here:    
https://repl.it/@lion137/propositionalcalculluseval    
More info here:
https://lion137.blogspot.com/2019/10/propositional-calculus-evaluation.html
