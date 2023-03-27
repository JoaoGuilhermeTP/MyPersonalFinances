document.addEventListener("DOMContentLoaded", function() {

    // Select all the table cells in the "VALUE" column
    var cells = document.querySelectorAll("td:nth-child(4)");
    // Convert NodeList object into Array and slice off the first element
    var cells = Array.from(cells).slice(1);
    // Extract the numerical values from the cells
    var values = extractValuesFromCells(cells);
    // Calculate the sum of the values
    var sum = calculateSum(values);
    // Create a new div element to display the sum
    var balanceDiv = document.createElement("div");
    balanceDiv.textContent = "Balance: " + sum;
    balanceDiv.style.fontSize = "120%";
    balanceDiv.style.display = "flex";
    balanceDiv.style.justifyContent = "right";
    // Append the div to a container element after the table
    var tableCard = document.querySelector(".tableCard");
    tableCard.appendChild(balanceDiv);


    $(".tablesorter").tablesorter({
        headers: {
            0: { sorter: "shortDate" }, // first column contains date values
            1: { sorter: "text" }, // second column contains text
            2: { sorter: "text" }, // third column contains text
            3: { sorter: "digit" } // fourth column contains numeric values
        }
    });



    var toggleButtons = document.querySelectorAll(".toggle_button");
    toggleButtons.forEach(function(toggleButton) {
        toggleButton.addEventListener("click", function() {
            var hiddenElementId = this.getAttribute("hiddenElementId");
            var hiddenElement = document.getElementById(hiddenElementId);
            hiddenElement.classList.toggle("hidden");
            if (hiddenElement.classList.contains("hidden")) {
                hiddenElement.style.display = "";
                hiddenElement.style.flexDirection = "";
            }
            else {
                if (hiddenElementId == "formRow") {
                    if (viewportWidth <= 700) {
                        hiddenElement.style.display = "flex";
                        hiddenElement.style.flexDirection = "column";
                    }
                    else
                    {
                        hiddenElement.style.display = "";
                        hiddenElement.style.flexDirection = "";
                    }

                }
            }
        });
    });

    var viewportWidth = window.innerWidth;
    var formRow = document.getElementById("formRow")
    window.onresize = function() {
    viewportWidth = window.innerWidth;
    if  (!(formRow.classList.contains("hidden"))) {
        if (viewportWidth <= 700) {
            formRow.style.display = "flex";
            formRow.style.flexDirection = "column";
        }
        else {
            formRow.style.display = "";
            formRow.style.flexDirection = "";
        }
    }

}
});


/**
 * Handles "click" events on toggle buttons.
 * @param {Event} event - The event object.
 */
function showElement() {

}



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