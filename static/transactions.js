// Show total
$(document).ready(function() {
    $("table").tablesorter();
    // Select all the table cells in the "VALUE" column
    var values = $("td:nth-child(4)").map(function() {
        return parseFloat($(this).text());
    }).get();
    // Calculate the sum of the values
    var sum = values.reduce(function(a, b) {
        return a + b;
    }, 0);
    // Append the sum to the HTML after the table
    $(".table-container").append("<div>Balance: " + sum + "</div>");
});