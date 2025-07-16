// Transpiled from EmotiLang

let myNumber = 42; // number
myNumber = (2 + (3 * 5));
let myInput = prompt("Enter input:"); // string
console.log(myInput);
function factorial(n /* number */) /* -> number */ {
  if ((n == 0)) {
    return 1;
  }
  return (n * factorial((n - 1)));
}
console.log(factorial(5));
let counter = 0; // number
while ((counter < 5)) {
  console.log(counter);
  counter = (counter + 1);
}
try {
  throw new Error("Something went wrong");
} catch (e) {
  console.log("Caught error: ");
}