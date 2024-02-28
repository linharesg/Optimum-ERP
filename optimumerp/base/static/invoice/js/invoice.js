jQuery(function () {
    $print = $(".print")

    $print.on("click", function() {
        window.print();
    })
})