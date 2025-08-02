# Mac 1984 Example: Simple Calculator
program SimpleCalculator;
var
  num1, num2, result: real;
  operation: char;

begin
  writeln('=== Simple Calculator ===');
  writeln;
  
  write('Enter first number: ');
  readln(num1);
  
  write('Enter operation (+, -, *, /): ');
  readln(operation);
  
  write('Enter second number: ');
  readln(num2);
  
  case operation of
    '+': result := num1 + num2;
    '-': result := num1 - num2;
    '*': result := num1 * num2;
    '/': begin
           if num2 <> 0 then
             result := num1 / num2
           else
           begin
             writeln('Error: Division by zero!');
             halt;
           end;
         end;
    else
    begin
      writeln('Error: Invalid operation!');
      halt;
    end;
  end;
  
  writeln;
  writeln(num1:0:2, ' ', operation, ' ', num2:0:2, ' = ', result:0:2);
  writeln;
  writeln('Press Enter to exit...');
  readln;
end.
