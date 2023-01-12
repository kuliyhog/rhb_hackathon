
async function fetchData() {
  await fetch('http://localhost:5000')
  .then((response) => response.json())
  .then((data) => console.log(data));
}