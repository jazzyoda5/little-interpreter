Simple interpreter that can run a language
that is somewhere between Python and Javascript ->
```
a: int = 32; 
if (a > 2) {
    print("Yayy");
} else {
    print(":(");
}
```
or 
```
variable: int = 3 * 3 - 6;
var: int = 70 / 10;
/*
I am a
multiline comment
*/
if (variable < var) {
    print("Whatever1");
} else {
    print("Whatever2");
}
print("Another print for the lolz!");
```

---
SOME RULES


- Variable names can only use [a-zA-Z]
- Type has to be stated on variable assignment -> var: str = "string variable";
- Supported types: int, str, float, bool
- Every statement must be closed of with ";"
unless it is an if else block, otherwise SyntaxError is raised
- Strings must be wrapped like this -> "string"
and not like this -> 'string'
- Print statement takes in only one argument
- No type conversion functions

---
To build:
- Variable declarations? -> a: int = 3;



