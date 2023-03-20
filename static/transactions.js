document.addEventListener("DOMContentLoaded", function() {
    // Select all the table cells in the "VALUE" column
    var cells = document.querySelectorAll("td:nth-child(4)");
    // Extract the numerical values from the cells
    var values = extractValuesFromCells(cells);
    // Calculate the sum of the values
    var sum = calculateSum(values);
    // Create a new div element to display the sum
    var balanceDiv = document.createElement("div");
    balanceDiv.textContent = "Balance: " + sum;
    // Append the div to a container element after the table
    var tableContainer = document.querySelector(".table-container");
    tableContainer.appendChild(balanceDiv);

    function confirmDelete() {
        return confirm("Are you sure you want to delete your account?");
    }

    $(".tablesorter").tablesorter({
        headers: {
            0: { sorter: "shortDate" }, // first column contains date values
            1: { sorter: "text" }, // second column contains text
            2: { sorter: "text" }, // third column contains text
            3: { sorter: "digit" } // fourth column contains numeric values
        }
    });

    var toggleButtons = document.querySelectorAll(".toggle_button");
    for (var i = 0; i < toggleButtons.length; i++) {
    toggleButtons[i].addEventListener("click", function() {
        var formId = this.getAttribute("form-id");
        var formElement = document.getElementById(formId);
        formElement.classList.toggle("hidden");
    });
    }
});


/**
 * Extracts numerical values from an array of table cells.
 * @param {NodeList} cells - An array-like object containing table cell elements.
 * @returns {number[]} An array of numerical values extracted from the cells.
 */
function extractValuesFromCells(cells) {
  var values = [];
  for (var i = 0; i < cells.length; i++) {
      var cellValue = parseFloat(cells[i].textContent);
      values.push(cellValue);
  }
  return values;
}

/**
 * Calculates the sum of an array of numbers.
 * @param {number[]} values - An array of numbers to sum.
 * @returns {number} The sum of all numbers in `values`.
 */
function calculateSum(values) {
  var sum = 0;
  for (var i = 0; i < values.length; i++) {
      sum += values[i];
  }
  return sum;
}

function confirmDeleteTransactions() {
    return confirm("Are you sure you want to delete all of your transactions?");
}